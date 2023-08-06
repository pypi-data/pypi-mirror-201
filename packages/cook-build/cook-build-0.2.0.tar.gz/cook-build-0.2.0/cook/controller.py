import asyncio
import logging
import os
from pathlib import Path
from sqlite3 import Connection
from typing import Dict, Iterable, Optional, Set, Tuple, TYPE_CHECKING, Union
from . import util

if TYPE_CHECKING:
    from .manager import Manager
    from .task import Task


LOGGER = logging.getLogger(__name__)
QUERIES = {
    "schema": """
    CREATE TABLE IF NOT EXISTS "files" (
        "name" TEXT PRIMARY KEY,
        "size" INTEGER NOT NULL,
        "digest" TEXT NOT NULL
    )
    """,
    "select": """
        SELECT "size", "digest" FROM "files" WHERE "name" = :name
    """,
    "upsert": """
        INSERT INTO "files" ("name", "size", "digest") VALUES (:name, :size, :digest)
        ON CONFLICT("name") DO UPDATE SET "size" = :size, "digest" = :digest
    """
}


class Controller:
    """
    Controller to manage dependencies and execute tasks.
    """
    def __init__(self, manager: "Manager", connection: Connection, num_concurrent: int = 1) -> None:
        self.manager = manager
        self.connection = connection
        self.dependencies = manager.resolve_dependencies()
        self.status: Dict[Task, bool] = {}
        self.futures: Dict[Task, asyncio.Future] = {}
        self.size_digest: Dict[str, Tuple[int, str]] = {}
        self.semaphore = asyncio.Semaphore(num_concurrent)

    def resolve_stale_tasks(self, tasks: Optional[Iterable["Task"]] = None) -> Set["Task"]:
        tasks = tasks or self.manager.tasks.values()
        for task in tasks:
            self.is_stale(task)
        return {task for task, is_stale in self.status.items() if is_stale}

    def path_to_name(self, path: Union[str, Path]) -> str:
        """
        Convert a path to a unique name by resolving it relative to the working directory.
        """
        return str(Path(path).resolve().relative_to(os.getcwd()))

    def evaluate_size_digest(self, path: Union[str, Path]) -> Tuple[int, str]:
        """
        Evaluate the size and hex digest of a file.
        """
        path = Path(path)
        name = self.path_to_name(path)
        if result := self.size_digest.get(name):
            return result
        size = path.stat().st_size
        digest = util.evaluate_hexdigest(path)
        self.size_digest[name] = size, digest
        return size, digest

    def _is_self_stale(self, task: "Task") -> bool:
        """
        Determine whether a task is *itself* stale irrespective of other tasks it may depend on.
        """
        # If there are no targets or the targets are missing, the task is stale.
        if not task.targets:
            LOGGER.debug('%s is "stale" because it has no targets', task)
            return True
        if not all(path.is_file() for path in task.targets):
            LOGGER.debug("%s is stale because one of its targets is missing", task)
            return True

        # If any dependency is outdated, the task is stale.
        for dependency in task.dependencies:
            name = self.path_to_name(dependency)
            result = self.connection.execute("SELECT size, digest FROM files WHERE name = :name",
                                             {"name": name}).fetchone()
            if result is None:
                LOGGER.debug("%s is stale because its dependency `%s` does not have a hash entry",
                             task, name)
                return True
            expected_size, expected_digest = result
            if dependency.stat().st_size != expected_size \
                    or util.evaluate_hexdigest(dependency) != expected_digest:
                LOGGER.debug("%s is stale because its dependency `%s` has changed", task, name)
                return True

        LOGGER.debug("%s is up to date", task)
        return False

    def is_stale(self, task: "Task", recursive: bool = True) -> bool:
        if not recursive:
            return self._is_self_stale(task)

        # Return the status if we have already evaluated it.
        if (status := self.status.get(task)) is not None:
            return status

        # We will evaluate all dependents (rather than using "any" with a generator expression)
        # because we want to find all stale tasks. Not just the first one in the hierarchy.
        dependents = [self.is_stale(dependent) for dependent in self.dependencies.get(task, [])]
        if any(dependents):
            return self.status.setdefault(task, True)

        return self.status.setdefault(task, self._is_self_stale(task))

    async def execute(self, task: "Task") -> None:
        # If there already is a future, just wait for it and return.
        if future := self.futures.get(task):
            await future
            return

        # Create a new future and add it to the lookup.
        future = self.futures.setdefault(task, asyncio.Future())

        # First execute all the dependents.
        await asyncio.gather(*(self.execute(dependency) for dependency in
                               self.dependencies.get(task, [])))

        # Then do the actual processing within the semaphore to limit concurrency.
        try:
            if self.is_stale(task):
                async with self.semaphore:
                    LOGGER.debug("started %s", task)
                    with util.Timer() as timer:
                        await task.execute()
                    LOGGER.debug("completed %s in %.3f seconds", task, timer.duration)

                # Validate that all desired targets exist.
                for target in task.targets:
                    if not target.is_file():
                        raise FileNotFoundError(f"`{task}` did not create `{target}`")
                    LOGGER.debug("`%s` created `%s`", task, target)

                # Update the state and write to the database.
                self.status[task] = False
                records = []
                for dependency in task.dependencies:
                    size, digest = self.evaluate_size_digest(dependency)
                    records.append({
                        "name": self.path_to_name(dependency),
                        "size": size,
                        "digest": digest,
                    })
                self.connection.executemany(QUERIES["upsert"], records)
        except Exception as ex:
            message = f"failed to execute {task}: {ex}"
            LOGGER.exception(message)
            error = util.FailedTaskError(message, task=task)
            error.__cause__ = ex
            future.set_exception(error)
        else:
            future.set_result(None)

        await future

    def execute_sync(self, *tasks: "Task") -> None:
        util.run_until_complete(*(self.execute(task) for task in tasks))

    def reset(self, *tasks: "Task") -> None:
        names = []
        for task in tasks:
            for dependency in task.dependencies:
                names.append({"name": self.path_to_name(dependency)})
        self.connection.executemany("DELETE FROM files WHERE name = :name", names)
        self.connection.commit()
        LOGGER.info("reset %d %s", len(tasks), "task" if len(tasks) == 1 else "tasks")

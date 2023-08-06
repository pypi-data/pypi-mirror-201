from __future__ import annotations
import asyncio
import contextlib
import hashlib
import inspect
import os
from pathlib import Path
from time import time
from typing import Dict, Hashable, Iterable, List, Optional, Tuple, TYPE_CHECKING, Union


if TYPE_CHECKING:
    from .task import Task


PathOrStr = Union[Path, str]


def find_cycle(dependencies: Dict[Hashable, Iterable[Hashable]]) -> Optional[List[Hashable]]:
    """
    Find a cycle in a list of dependencies.
    """
    raise NotImplementedError


def evaluate_hexdigest(path: PathOrStr, size=2 ** 16, hasher: str = "sha1") -> str:
    hasher = hashlib.new(hasher)
    path = Path(path)
    with path.open("rb") as fp:
        while chunk := fp.read(size):
            hasher.update(chunk)
    return hasher.hexdigest()


def run_until_complete(*awaitables) -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(*awaitables))


class Timer:
    def __init__(self):
        self.start = None

    def __enter__(self) -> Timer:
        self.start = time()
        return self

    def __exit__(self, *_) -> None:
        self.end = time()

    @property
    def duration(self):
        return self.end - self.start


class CookError(Exception):
    pass


class FailedTaskError(Exception):
    def __init__(self, *args: object, task: "Task") -> None:
        super().__init__(*args)
        self.task = task


@contextlib.contextmanager
def working_directory(path: PathOrStr) -> Path:
    path = Path(path)
    original = Path.cwd()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(original)


def get_location() -> Tuple[str, int]:
    """
    Get the first location in the call stack which is not part of the `cook` package.

    Returns:
        Location as a tuple :code:`(filename, lineno)`.
    """
    frame = inspect.currentframe()
    while frame.f_globals.get("__name__", "<unknown>").startswith("cook"):
        frame = frame.f_back
    return frame.f_code.co_filename, frame.f_lineno

r"""
Actions
-------

Actions are performed when tasks are executed. Builtin actions include calling python functions
using :class:`.FunctionAction`, running subprocesses using :class:`.SubprocessAction`, executing
commands using :class:`.ShellAction`, and composing multiple actions using
:class:`.CompositeAction`.

Custom contexts can be implemented by inheriting from :class:`.Action` and implementing the
:meth:`~.Action.execute` method which receives a :class:`~.task.Task`. The method should execute the
action; its return value is ignored. For example, the following action waits for a specified time.

.. doctest::

    >>> from asyncio import sleep
    >>> from cook.actions import Action
    >>> from cook.task import Task
    >>> from cook.util import run_until_complete
    >>> from time import time

    >>> class SleepAction(Action):
    ...     def __init__(self, delay: float) -> None:
    ...         self.delay = delay
    ...
    ...     async def execute(self, task: Task) -> None:
    ...         start = time()
    ...         await sleep(self.delay)
    ...         print(f"time: {time() - start:.3f}")

    >>> action = SleepAction(0.1)
    >>> action.execute_sync(None)
    time: 0.1...
"""
import asyncio
from subprocess import SubprocessError
from typing import Awaitable, Callable, TYPE_CHECKING
from . import util


if TYPE_CHECKING:
    from .task import Task


class Action:
    """
    Action to perform when a task is executed.
    """
    async def execute(self, task: "Task") -> None:
        """
        Execute the action.
        """
        raise NotImplementedError

    def execute_sync(self, task: "Task") -> None:
        """
        Execute the action synchronously.
        """
        util.run_until_complete(self.execute(task))


class FunctionAction(Action):
    """
    Action wrapping a python callable. Both synchronous functions and :code:`async` functions are
    supported.

    Args:
        func: Function to call which must accept a :class:`~.task.Task` as its first argument.
        *args: Additional positional arguments.
        **kwargs: Keyword arguments.
    """
    def __init__(self, func: Callable, *args, **kwargs) -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    async def execute(self, task: "Task") -> None:
        result = self.func(task, *self.args, **self.kwargs)
        if isinstance(result, Awaitable):
            await result


class SubprocessAction(Action):
    """
    Run a subprocess.

    Args:
        program: Program to run.
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Example:

        .. doctest::

            >>> from cook.actions import SubprocessAction
            >>> from pathlib import Path

            >>> action = SubprocessAction("touch", "hello.txt")
            >>> action.execute_sync(None)
            >>> Path("hello.txt").is_file()
            True
    """
    def __init__(self, program: str, *args, **kwargs) -> None:
        self.program = program
        self.args = args
        self.kwargs = kwargs

    async def execute(self, task: "Task") -> None:
        process = await asyncio.create_subprocess_exec(self.program, *self.args, **self.kwargs)
        status = await process.wait()
        if status:
            raise SubprocessError(f"executing {[self.program, *self.args]} returned status code "
                                  f"{status}")


class ShellAction(Action):
    r"""
    Execute a shell command.

    Args:
        cmd: Command to execute.
        *args: Additional positional arguments.
        **kwargs: Keyword arguments.

    Example:

        .. doctest::

            >>> from cook.actions import ShellAction
            >>> from pathlib import Path

            >>> action = ShellAction("echo hello > world.txt")
            >>> action.execute_sync(None)
            >>> Path("world.txt").read_text()
            'hello\n'
    """
    def __init__(self, cmd: str, *args, **kwargs) -> None:
        self.cmd = cmd
        self.args = args
        self.kwargs = kwargs

    async def execute(self, task: "Task") -> None:
        process = await asyncio.create_subprocess_shell(self.cmd, *self.args, **self.kwargs)
        status = await process.wait()
        if status:
            raise SubprocessError(f"executing `{self.cmd}` returned status code {status}")


class CompositeAction(Action):
    """
    Execute multiple actions in order.

    Args:
        *actions: Actions to execute.
    """
    def __init__(self, *actions: Action) -> None:
        self.actions = actions

    async def execute(self, task: "Task") -> None:
        for action in self.actions:
            await action.execute(task)

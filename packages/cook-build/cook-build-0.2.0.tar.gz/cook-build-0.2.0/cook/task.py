from __future__ import annotations
from pathlib import Path
from typing import List, Optional, Tuple, TYPE_CHECKING
from . import util


if TYPE_CHECKING:
    from .util import PathOrStr
    from .actions import Action


class Task:
    """
    Task to be executed.
    """
    def __init__(
            self,
            name: str,
            *,
            dependencies: Optional[List["PathOrStr"]] = None,
            targets: Optional[List["PathOrStr"]] = None,
            action: Optional[Action] = None,
            task_dependencies: Optional[List[Task]] = None,
            location: Optional[Tuple[str, int]] = None,
            ) -> None:
        self.name = name
        self.dependencies = dependencies or []
        self.targets = [Path(path) for path in (targets or [])]
        self.action = action
        self.task_dependencies = task_dependencies or []
        self.location = location or util.get_location()

    async def execute(self) -> None:
        if self.action:
            await self.action.execute(self)

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        filename, lineno = self.location
        return f"<task `{self.name}` @ {filename}:{lineno}>"

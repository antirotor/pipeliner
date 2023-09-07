from abc import ABC, abstractmethod
from typing import List

from pyglet.shapes import BorderedRectangle, ShapeBase
from pyglet.graphics import Batch

from pipeliner.actors.node import Node
from pipeliner.tasks.state import (
    TaskState,
    NotStartedState,
    InProgressState,
    DoneState,
    FailedState,
)
from pipeliner.tasks.status import (
    TaskStatus,
    NotReadyStatus,
    ReadyStatus,
    InProgressStatus,
    DoneStatus,
    ReviewStatus,
    ApprovedStatus,
    RejectedStatus,
)
from pipeliner.tasks.type import (
    TaskType,
    EmptyTaskType,
)


class Task(ABC):
    type: TaskType
    state: TaskState
    status: TaskStatus
    name: str
    id: int
    assignee: Node
    progress: float

    _batch: Batch

    @abstractmethod
    def get_shapes(self) -> List[ShapeBase]:
        return []


class EmptyTask(Task):
    def __init__(self, batch: Batch, name: str = "Empty", assignee: Node = None):
        self.type = EmptyTaskType()
        self.state = InProgressState
        self.status = ReadyStatus
        self.name = name
        self.id = 0
        self.assignee = assignee
        self.progress = 0.0
        
        self._batch = batch


    def get_shapes(self, x: int, y: int) -> List[ShapeBase]:
        """Get the shapes that represent this task.
        
        Resulting shape is combination of tasks type and tasks state.

        Args:
            x (int): X coordinate of the task.
            y (int): Y coordinate of the task.

        Todo:
            * Add support for different shapes for different states.
            * Add support for different shapes for different types.

        Returns:
            List[ShapeBase]: List of shapes that represent this task.

        """
        shapes = super().get_shapes()
        shapes += self.type.get_shapes(x, y, self._batch)
        return shapes
    

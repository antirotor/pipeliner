"""Task definitions.

Tasks are the smallest unit of work in the pipeline. They are assigned to
nodes and they can be in different states. Tasks can be of different types
and they can have different statuses.

Every node can accept tasks of different types. For example, a node can accept 
only compositing tasks or only rendering tasks. This is defined by the node
itself. Nodes can also have different failure rates. This means that a node
can fail a task with a certain probability. This is also defined by the node
itself.

"""
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
    CompositingTaskType
)


class Task(ABC):
    """Task base class.
    
    Task has type, state and status. Task is assigned to a node and it has
    a progress and difficulty. Progress is a value between 0 and 1. Difficulty
    is a value between 0 and 1. Difficulty is used to calculate the time it
    takes to complete the task. Difficulty is calculated by the node based on
    the type of the task and the level of the node. For example, a compositing
    task can have a difficulty of 0.5 and a rendering task can have a difficulty
    of 0.8. This means that a rendering task takes longer to complete than a
    compositing task. Difficulty is also affected by the level of the node. For
    example, a compositing task can have a difficulty of 0.5 on a level 1 node
    and a difficulty of 0.4 on a level 2 node. This means that a compositing
    task takes longer to complete on a level 1 node than on a level 2 node.

    Difficulty also affects the failure rate of the node. For example, a
    compositing task can have a failure rate of 0.1 on a level 1 node and a
    failure rate of 0.05 on a level 2 node. This means that a compositing task
    is more likely to fail on a level 1 node than on a level 2 node.

    
    """
    type: TaskType = EmptyTaskType()
    state: TaskState = NotStartedState()
    status: TaskStatus = NotReadyStatus()
    name: str
    id: int
    assignee: Node
    progress: float
    difficulty: float
    

    _batch: Batch

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
        shapes = []
        shapes += self.type.get_shapes(x, y, self._batch)
        shapes += self.state.get_shapes(x, y, self._batch)
        # shapes += self.status.get_shapes(x, y, self._batch)
        return shapes


class EmptyTask(Task):
    """Empty task.
    
    This is placeholder task that is used to fill the pipeline. It is used
    to fill the pipeline when there are no tasks available.

    """
    def __init__(self, batch: Batch, name: str = "Empty", assignee: Node = None):
        self.name = name
        self.id = 0
        self.assignee = assignee
        self.progress = 0.0
        
        self._batch = batch

class SimpleCompositingTask(Task):
    def __init__(self, batch: Batch, name: str = "Simple Compositing", assignee: Node = None):
        super().__init__(batch, name, assignee)
        self.type = CompositingTaskType()
        self.id = 1
        self.difficulty = 0.1


class MediumCompositingTask(Task):
    def __init__(self, batch: Batch, name: str = "Medium Compositing", assignee: Node = None):
        super().__init__(batch, name, assignee)
        self.type = CompositingTaskType()
        self.id = 2
        self.difficulty = 0.5

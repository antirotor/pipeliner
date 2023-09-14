"""Definition of task states."""
from pyglet.graphics import Batch
from pyglet.shapes import ShapeBase, Rectangle
from typing import List
from abc import ABC, abstractmethod
from pipeliner.constants import TASK_SIZE


class TaskState(ABC):
    """State base class.
    
    Every task has a state, which is represented by a color and a name.
    State needs to define its visual representation to be combined finally
    with the task and status of the task.

    """
    name: str
    color: tuple

    def get_shapes(self, x: int, y: int, batch: Batch) -> List[ShapeBase]:
        return [
            Rectangle(x + TASK_SIZE-2, y + (TASK_SIZE - 2), 2, 2, color=self.color, batch=batch),
        ]

class NotStartedState(TaskState):
    """Not started state.
    
    This state is used for tasks that are not started yet by the node.
    This is the default state of a task.

    """
    def __init__(self):
        self.name = "Not Started"
        self.color = (128, 128, 128)

class InProgressState(TaskState):
    """In progress state.
    
    Once a task is started by the node, it is in progress.
    
    """
    def __init__(self):
        self.name = "In Progress"
        self.color = (96, 96, 200)

class DoneState(TaskState):
    """Done state.
    
    When a task is finished, it is in done state or failed state.

    """
    def __init__(self):
        self.name = "Done"
        self.color = (128, 200, 128)

class FailedState(TaskState):
    """Failed state.
    
    Every node has its failure rate that affects the tasks. Lower the level of
    the node, higher the failure rate. When a task fails, it is in failed state.
    Failed task can be detected by the Supervisor node and can be reassigned to
    another node. Higher the level of the Supervisor node, higher the chance of
    detecting the failed task.

    """
    def __init__(self):
        self.name = "Failed"
        self.color = (200, 150, 64)

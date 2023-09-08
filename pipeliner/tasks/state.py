from pyglet.graphics import Batch
from pyglet.shapes import ShapeBase, Rectangle
from typing import List
from abc import ABC, abstractmethod
from pipeliner.constants import TASK_SIZE


class TaskState(ABC):
    name: str
    color: tuple

    def get_shapes(self, x: int, y: int, batch: Batch) -> List[ShapeBase]:
        return [
            Rectangle(x + TASK_SIZE-2, y + (TASK_SIZE - 2), 2, 2, color=self.color, batch=batch),
        ]

class NotStartedState(TaskState):
    def __init__(self):
        self.name = "Not Started"
        self.color = (128, 128, 128)

class InProgressState(TaskState):
    def __init__(self):
        self.name = "In Progress"
        self.color = (96, 96, 200)

class DoneState(TaskState):
    def __init__(self):
        self.name = "Done"
        self.color = (128, 200, 128)

class FailedState(TaskState):
    def __init__(self):
        self.name = "Failed"
        self.color = (200, 150, 64)

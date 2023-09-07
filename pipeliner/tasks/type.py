from abc import ABC, abstractmethod
from typing import List

from pyglet.graphics import Batch
from pyglet.shapes import ShapeBase
from pyglet.shapes import Rectangle, BorderedRectangle


class TaskType(ABC):
    name: str
    color: tuple

    @abstractmethod
    def get_shapes(self, x: int, y: int, batch: Batch) -> List[ShapeBase]:
        return []

class EmptyTaskType(TaskType):
    def __init__(self):
        self.name = "Empty"
        self.color = (32, 32, 32)

    def get_shapes(self, x: int, y: int, batch: Batch) -> List[ShapeBase]:
        return [
            Rectangle(x, y, 5, 5, color=self.color, batch=batch),
        ]

class CompositingTaskType(TaskType):
    def __init__(self):
        self.name = "Compositing"
        self.color = (200, 128, 128)

class RenderingTaskType(TaskType):
    def __init__(self):
        self.name = "Rendering"
        self.color = (128, 200, 128)

class ModelingTaskType(TaskType):
    def __init__(self):
        self.name = "Modeling"
        self.color = (128, 128, 200)

class RotoscopingTaskType(TaskType):
    def __init__(self):
        self.name = "Rotoscoping"
        self.color = (200, 200, 128)
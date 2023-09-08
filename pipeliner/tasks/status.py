from abc import ABC
from pipeliner.constants import TASK_SIZE
from pyglet.graphics import Batch
from pyglet.shapes import ShapeBase, BorderedRectangle
from typing import List



class TaskStatus(ABC):
    name: str
    color: tuple

    def get_shapes(self, x: int, y: int, batch: Batch) -> List[ShapeBase]:
        return [
            BorderedRectangle(
                x + TASK_SIZE-2, y + TASK_SIZE-2,
                TASK_SIZE, TASK_SIZE,
                border=1, border_color=self.color,
                color=(0, 0, 0, 0),
                batch=batch),
        ]

class NotReadyStatus(TaskStatus):
    def __init__(self):
        self.name = "Not Ready"
        self.color = (128, 128, 128)

class ReadyStatus(TaskStatus):
    def __init__(self):
        self.name = "Ready"
        self.color = (128, 200, 128)

class InProgressStatus(TaskStatus):
    def __init__(self):
        self.name = "In Progress"
        self.color = (128, 128, 200)

class DoneStatus(TaskStatus):
    def __init__(self):
        self.name = "Done"
        self.color = (200, 128, 128)

class ReviewStatus(TaskStatus):
    def __init__(self):
        self.name = "Review"
        self.color = (200, 200, 128)

class ApprovedStatus(TaskStatus):
    def __init__(self):
        self.name = "Approved"
        self.color = (128, 200, 200)

class RejectedStatus(TaskStatus):
    def __init__(self):
        self.name = "Rejected"
        self.color = (200, 128, 200)

from abc import ABC

from pyglet.shapes import BorderedRectangle

from pypeliner.actors.node import Node
from pypeliner.tasks.state import TaskState
from pypeliner.tasks.status import TaskStatus
from pypeliner.tasks.type import TaskType


class Task(ABC):
    type: TaskType
    state: TaskState
    status: TaskStatus
    name: str
    id: int
    assignee: Node
    progress: float


from abc import ABC

from pyglet.shapes import BorderedRectangle

from pipeliner.actors.node import Node
from pipeliner.tasks.state import TaskState
from pipeliner.tasks.status import TaskStatus
from pipeliner.tasks.type import TaskType


class Task(ABC):
    type: TaskType
    state: TaskState
    status: TaskStatus
    name: str
    id: int
    assignee: Node
    progress: float


from abc import ABC, abstractmethod

class TaskState(ABC):
    name: str
    color: tuple

class NotStartedState(TaskState):
    def __init__(self):
        self.name = "Not Started"
        self.color = (128, 128, 128)

class InProgressState(TaskState):
    def __init__(self):
        self.name = "In Progress"
        self.color = (128, 128, 200)

class DoneState(TaskState):
    def __init__(self):
        self.name = "Done"
        self.color = (200, 128, 128)

class FailedState(TaskState):
    def __init__(self):
        self.name = "Failed"
        self.color = (200, 128, 200)

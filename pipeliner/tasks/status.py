from abc import ABC


class TaskStatus(ABC):
    name: str
    color: tuple

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

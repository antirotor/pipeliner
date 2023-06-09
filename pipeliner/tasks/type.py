class TaskType(object):
    name: str
    color: tuple

class CompositingTask(TaskType):
    def __init__(self):
        self.name = "Compositing"
        self.color = (200, 128, 128)

class RenderingTask(TaskType):
    def __init__(self):
        self.name = "Rendering"
        self.color = (128, 200, 128)

class ModelingTask(TaskType):
    def __init__(self):
        self.name = "Modeling"
        self.color = (128, 128, 200)

class RotoscopingTask(TaskType):
    def __init__(self):
        self.name = "Rotoscoping"
        self.color = (200, 200, 128)
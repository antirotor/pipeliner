import pyglet
from pypeliner.actors import Node
from pypeliner.actors.node import Bounds, Point
from pypeliner.tasks import Task
from pypeliner.util import get_in_connection, get_out_connection

class Artist(Node):

    def get_bounds(self) -> Bounds:
        return Bounds(self.x, self.y, self.x + self._square_size, self.y + self._square_size)

    def __init__(
            self, batch: pyglet.graphics.Batch,
            level: int = 1, x: int = 0, y: int = 0, state: int = 0):
        super().__init__(batch, level, x, y, state)
        self.color = (128, 200, 128, 255)
        self.name = f"A:{self.level}"
        self._square_size = 64
        self._left_pad = 10
        self._right_pad = 10
        self._line_width = 2
        self._background_color = (0, 0, 0, 255)
        self.current_hour = 4
        self.in_port_position_bound = Bounds(0, 0, 0, 0)
        self.out_port_position_bound = Bounds(0, 0, 0, 0)

        self.in_port_position: Point = Point(0, 0)
        self.out_port_position: Point = Point(0, 0)


    def level_up(self):
        self.level += 1
        self.production_rate += 0.5
        self.work_hours += 1

    def _get_main_square(self):

        shapes = [
            pyglet.shapes.BorderedRectangle(
                x=self.x + self._left_pad, y=self.y,
                width=self._square_size, height=self._square_size,
                border=self._line_width,
                color=self._background_color,
                border_color=self.color, batch=self.batch),
            pyglet.text.Label(
                self.name,
                bold=True,
                font_name="Arial",
                font_size=24,
                x=self.x + (self._left_pad + self._square_size + self._right_pad) // 2,
                y=self.y + self._square_size // 2,
                anchor_x="center", anchor_y="center",
                color=self.color, batch=self.batch),
        ]
        self.in_port_position.x = self.x - 5
        self.in_port_position.y = self.y + (self._square_size // 2)
        self.out_port_position.x = self.x + self._square_size + 20
        self.out_port_position.y = self.y + (self._square_size // 2)

        shapes += get_in_connection(
            (self.x-5, self.y + (self._square_size // 2)),
            self.batch, self.in_port_position_bound)
        shapes += get_out_connection(
            (self.x + self._square_size + 20, self.y + (self._square_size // 2)),
            self.batch, self.out_port_position_bound)
        return shapes

    def _get_work_hours_bar(self):
        hour_step = (self._square_size - 2) / self.work_hours
        bar_height = self.current_hour * hour_step
        if self.current_hour >= self.work_hours:
            bar_height = self._square_size - 2

        return [
            pyglet.shapes.BorderedRectangle(
                x=self.x + 3, y=self.y,
                width=5, height=self._square_size,
                border=1,
                color=self._background_color,
                border_color=self.color, batch=self.batch),
            pyglet.shapes.Rectangle(
                x=self.x + 4, y=self.y + 1,
                width=3, height=bar_height,
                color=(64, 64, 64, 255), batch=self.batch)
        ]

    def draw(self):
        shapes = []
        shapes += self._get_main_square()
        shapes += self._get_work_hours_bar()

        for shape in shapes:
            shape.draw()

    def get_task_shapes(self):
        shapes = []
        task: Task
        for task in self.tasks:
            shapes += self.get_task_shape(task)
        return shapes

    def update(self, delta_time: float):
        self.current_hour += delta_time
        if self.current_hour >= self.work_hours:
            self.current_hour = 0
            self.state = 0
            self.color = (128, 200, 128, 255)
            self.tasks = []
        for connection in self.connections:
            connection.update(delta_time)

    def get_task_shape(self, task: Task):
        ...

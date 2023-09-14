"""Artist node that can do any task.

Artist is a basic workhorse of the game, it can do any task. It has a limited
number of task slots and can only work for a limited number of hours per day.
It is rendered as a green square with a letter A in it.

"""
import pyglet
from pipeliner.actors import Node
from pipeliner.actors.node import Bounds, Point
from pipeliner.tasks import EmptyTask, Task
from pipeliner.tasks.type import (
    EmptyTaskType,
    CompositingTaskType,
    RenderingTaskType,
    ModelingTaskType,
    RotoscopingTaskType,
)

from pipeliner.util import get_in_connection, get_out_connection
from pipeliner.constants import ARTIST_DEFAULT_TASK_SLOTS, ARTIST_DEFAULT_WORK_HOURS


class Artist(Node):
    """Generalist Artist node that can do any task."""

    def get_bounds(self) -> Bounds:
        return Bounds(self.x, self.y, self.x + self._square_size, self.y + self._square_size)

    def __init__(
            self, batch: pyglet.graphics.Batch,
            level: int = 1, x: int = 0, y: int = 0):
        super().__init__(batch, level, x, y)
        self.color = (128, 200, 128, 255)
        self.name = f"A"
        
        self.work_hours = ARTIST_DEFAULT_WORK_HOURS
        self.current_hour = 0

        self.task_slots = ARTIST_DEFAULT_TASK_SLOTS
        self.accept_types = {
            EmptyTaskType, CompositingTaskType, RenderingTaskType,
            ModelingTaskType, RotoscopingTaskType
        }
        
        self.provide_types = {
            EmptyTaskType, CompositingTaskType, RenderingTaskType,
            ModelingTaskType, RotoscopingTaskType
        }

        self._square_size = 64
        self._left_pad = 10
        self._right_pad = 10
        self._line_width = 4
        self._background_color = (0, 0, 0, 255)
        
        self._current_task = EmptyTask(batch, assignee=self)

        self.in_port_position_bound = Bounds(0, 0, 0, 0)
        self.out_port_position_bound = Bounds(0, 0, 0, 0)

        self.in_port_position: Point = Point(0, 0)
        self.out_port_position: Point = Point(0, 0)


    def level_up(self) -> None:
        """Level up the node.
        
        This method calculates the new production rate and work hours
        for the node.

        Todo:
            This method should be moved to the base class.

        """
        self.level += 1
        self.production_rate += 0.5
        self.work_hours += 1

    def _get_main_square(self):
        """Draw the main square of the node."""

        shapes = [
            pyglet.shapes.BorderedRectangle(
                x=self.x + self._left_pad, y=self.y,
                width=self._square_size, height=self._square_size,
                border=self._line_width,
                color=self._background_color,
                border_color=self.color, batch=self.batch),
            *self._get_io_load_indicator(),
            pyglet.text.Label(
                self.name,
                bold=True,
                font_name="Arial",
                font_size=38,
                x=self.x + (self._left_pad + self._square_size + self._right_pad) // 2 - 2 ,
                y=self.y + self._square_size // 2,
                anchor_x="center", anchor_y="center",
                color=self.color, batch=self.batch),
            pyglet.text.Label(
                str(self.level),
                bold=True,
                font_name="Arial",
                font_size=16,
                x=self.x + self._left_pad + self._square_size - 10 - self._right_pad,
                y=self.y + self._square_size - 20,
                anchor_x="left", anchor_y="center",
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
        """Draw the work hours bar.
        
        This is the leftmost bar in the node. It shows how many hours
        the node has worked today.

        """
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

    def _get_io_load_indicator(self):
        """Draw the load indicator.
        
        Load indicator is drawn on the background of the main square.
        It shows how many tasks the node has in its task slots.

        Todo:
            implement this method properly. Currently it is only static.
        """
        return [
            pyglet.shapes.Rectangle(
                x=self.x + self._left_pad + 4,
                y=self.y + 4,
                width=self._square_size - 8,
                height=(self._square_size - 8) // 2,
                color=(64, 64, 64, 128),
                batch=self.batch),
        ]

    def _get_task_progress_bar(self, task: Task) -> None:
        """Draw the task progress bar.

        This is the bar on the bottom above the Task View
        that shows how much progress the current task
        has made.

        Args:
            task (Task): Task to draw the progress bar for.

        """
        x = self.x + self._left_pad
        y = self.y - 7
        return [
            pyglet.shapes.BorderedRectangle(
                x=x, y=y,
                width=self._square_size, height=5,
                border=1,
                color=self._background_color,
                border_color=self.color, batch=self.batch),
            pyglet.shapes.Rectangle(
                x=x + 1, y=self.y - 2,
                width=(self._square_size - 2) * task.progress,
                height=3,
                color=task.type.color,
                batch=self.batch)
            
        ]

    def draw(self):
        """Draw the node."""
        shapes = []
        shapes += self._get_main_square()
        shapes += self._get_work_hours_bar()
        shapes += self._get_task_progress_bar(self._current_task)
        shapes += self.get_task_view(offset_x=self._left_pad, offset_y=-14, max_length=self.x + self._square_size + 7)

        for shape in shapes:
            shape.draw()

    def update(self, delta_time: float):
        """Update the node.

        Args:
            delta_time (float): Time since last update.

        """
        self.current_hour += delta_time
        if self.current_hour >= self.work_hours:
            self.current_hour = 0
            self.state = 0
            self.color = (128, 200, 128, 255)
        for connection in self.connections:
            connection.update(delta_time)

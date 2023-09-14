"""Base for all nodes/actors in the game."""
import pyglet
from pipeliner.constants import TASK_SIZE, TASK_PADDING
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass


@dataclass
class Bounds:
    """Bounds of a rectangle.
    
    It includes drawing methods for debugging.
    """
    x1: int
    y1: int
    x2: int
    y2: int

    def get_shapes(self, color: tuple, batch: pyglet.graphics.Batch) -> List:
        """Get bounds shapes as lines.
        
        This is used for debugging purposes to draw the bounds.

        Args:
            color (tuple): Color of the bounds.
            batch (pyglet.graphics.Batch): Batch to add the shapes to.

        Returns:
            List: List of shapes.

        """
        return [
            pyglet.shapes.Line(x=self.x1, y=self.y1, x2=self.x1, y2=self.y2, color=color, batch=batch),
            pyglet.shapes.Line(x=self.x1, y=self.y2, x2=self.x2, y2=self.y2, color=color, batch=batch),
            pyglet.shapes.Line(x=self.x2, y=self.y2, x2=self.x2, y2=self.y1, color=color, batch=batch),
            pyglet.shapes.Line(x=self.x2, y=self.y1, x2=self.x1, y2=self.y1, color=color, batch=batch),
        ]

    def draw(self, color: tuple, batch: pyglet.graphics.Batch) -> None:
        for shape in self.get_shapes(color, batch):
            shape.draw()


@dataclass
class Point:
    x: int
    y: int


class Node(ABC):
    """Base class for all nodes/actors in the game.
    
    Properties:
        
        x (int): X position of the node.
        y (int): Y position of the node.
        color (tuple): Color of the node.
        
        connections (List[Connection]): List of connections to other nodes.
        accept_types (Set): Set of task types that the node accepts.
        provide_types (Set): Set of task types that the node provides.

        level (int): Level of the node.
        production_rate (float): How many tasks the node produces per hour.
        work_hours (int): How many hours the node works per day.
        current_hour (int): Current hour in the working day of the node.

        _in_port_position_bound (Optional[Bounds]): Bounds of the in port position.
        _out_port_position_bound (Optional[Bounds]): Bounds of the out port position.
        _in_port_position (Point): Position of the in port.
        _out_port_position (Point): Position of the out port.
        
        _batch (pyglet.graphics.Batch): Batch to add the shapes to.

    """
    x: int
    y: int
    color: tuple

    connections: List
    accept_types: Set
    provide_types: Set
    
    level: int
    production_rate: float
    work_hours: int
    current_hour: int
    
    _in_port_position_bound: Optional[Bounds]
    _out_port_position_bound: Optional[Bounds]
    _in_port_position: Point
    _out_port_position: Point

    _batch: pyglet.graphics.Batch

    def __init__(self,
                 batch: pyglet.graphics.Batch,
                 level: int = 1,
                 x: int = 0,
                 y: int = 0):
        self.level = level
        self.batch = batch
        self.x = x
        self.y = y
        self.connections = []
        self.production_rate = 1.0
        self.work_hours = 8
        self._tasks = []
        self.task_slots = 2
        self.current_hour = 0
        self.current_task = None
        self.in_port_position_bound = None
        self.out_port_position_bound = None

    @abstractmethod
    def update(self, delta_time: float):
        """Update the node."""
        for connection in self.connections:
            connection.update(delta_time)

    @abstractmethod
    def get_bounds(self) -> Bounds:
        """Get bounds of the node.
        
        Returns:
            Bounds: Bounds of the node.
        
        """
        pass

    def add_task(self, task) -> bool:
        """Add task to the node.
        
        Add task if there is space for it and if the task
        type is accepted by the node.

        Args:
            task (Task): Task to add.

        Returns:
            bool: True if task was added, False otherwise.
        
        """
        if len(self._tasks) >= self.task_slots:
            return False
        if not isinstance(task.type, (*self.accept_types,)):
            return False
        self._tasks.append(task)
        return True
    
    def add_tasks(self, tasks: List) -> List[bool]:
        """Add multiple tasks to the node.
        
        Args:
            tasks (List): List of tasks to add.

        Returns:
            List[bool]: List of booleans indicating if the task was added.

        """
        results = []
        for t in tasks:
            results.append(self.add_task(t))

        return results

    def get_task_view(
            self,
            offset_x: int = 0,
            offset_y: int = 0,
            max_length: int = 64) -> List[pyglet.shapes.ShapeBase]:
        """Get shapes for the node's task view.
        
        Task view is a visual representation of the tasks and their
        state associated with the node. Task shapes are drawn in a grid
        with a maximum length of max_length.

        Args:
            offset_x (int, optional): X offset of the task view. Defaults to 0.
            offset_y (int, optional): Y offset of the task view. Defaults to 0.
            max_length (int, optional): Maximum length of the task view. Defaults to 64.

        Returns:
            List: List of shapes.

        """
        x = self.x + offset_x
        y = self.y + offset_y
        shapes = []

        shape_x = x
        shape_y = y
    
        for i, task in enumerate(self._tasks):
            if i > self.task_slots:
                break
            shapes += task.get_shapes(shape_x, shape_y)
            shape_x += TASK_SIZE + TASK_PADDING
            if shape_x > max_length:
                shape_x = x
                shape_y -= TASK_SIZE + TASK_PADDING

        if len(self._tasks) < self.task_slots:
            for i in range(self.task_slots - len(self._tasks)):
                shapes += [
                    pyglet.shapes.BorderedRectangle(
                        x=shape_x, y=shape_y,
                        width=TASK_SIZE, height=TASK_SIZE,
                        border=1,
                        color=(0, 0, 0, 255),
                        border_color=(128, 128, 128, 255),
                        batch=self.batch)
                    ]
                shape_x += TASK_SIZE + TASK_PADDING
                if shape_x > max_length:
                    shape_x = x
                    shape_y -= TASK_SIZE + TASK_PADDING
        return shapes

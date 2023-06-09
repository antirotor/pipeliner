import pyglet
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Bounds:
    x1: int
    y1: int
    x2: int
    y2: int

    def get_shapes(self, color: tuple, batch: pyglet.graphics.Batch) -> List:
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
    level: int
    batch: pyglet.graphics.Batch
    x: int
    y: int
    state: int
    connections: List
    production_rate: float
    work_hours: int
    current_hour: int
    tasks_in: List
    tasks_out: List
    color: tuple
    in_port_position_bound: Optional[Bounds]
    out_port_position_bound: Optional[Bounds]
    in_port_position: Point
    out_port_position: Point

    def __init__(self,
                 batch: pyglet.graphics.Batch,
                 level: int = 1,
                 x: int = 0,
                 y: int = 0,
                 state: int = 0):
        self.level = level
        self.batch = batch
        self.x = x
        self.y = y
        self.state = state
        self.connections = []
        self.production_rate = 1.0
        self.work_hours = 8
        self.tasks = []
        self.current_hour = 0
        self.in_port_position_bound = None
        self.out_port_position_bound = None

    @abstractmethod
    def update(self, delta_time: float):
        for connection in self.connections:
            connection.update(delta_time)

    @abstractmethod
    def get_bounds(self) -> Bounds:
        pass

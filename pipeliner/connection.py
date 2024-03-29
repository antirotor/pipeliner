"""Class for connection between two nodes"""
from pipeliner.actors import Node
from pyglet.shapes import Line, Triangle, ShapeBase
import math
from typing import List


class Connection(object):
    source: Node
    target: Node

    def __init__(self, source: Node, target: Node, batch=None):
        self.source = source
        self.target = target
        self.batch = batch
        self._shapes = []

        line = Line(
            source.out_port_position.x, source.out_port_position.y,
            target.in_port_position.x, target.in_port_position.y,
            2, color=(50, 225, 30), batch=batch
        )

        self._shapes.append(line)

    def __repr__(self):
        return f"Connection: {self.source} -> {self.target}"

    def __str__(self):
        return f"Connection: {self.source} -> {self.target}"

    def draw(self):
        try:
            for shape in self._shapes:
                shape.draw()
        except AttributeError as e:
            print(self._shapes)
            raise e

    def update(self, delta_time: float):
        self._shapes = self.get_arrow(
                self.source.out_port_position.x, self.source.out_port_position.y,
                self.target.in_port_position.x, self.target.in_port_position.y,
                color=(50, 225, 30))

    def get_arrow(self, x1: int, y1: int, x2: int, y2: int, color) -> List[ShapeBase]:
        """Get shapes for end pointing arrow.
        
        Args:
            x1 (int): x coordinate of start point
            y1 (int): y coordinate of start point
            x2 (int): x coordinate of end point
            y2 (int): y coordinate of end point
            color (tuple): color of arrow

        Returns:
            List[ShapeBase]: list of shapes for arrow

        """
        arrow_size=10

        # calculate angle between line and x-axis
        angle = math.atan2(y2 - y1, x2 - x1)

        # calculate arrow points
        arrow_x1 = x2 - arrow_size * math.cos(angle - math.pi/6)
        arrow_y1 = y2 - arrow_size * math.sin(angle - math.pi/6)
        arrow_x2 = x2 - arrow_size * math.cos(angle + math.pi/6)
        arrow_y2 = y2 - arrow_size * math.sin(angle + math.pi/6)
        
        return [
            Line(x=x1, y=y1, x2=x2, y2=y2, color=color, batch=self.batch),
            # draw arrow head
            Triangle(arrow_x1, arrow_y1, x2, y2, arrow_x2, arrow_y2, color=color, batch=self.batch),
        ]
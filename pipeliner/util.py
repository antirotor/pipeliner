from abc import ABC

import pyglet.shapes
from pyglet.graphics import Batch
from pyglet.shapes import Circle, Polygon
from pyglet.text import Label
from typing import List, Tuple, Optional
from pipeliner.actors.node import Bounds, Point


def get_in_connection(
        position: Tuple, batch: Batch,
        bounds: Optional[Bounds] = None) -> List:
    shapes = [
        Circle(
            x=position[0], y=position[1],
            radius=2, color=(255, 255, 255), batch=batch),
        Label(x=position[0] - 5, y=position[1] - 15, text="IN", batch=batch, font_size=8),
    ]
    if bounds:
        bounds.x1 = position[0] - 5
        bounds.y1 = position[1] - 15
        bounds.x2 = position[0] + 15
        bounds.y2 = position[1] + 5
        # shapes += bounds.get_shapes((255, 0, 0), batch)
    return shapes


def get_out_connection(position: Tuple, batch: Batch,
                       bounds: Optional[Bounds] = None) -> List:
    shapes = [
        Circle(
            x=position[0], y=position[1],
            radius=2, color=(255, 255, 255), batch=batch),
        Label(x=position[0] - 8, y=position[1] - 15, text="OUT", batch=batch, font_size=8)
    ]
    if bounds:
        bounds.x1 = position[0] - 8
        bounds.y1 = position[1] - 15
        bounds.x2 = position[0] + 15
        bounds.y2 = position[1] + 5
        # shapes += bounds.get_shapes((255, 0, 0), batch)
    return shapes


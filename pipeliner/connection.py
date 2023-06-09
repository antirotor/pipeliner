from pypeliner.actors import Node
from pyglet.shapes import Line


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
        """
        self._shapes = [
            Line(self.source.out_port_position.x, self.source.out_port_position.y,
                 self.target.in_port_position.x, self.target.in_port_position.y,
                 2, color=(50, 225, 30), batch=self.batch)
        ]
        """

        self._shapes = self.get_arrow(
                self.source.out_port_position.x, self.source.out_port_position.y,
                self.target.in_port_position.x, self.target.in_port_position.y,
                color=(50, 225, 30))


    def get_arrow(self, x1: int, y1: int, x2: int, y2: int, color):
        return [
            Line(x=x1, y=y1, x2=x2, y2=y2, color=color, batch=self.batch),
            # draw arrow head
            Line(x=x2, y=y2, x2=x2 - 5, y2=y2 - 5, color=color, batch=self.batch),
            Line(x=x2, y=y2, x2=x2 - 5, y2=y2 + 5, color=color, batch=self.batch),
        ]
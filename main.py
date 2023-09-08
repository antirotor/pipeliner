#!/usr/bin/env bash
# -*- coding: utf-8 -*-
import itertools
from typing import Optional

import pyglet
from pipeliner.actors.node import Node
from pyglet.window import key
from pipeliner.actors import Artist
from pipeliner.connection import Connection
from pipeliner.tasks import (
    EmptyTask,
    CompositingTask
)


window = pyglet.window.Window(1024, 640)
main_batch = pyglet.graphics.Batch()

class ControlState(object):
    allow_drag: bool
    drag_on_actor: bool
    drag_on_connection: bool
    start_actor: Optional[Node]
    end_actor: Optional[Node]
    active_actor: Optional[Node]

    def __init__(self):
        self.allow_drag = False
        self.drag_on_actor = False
        self.drag_on_connection = False
        self.start_actor = None
        self.end_actor = None
        self.active_actor = None

control_state = ControlState()

actors = [
    Artist(main_batch, x=32, y=64),
    Artist(main_batch, x=128, y=128)
]

actors[0].task_slots = 10
actors[0].add_tasks([EmptyTask(main_batch, assignee=actors[0]) for _ in range(5)])
actors[0].add_task(CompositingTask(main_batch, assignee=actors[0]))

score_label = pyglet.text.Label(text="Score: 0", x=10, y=window.height - 20)


@window.event
def on_draw():
    window.clear()
    main_batch.draw()
    for actor in actors:
        actor.draw()
        for connection in actor.connections:
            connection.draw()
    score_label.draw()

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    actor: Node
    if control_state.active_actor:
        control_state.active_actor.x += dx
        control_state.active_actor.y += dy
        return   None
    for actor in actors:
        bounds = actor.get_bounds()
        if bounds.x1 < x < bounds.x2 and bounds.y1 < y < bounds.y2 and control_state.allow_drag:
            control_state.drag_on_actor = True
            control_state.start_actor = actor
            actor.x += dx
            actor.y += dy

@window.event
def on_mouse_press(x, y, button, modifiers):
    actor: Node
    for actor in actors:
        bounds = actor.get_bounds()
        if bounds.x1 < x < bounds.x2 and bounds.y1 < y < bounds.y2:
            control_state.allow_drag = True
            control_state.start_actor = actor
            control_state.active_actor = actor
        if actor.out_port_position_bound and (actor.out_port_position_bound.x1 < x < actor.out_port_position_bound.x2 and actor.out_port_position_bound.y1 < y < actor.out_port_position_bound.y2):
            control_state.drag_on_connection = True
            control_state.start_actor = actor


@window.event
def on_mouse_release(x, y, button, modifiers):
    actor: Node
    control_state.active_actor = None
    for actor in actors:
        bounds = actor.get_bounds()
        if bounds.x1 < x < bounds.x2 and bounds.x1 < y < bounds.x2 and control_state.allow_drag:
            control_state.allow_drag = False
            if control_state.drag_on_actor:
                control_state.drag_on_actor = False
            control_state.end_actor = actor
        if actor.in_port_position_bound.x1 < x < actor.in_port_position_bound.x2 and actor.in_port_position_bound.y1 < y < actor.in_port_position_bound.y2 and control_state.drag_on_connection:
            control_state.drag_on_connection = False
            control_state.end_actor = actor
            if control_state.start_actor != control_state.end_actor:
                print(f"Connect {control_state.start_actor} to {control_state.end_actor}")
                control_state.start_actor.connections.append(Connection(control_state.start_actor, control_state.end_actor, main_batch))
            else:
                print(
                    f"Cannot connect {control_state.start_actor} to {control_state.end_actor}"
                )


def update(date_time: float):
    # Check for keyboard input
    for actor in actors:
        actor.update(date_time)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 0.1)
    pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)
    pyglet.app.run()



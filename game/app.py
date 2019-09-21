import os
from random import randint
import pyglet
from game import config
from game.system.component import Component
from game.entities.runner import Runner
 
window = pyglet.window.Window(height=config.WINDOW_HEIGHT,
                              width=config.WINDOW_WIDTH)

pyglet.resource.path = [config.ASSETS_DIR]
pyglet.resource.reindex()

fps_display = pyglet.window.FPSDisplay(window=window)

objects = []
MAIN_BATCH = pyglet.graphics.Batch()
player = Runner(x=window.width // 2, y=window.height // 2, speed=randint(3, 12), batch=MAIN_BATCH)
 
def update(dt):
    """
    Updates our list of ball objects
    :param time:
    :return:
    """
    for ball in objects:
        if isinstance(ball, Component):
            ball.update(dt)
 
@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    MAIN_BATCH.draw()

 
@window.event
def on_key_press(symbol, modifiers):
    """
    On each mouse click, we create a new ball object
    """
    player.on_key_press(symbol, modifiers)

@window.event
def on_key_release(symbol, modifiers):
    player.on_key_release(symbol, modifiers)
 
def main():
    """
    This is the main method. This contains an embedded method
    :return:
    """

    pyglet.clock.schedule_interval(update, 1/120.0)
    objects.append(player)    
    pyglet.app.run()

import os
import math
import pyglet
from pyglet.window import key
from game import config
from game.system.component import Component


class Runner(Component):

    def __init__(self, *args, **kwargs):
        """
        Creates a sprite using a ball image.
        """
        super(Runner, self).__init__(*args, **kwargs)
        self.speed = kwargs.get('speed', 0)
        self.image = pyglet.resource.image('runner.png')
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2
        self.width = self.image.width
        self.height = self.image.height
        self.sprite = pyglet.sprite.Sprite(self.image, self.x, self.y, batch=kwargs.get('batch', None))
        self.rotation = 0
        self.impulse = 200
        self.drag = 0.005
        self.rotate_speed = 200
        self.keys = dict(left=False, right=False, up=False, down=False)

    def update(self, dt):
        """
        Increments x and y value and updates position.
        Also ensures that the ball does not leave the screen area by changing its axis direction
        :return:
        """
        a_x = 0
        a_y = 0

        # turning
        if self.keys['left']:
            self.rotation -= self.rotate_speed * dt
        if self.keys['right']:
            self.rotation += self.rotate_speed * dt


        if self.keys['up']:
            angle_radians = - math.radians(self.rotation)
            a_x = math.cos(angle_radians) * self.impulse
            a_y = math.sin(angle_radians) * self.impulse


        if self.keys['down']:
            angle_radians = - math.radians(self.rotation)
            a_x = math.cos(angle_radians) * - self.impulse
            a_y = math.sin(angle_radians) * - self.impulse

        # christmas wrapping
        if self.x - self.width // 2 < 0 or (self.x + self.width // 2) > config.WINDOW_WIDTH:
            self.v_x *= -1

        if self.y - self.width // 2 < 0 or (self.y + self.width // 2) > config.WINDOW_HEIGHT:
            self.v_y *= -1

        self.v_x += a_x * dt - self.drag * self.v_x
        self.v_y += a_y * dt - self.drag * self.v_y
        self.x += self.v_x * dt
        self.y += self.v_y * dt

        self.sprite.update(self.x, self.y, rotation=self.rotation)

    def draw(self):
        """
        Draws our ball sprite to screen
        :return:
        """
        print(self)
        self.sprite.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys['up'] = True
        elif symbol == key.LEFT:
            self.keys['left'] = True
        elif symbol == key.RIGHT:
            self.keys['right'] = True
        elif symbol == key.DOWN:
            self.keys['down'] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys['up'] = False
        elif symbol == key.LEFT:
            self.keys['left'] = False
        elif symbol == key.RIGHT:
            self.keys['right'] = False
        elif symbol == key.DOWN:
            self.keys['down'] = False

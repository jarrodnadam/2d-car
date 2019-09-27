import abc
import pyglet
from math import atan2, degrees, sqrt, sin, cos, radians
import numpy as np
from game import config

class Component(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        """
        Constructs Component object given passed kwargs.
        
        :param active Defines if the object has to update
        :param render Defines if the object has to render
        :param x Defines the x location of the object
        :param y Defines the y location of the object
        :param width Defines the width of the object
        :param height Defines the height of the object
        """

        # Basic stuff
        
        self.image = pyglet.resource.image(kwargs.get('image_name', 'dvd.png'))
        self.image.anchor_x = self.image.width / 2
        self.image.anchor_y = self.image.height / 2
        self.width = self.image.width
        self.height = self.image.height
        self.active = kwargs.get('active', True)
        self.render = kwargs.get('render', True)
        self.debug = kwargs.get('debug', False)
        self.position = np.array([kwargs.get('x', 0.0), kwargs.get('y', 0.0)], dtype='float64')
        self.sprite = pyglet.sprite.Sprite(self.image,
                                    self.position[0],
                                    self.position[1],
                                    batch=kwargs.get('batch', None))
        self.velocity = np.zeros(2, dtype='float64')
        self.acceleration = np.zeros(2, dtype='float64')
        self.rotation = 0.0
        self.impulse = 0.0
        self.drag = 0.005

    def get_speed(self):
        return sqrt(self.velocity[0]**2 + self.velocity[1]**2)

    def update(self, dt):
        # christmas wrapping
        if self.position[0] - self.width // 2 < 0 or (self.position[0] + self.width // 2) > config.WINDOW_WIDTH:
            self.velocity[0] *= -1

        if self.position[1]  - self.width // 2 < 0 or (self.position[1] + self.width // 2) > config.WINDOW_HEIGHT:
            self.velocity[1] *= -1

        self.velocity += self.acceleration * dt - self.drag * self.velocity
        self.position += self.velocity * dt
        self.sprite.update(x=self.position[0], y=self.position[1], rotation=self.rotation + 90)
        self.acceleration[0], self.acceleration[1] = 0, 0


    @abc.abstractmethod
    def draw(self):
        pass

    def __str__(self):
        return f'position: {self.position}, velocity: {self.velocity}' 
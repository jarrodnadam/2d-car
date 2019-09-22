import abc
from math import atan2, degrees, sqrt, sin, cos, radians
import numpy as np

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
        self.active = kwargs.get('active', True)
        self.render = kwargs.get('render', True)
        self.debug = kwargs.get('debug', False)
        self.position = np.array([kwargs.get('x', 0.0), kwargs.get('y', 0.0)], dtype='float64')
        self.width = kwargs.get('width', 0)
        self.height = kwargs.get('height', 0)
        self.velocity = np.zeros(2, dtype='float64')
        self.acceleration = np.zeros(2, dtype='float64')
        self.rotation = 0.0
        self.impulse = 0.0
        self.drag = 0.005

    def get_speed(self):
        return sqrt(self.velocity[0]**2 + self.velocity[1]**2)

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def draw(self):
        pass

    def __str__(self):
        return f'position: {self.position}, velocity: {self.velocity}' 
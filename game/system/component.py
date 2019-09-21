import abc


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
        self.x = kwargs.get('x', 0.0)
        self.y = kwargs.get('y', 0.0)
        self.v_x = kwargs.get('v_x', 0.0)
        self.v_y = kwargs.get('v_y', 0.0)
        self.impulse = kwargs.get('impulse', 0.0)
        self.rotation = kwargs.get('rotation', 0.0)
        self.rotate_speed = kwargs.get('rotate_speed', 0.0)
        self.width = kwargs.get('width', 0)
        self.height = kwargs.get('height', 0)

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def draw(self):
        pass

    def __str__(self):
        return f'x: {self.x}, y: {self.y}, v_x: {self.v_x}, v_y: {self.v_y}' 
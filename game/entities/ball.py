import pyglet
import os
from game import config
from game.system.component import Component


class Ball(Component):

    def __init__(self, *args, **kwargs):
        """
        Creates a sprite using a ball image.
        """
        super(Ball, self).__init__(*args, **kwargs)
        self.speed = kwargs.get('speed', 5)
        self.ball_image = pyglet.image.load(os.path.join(config.ASSETS, 'ball.png'))
        self.width = self.ball_image.width
        self.height = self.ball_image.height
        self.ball_sprite = pyglet.sprite.Sprite(self.ball_image, self.x, self.y)
        self.x_direction = 1
        self.y_direction = 1

        print('Ball Created')

    def update(self):
        """
        Increments x and y value and updates position.
        Also ensures that the ball does not leave the screen area by changing its axis direction
        :return:
        """
        self.x += (self.speed * self.x_direction)
        self.y += (self.speed * self.y_direction)
        self.ball_sprite.update(self.x, self.y)

        if self.x < 0 or (self.x + self.width) > config.WINDOW_WIDTH:
            self.x_direction *= -1

        if self.y < 0 or (self.y + self.height) > config.WINDOW_HEIGHT:
            self.y_direction *= -1

    def draw(self):
        """
        Draws our ball sprite to screen
        :return:
        """
        self.ball_sprite.draw()
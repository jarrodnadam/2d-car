import os
import math
import numpy as np
import pyglet
from pyglet.window import key
from game import config
from game.system.component import Component

debug = False 

class Car(Component):
    
    def __init__(self, *args, **kwargs):
        """
        Creates a sprite using a ball image.
        """
        super().__init__(*args, image_name='car.png', **kwargs)
        self.image = pyglet.resource.image('car.png')
        self.wheel_base = self.image.height
        self.steering_angle = 0.0
        self.max_steering = 30
        self.front_wheel = 0
        self.back_wheel = 0
        self.rotation = 0
        self.max_impulse = 200
        self.drag = 0.005
        self.rotate_speed = 180
        self.keys = dict(left=False, right=False, up=False, down=False)
        self.frame_count = 0

        if debug:
            wheel_image = pyglet.resource.image('ball.png')
            wheel_image.anchor_x = wheel_image.width / 2
            wheel_image.anchor_y = wheel_image.height / 2
            self.front_wheel_sprite = pyglet.sprite.Sprite(wheel_image, x=0, y=1, batch=kwargs.get('batch', None))
            self.front_wheel_sprite.color = 255, 0, 0
            self.centre_sprite = pyglet.sprite.Sprite(wheel_image, x=0, y=1, batch=kwargs.get('batch', None))
            self.centre_sprite.color = 0, 255, 0
            self.back_wheel_sprite = pyglet.sprite.Sprite(wheel_image, x=0, y=1, batch=kwargs.get('batch', None))


    def update(self, dt):
        """
        Increments x and y value and updates position.
        Also ensures that the ball does not leave the screen area by changing its axis direction
        :return:
        """
        # turning
        if self.keys['left']:
            self.steering_angle = + self.max_steering
        elif self.keys['right']:
            self.steering_angle = - self.max_steering
        else:
            self.steering_angle = 0

        if self.keys['up']:
            self.impulse = self.max_impulse
        elif self.keys['down']:
            self.impulse = - self.max_impulse / 2
        else:
            self.impulse = 0.0

        if self.position[0] - self.width // 2 < 0 or (self.position[0] + self.width // 2) > config.WINDOW_WIDTH:
            self.velocity[0] *= -1

        if self.position[1]  - self.width // 2 < 0 or (self.position[1] + self.width // 2) > config.WINDOW_HEIGHT:
            self.velocity[1] *= -1

        self.acceleration = self.impulse * get_heading(self.rotation)
        self.velocity += self.acceleration * dt - self.drag * self.velocity

        speed = np.copysign(self.get_speed(), np.dot(self.velocity, get_heading(self.rotation)))

        # position of wheels
        self.front_wheel = self.position + (self.wheel_base / 2) * get_heading(self.rotation)
        self.back_wheel = self.position - (self.wheel_base / 2) * get_heading(self.rotation)
        
        # update wheel position
        # TODO rotation velocity by self.steering_angle
        front_wheel_delta = speed * get_heading(self.rotation + self.steering_angle) * dt 
        back_wheel_delta = speed * get_heading(self.rotation) * dt

        self.front_wheel += front_wheel_delta
        self.back_wheel += back_wheel_delta


        # Update sprite positon and heading
        self.position = (self.front_wheel + self.back_wheel) / 2
        self.rotation = rotation_angle(self.front_wheel - self.back_wheel)
        self.bearing = - self.rotation + 90
        self.sprite.update(x=self.position[0], y=self.position[1], rotation=self.bearing)
        if debug:
            self.centre_sprite.update(x=self.position[0], y=self.position[1], rotation=self.bearing)
            self.front_wheel_sprite.update(x=self.front_wheel[0], 
                                        y=self.front_wheel[1], 
                                        rotation= - rotation_angle(front_wheel_delta)  + 90)
            self.back_wheel_sprite.update(x=self.back_wheel[0], 
                                        y=self.back_wheel[1], 
                                        rotation= - rotation_angle(back_wheel_delta) + 90)


        self.frame_count += 1

  
    def draw(self):
        """
        Draws our ball sprite to screen
        :return:
        """
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

    def get_new_rotation(self):
        return math.degrees(math.atan2(self.front_wheel[1] - self.back_wheel[1], self.front_wheel[0] - self.back_wheel[0]))

def rotation_angle(vector):
    return math.degrees(math.atan2(vector[1], vector[0]))


def get_heading(rotation):
    return np.array([math.cos(math.radians(rotation)), math.sin(math.radians(rotation))], dtype='float64')

def get_bearing(vector):
    return math.acos(vector[1])


def rotate_vector(vector, rotation=0):
    rads = math.radians(rotation)
    x = vector[0]
    y = vector[1]
    new_vector = np.array([x * math.cos(rads) - y * math.sin(rads), x * math.sin(rads) + y * math.cos(rads)])
    return new_vector
import pygame
import pymunk
from pymunk import Vec2d
import random

from settings import *

# class Ball(pygame.sprite.Sprite):
#
#     def __init__(self):
#         super(Ball, self).__init__()
#
#         self.image = pygame.image.load('assets/ball2.png')
#         self.rect = self.image.get_rect()
#
#         self.rect.x = WIDTH / 2
#         self.rect.y = 75
#         self.current_speed = 0

    # def update(self):
    #     # scale = abs((self.rect.y - y) / -2)
    #     # self.width = self.height = abs(int(self.width - scale))
    #     # print('scale = {}, w = {}, h = {}'.format(scale, self.width, self.height))
    #     # self.image = pygame.transform.scale(self.image, (self.width, self.height))
    #     self.current_speed = -self.max_speed

class Ball2():
    def __init__(self, distance, angle, x, y, space):
        mass = 5
        radius = 12
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = x, y
        power = distance * 53
        impulse = power * Vec2d(1, 0)
        angle = -angle
        body.apply_impulse_at_local_point(impulse.rotated(angle))
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 0
        space.add(body, shape)
        self.body = body
        self.shape = shape

class Ball():
    def __init__(self, space, x):
        mass = 10
        radius = 20
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = x, 400
        # power = distance * 53
        # impulse = power * Vec2d(1, 0)
        # body.apply_impulse_at_local_point(impulse.rotated(angle))
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        space.add(body, shape)
        self.body = body
        self.shape = shape
        self.ball_path = []
        self.path_color = (0, random.randint(200, 255), random.randint(200, 255))

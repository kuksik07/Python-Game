import pygame
import pymunk as pm
from pymunk import Vec2d
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

class Ball():
    def __init__(self, distance, angle, x, y, space):
        mass = 5
        radius = 12
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia)
        body.position = x, y
        power = distance * 53
        impulse = power * Vec2d(1, 0)
        angle = -angle
        body.apply_impulse_at_local_point(impulse.rotated(angle))
        shape = pm.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 0
        space.add(body, shape)
        self.body = body
        self.shape = shape


import pygame
import pymunk
from pymunk import Vec2d
import random


class Ball():
    def __init__(self, distance, angle, x, y, space):
        mass = 5
        radius = 15
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = x, y
        power = distance * 60
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
        self.ball_path = []
        self.path_color = (0, random.randint(200, 255), random.randint(200, 255))


class Polygon():
    def __init__(self, pos, size, space):
        mass = 5
        moment = pymunk.moment_for_box(mass, size)
        body = pymunk.Body(mass, moment)
        body.position = Vec2d(pos)
        shape = pymunk.Poly.create_box(body, size)
        shape.friction = 0.4
        shape.collision_type = 2
        space.add(body, shape)
        self.body = body
        self.shape = shape


import pygame
import pymunk
from pymunk import Vec2d
import random
import math


class Ball():
    def __init__(self, distance, angle, x, y, space):
        mass = 5
        radius = 15
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = x, y
        power = distance * 65
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


class Brick():
    def __init__(self, pos, space, size=(30, 30)):
        mass = 5
        moment = 1000
        body = pymunk.Body(mass, moment)
        body.position = Vec2d(pos)
        shape = pymunk.Poly.create_box(body, size)
        shape.friction = 0.5
        shape.collision_type = 1
        space.add(body, shape)
        self.body = body
        self.isBase = False
        self.shape = shape
        self.image = pygame.image.load("./assets/pictures/box.png")

    def to_pygame(self, p):
        return int(p.x), int(-p.y + 600)

    def draw_brick(self, screen):
        poly = self.shape
        p = poly.body.position
        p = Vec2d(self.to_pygame(p))
        angle_degrees = math.degrees(poly.body.angle) + 180
        rotated_logo_img = pygame.transform.rotate(self.image, angle_degrees)
        offset = Vec2d(rotated_logo_img.get_size()) / 2.
        p = p - (offset - (1, 52))
        np = p
        screen.blit(rotated_logo_img, (np.x, np.y))


class HorizontalBrick(Brick):
    def __init__(self, pos, space):
        Brick.__init__(self, pos, space, (90, 30))
        self.image = pygame.image.load("./assets/pictures/brick.png")


class VerticalBrick(Brick):
    def __init__(self, pos, space):
        Brick.__init__(self, pos, space, (30, 90))
        self.image = pygame.image.load("./assets/pictures/brick.png")
        self.image = pygame.transform.rotate(self.image, 90)

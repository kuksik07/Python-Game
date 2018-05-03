import pygame
import pymunk
from pymunk import Vec2d
import random
import math
from game_objects import Brick, HorizontalBrick, VerticalBrick


class Level():
    def __init__(self, bricks, space):
        self.bricks = bricks
        self.space = space
        self.number_of_balls = 5

    def level_0(self):
        """level 0"""
        x = 900
        while x <= 1100:
            self.bricks.append(VerticalBrick((x, 105), self.space))
            x += 60

        self.bricks.append(HorizontalBrick((945, 165), self.space))
        self.bricks.append(HorizontalBrick((1035, 165), self.space))

        self.bricks.append(VerticalBrick((930, 225), self.space))
        self.bricks.append(VerticalBrick((990, 225), self.space))
        self.bricks.append(VerticalBrick((1050, 225), self.space))

        self.bricks.append(HorizontalBrick((990, 285), self.space))

        self.bricks.append(Brick((990, 315), self.space))
        self.bricks.append(Brick((990, 345), self.space))


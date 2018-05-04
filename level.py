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
        self.number = 0
        self.number_of_balls = 5
        self.count_of_balls = self.count_of_balls(self.number_of_balls)

    def count_of_balls(self, count):
        return  count

    def build_level_0(self):
        """level 0"""
        # 1 block level
        x = 840
        y = 105
        for _ in range(2):
            brick = VerticalBrick((x, y), self.space)
            brick.isBase = True
            self.bricks.append(brick)
            x += 60
        x -= 30
        for _ in range(2):
            brick = VerticalBrick((x, y), self.space)
            brick.isBase = True
            self.bricks.append(brick)
            x += 60
        # 2 block level
        x = 870
        y += 60
        for _ in range(2):
            self.bricks.append(HorizontalBrick((x, y), self.space))
            x += 89
        # 3 block level
        x = 885
        y += 60
        for _ in range(2):
            self.bricks.append(VerticalBrick((x, y), self.space))
            x += 60
        # 4 block level
        x = 915
        y += 60
        self.bricks.append(HorizontalBrick((x, y), self.space))

        self.number_of_balls = 5

    def build_level_1(self):
        """level 1"""
        # 1 block level
        x = 840
        y = 75
        for _ in range(3):
            brick = Brick((x, y), self.space)
            brick.isBase = True
            self.bricks.append(brick)
            x += 60
        # 2 block level
        x = 840
        y += 29
        for _ in range(3):
            x = 840
            for _ in range(3):
                self.bricks.append(Brick((x, y), self.space))
                x += 60
            y += 29

        self.number_of_balls = 5

    def build_level_2(self):
        """level 2"""
        # 1 block level
        x = 840
        y = 105
        for _ in range(4):
            brick = VerticalBrick((x, y), self.space)
            brick.isBase = True
            self.bricks.append(brick)
            x += 60
        # 2 block level
        x = 840
        y += 89
        for i in range(3):
            x = 840
            x1 = 960
            for j in range(2):
                if i < 1:
                    self.bricks.append(VerticalBrick((x1, y), self.space))
                self.bricks.append(VerticalBrick((x, y), self.space))
                x += 60
                x1 += 60
            y += 90
        y -= 30
        self.bricks.append(HorizontalBrick((870, y), self.space))
        self.bricks.append(HorizontalBrick((990, 250), self.space))

        self.number_of_balls = 5

    def build_level_3(self):
        """level 3"""
        # 1 block level
        x = 840
        y = 105
        for _ in range(4):
            brick = VerticalBrick((x, y), self.space)
            brick.isBase = True
            self.bricks.append(brick)
            x += 60
        # other block levels
        x = 840
        y += 89
        for _ in range(1):
            x = 840
            for _ in range(4):
                self.bricks.append(VerticalBrick((x, y), self.space))
                x += 60
            y += 90
        y -= 30
        self.bricks.append(HorizontalBrick((870, 255), self.space))
        self.bricks.append(HorizontalBrick((990, 255), self.space))
        self.bricks.append(VerticalBrick((900, 315), self.space))
        self.bricks.append(VerticalBrick((960, 315), self.space))
        self.bricks.append(HorizontalBrick((930, 375), self.space))

        self.number_of_balls = 5

    def load_level(self):
        try:
            build_name = "build_level_"+str(self.number)
            getattr(self, build_name)()
        except AttributeError:
            self.number = 0
            build_name = "build_level_"+str(self.number)
            getattr(self, build_name)()

import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math, sys, random

from game_objects import Ball
from settings import *

mouse_pressed = False

pygame.init()

pygame.display.set_caption("My game!")

# space.add(body)

screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# Game objects
# ball = Ball()

def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+600

space = pymunk.Space()
space.gravity = (0.0, -700.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Static floor
static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
static_lines = [pymunk.Segment(static_body, (0.0, 060.0), (1200.0, 060.0), 0.0),
                pymunk.Segment(static_body, (1200.0, 060.0), (1200.0, 800.0), 0.0)]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3

space.add(static_lines)

ticks_to_next_ball = 10

ball_img = pygame.image.load('assets/ball2.png')
balls = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if ball_img.rect.collidepoint(event.pos):
        #         mouse_pressed = True
        #         mouse_x, mouse_y = event.pos
        #         offset_x = ball_img.rect.x - mouse_x
        #         offset_y = ball_img.rect.y - mouse_y
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     mouse_pressed = False
        # elif event.type == pygame.MOUSEMOTION:
        #     if mouse_pressed:
        #         mouse_x, mouse_y = event.pos
        #         ball_img.rect.x = mouse_x + offset_x
        #         ball_img.rect.y = mouse_y + offset_y

    ticks_to_next_ball -= 1
    if ticks_to_next_ball <= 0:
        ticks_to_next_ball = 100
        mass = 10
        radius = 20
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(115, 350)
        body.position = x, 400
        # power = distance * 53
        # impulse = power * Vec2d(1, 0)
        # body.apply_impulse_at_local_point(impulse.rotated(angle))
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        space.add(body, shape)
        balls.append(shape)

    ### Clear screen
    screen.fill(WHITE)

    ### Draw stuff
    balls_to_remove = []
    for ball in balls:
        if ball.body.position.y < 60:
            balls_to_remove.append(ball)
        # image draw
        p = ball.body.position
        p = Vec2d(p.x, flipy(p.y))

        # we need to rotate 180 degrees because of the y coordinate flip
        angle_degrees = math.degrees(ball.body.angle) + 180
        rotated_logo_img = pygame.transform.rotate(ball_img, angle_degrees)

        offset = Vec2d(rotated_logo_img.get_size()) / 2.
        p = p - offset + (0, 50)

        screen.blit(rotated_logo_img, p)

    for ball in balls_to_remove:
        space.remove(ball, ball.body)
        balls.remove(ball)

    # space.debug_draw(draw_options)

    ### Update physics
    dt = 1.0 / FPS
    for x in range(1):
        space.step(dt)

    ### Flip screen
    pygame.display.flip()
    clock.tick(FPS)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
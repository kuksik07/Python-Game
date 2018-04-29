import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math, sys, random, time
from game_objects import Ball
from settings import *

# Pygame
pygame.init()
pygame.display.set_caption("My game!")
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
mouse_pressed = False

# Sprites
ball_img = pygame.image.load('assets/ball4.png')
background = pygame.image.load('assets/bg2.png')

# Physics
space = pymunk.Space()
space.gravity = (0.0, -700.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)
ticks_to_next_ball = 10
balls = []
ball_path = []
counter = 0
count = 10
restart_counter = False

# Static floor
static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
static_lines = [pymunk.Segment(static_body, (0.0, 060.0), (1200.0, 060.0), 0.0),
                pymunk.Segment(static_body, (1200.0, 060.0), (1200.0, 800.0), 0.0)]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3

space.add(static_lines)


# Convert pymunk to pygame coordinates
def to_pygame(p):
    return int(p.x), int(-p.y+600)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if len(balls) < 5:
                ball = Ball(space, mouse_x)
                balls.append(ball)
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

    # Draw background
    screen.fill(WHITE)
    screen.blit(background, (-50, -50))

    # Draw stuff
    balls_to_remove = []

    # Trace from the ball
    counter += 1
    if restart_counter:
        counter = 0
        restart_counter = False

    for point in ball_path:
        pygame.draw.circle(screen, WHITE, point, 3, 0)

    for ball in balls:
        if ball.body.position.y < 60:
            balls_to_remove.append(ball)
        # image draw
        p = ball.body.position
        p = Vec2d(to_pygame(p))

        # Draw the trail
        if counter >= 4:
            ball_path.append(p + (0, 40))
            restart_counter = True
            if len(ball_path) >= 10:
                ball_path.pop(0)
                # del ball_path[:2]

        # We need to rotate 180 degrees because of the y coordinate flip
        angle_degrees = math.degrees(ball.body.angle) + 180
        rotated_logo_img = pygame.transform.rotate(ball_img, angle_degrees)
        offset = Vec2d(rotated_logo_img.get_size()) / 2.
        p = p - offset + (0, 50)

        # Draw sprite ball
        screen.blit(rotated_logo_img, p)

    for ball in balls_to_remove:
        space.remove(ball.shape, ball.shape.body)
        balls.remove(ball)

    # Update physics
    dt = 1.0 / FPS
    for x in range(1):
        space.step(dt)

    # Flip screen
    pygame.display.flip()
    clock.tick(FPS)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
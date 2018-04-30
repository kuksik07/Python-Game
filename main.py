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
background = pygame.image.load('assets/bg6.png')
sling_shot_back = pygame.image.load('assets/sling-shot-back.png')
sling_shot_front = pygame.image.load('assets/sling-shot-front.png')

# Physics
space = pymunk.Space()
space.gravity = (0.0, -700.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)
ticks_to_next_ball = 10
balls = []
rope_lenght = 80
x_mouse = 0
y_mouse = 0
sling_x, sling_y = 150, 390
sling2_x, sling2_y = 195, 396
counter = 0
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


def vector(p0, p1):
    """Return the vector of the points
    p0 = (xo,yo), p1 = (x1,y1)"""
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)


def unit_vector(v):
    """Return the unit vector of the points
    v = (a,b)"""
    h = ((v[0]**2)+(v[1]**2))**0.5
    if h == 0:
        h = 0.000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)


def distance(xo, yo, x, y):
    """distance between points"""
    dx = x - xo
    dy = y - yo
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d

def sling_action():
    """Set up sling behavior"""
    global mouse_distance
    global rope_lenght
    global angle
    global x_mouse
    global y_mouse
    # Fixing bird to the sling rope
    v = vector((sling_x, sling_y), (x_mouse, y_mouse))
    uv = unit_vector(v)
    uv1 = uv[0]
    uv2 = uv[1]
    mouse_distance = distance(sling_x, sling_y, x_mouse, y_mouse)
    pu = (uv1*rope_lenght+sling_x, uv2*rope_lenght+sling_y)
    bigger_rope = 102
    x_ball = x_mouse - 20
    y_ball = y_mouse - 20
    if mouse_distance > rope_lenght:
        pux, puy = pu
        pux -= 20
        puy -= 20
        pul = pux, puy
        pu2 = (uv1*bigger_rope+sling_x, uv2*bigger_rope+sling_y)
        pygame.draw.line(screen, (68, 36, 104), (sling2_x, sling2_y), pu2, 10)
        screen.blit(ball_img, pul)
        pygame.draw.line(screen, (68, 36, 104), (sling_x, sling_y), pu2, 10)
    else:
        mouse_distance += 10
        pu3 = (uv1*mouse_distance+sling_x, uv2*mouse_distance+sling_y)
        pygame.draw.line(screen, (68, 36, 104), (sling2_x, sling2_y), pu3, 10)
        screen.blit(ball_img, (x_ball, y_ball))
        pygame.draw.line(screen, (68, 36, 104), (sling_x, sling_y), pu3, 10)
    # Angle of impulse
    dy = y_mouse - sling_y
    dx = x_mouse - sling_x
    if dx == 0:
        dx = 0.00000000000001
    angle = math.atan((float(dy))/dx)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # if len(balls) < 5:
                # ball = Ball(space, mouse_x)
                # balls.append(ball)
        #     if ball_img.rect.collidepoint(event.pos):
            mouse_pressed = True
        #         mouse_x, mouse_y = event.pos
        #         offset_x = ball_img.rect.x - mouse_x
        #         offset_y = ball_img.rect.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP and mouse_pressed:
            # Release new ball
            mouse_pressed = False
            xo = 160
            yo = 250
            if mouse_distance > rope_lenght:
                mouse_distance = rope_lenght
            if x_mouse < sling_x+5:
                bird = Ball(mouse_distance, angle, xo, yo, space)
                balls.append(bird)
            else:
                bird = Ball(-mouse_distance, angle, xo, yo, space)
                balls.append(bird)

        # elif event.type == pygame.MOUSEBUTTONUP:
        #     mouse_pressed = False
        # elif event.type == pygame.MOUSEMOTION:
        #     if mouse_pressed:
        #         mouse_x, mouse_y = event.pos
        #         ball_img.rect.x = mouse_x + offset_x
        #         ball_img.rect.y = mouse_y + offset_y

    x_mouse, y_mouse = pygame.mouse.get_pos()

    # Draw background
    screen.fill(WHITE)
    screen.blit(background, (-50, -50))

    # Draw back side of the sling shot
    rect = pygame.Rect(50, 0, 70, 220)
    screen.blit(sling_shot_back, (140, 365))

    # Draw stuff
    balls_to_remove = []

    # Trace from the ball
    counter += 1
    if restart_counter:
        counter = 0
        restart_counter = False

    # Draw sling behavior
    if mouse_pressed:
        sling_action()

    for ball in balls:
        if ball.body.position.y < 60 or event.type == pygame.KEYUP:
            balls_to_remove.append(ball)

        p = ball.body.position
        p = Vec2d(to_pygame(p))

        # Draw the trail
        for point in ball.ball_path:
            pygame.draw.circle(screen, ball.path_color, point, 3, 0)

        # Add / Remove the trail
        if counter >= 4:
            ball.ball_path.append(p + (0, 50))
            restart_counter = True
            if len(ball.ball_path) >= 20:
                ball.ball_path.pop(0)

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

    # Draw back side of the sling shot
    rect = pygame.Rect(50, 0, 70, 220)
    screen.blit(sling_shot_front, (140, 365))

    # space.debug_draw(draw_options) # to display the physical representation

    # Update physics
    dt = 1.0 / FPS / 2.
    for x in range(2):
        space.step(dt)

    # Flip screen
    pygame.display.flip()
    clock.tick(FPS)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
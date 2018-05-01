import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import sys, random, time, math
from game_objects import Ball
from settings import *  # All sprites, colors, etc. - are there

# Pygame
pygame.init()
pygame.display.set_caption("My game!")
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
mouse_pressed = False

# Physics
space = pymunk.Space()
space.gravity = (0.0, -700.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)

balls = []
ticks_to_next_ball = 10
rope_lenght = 90
mouse_distance = 0
angle = 0
x_mouse = 0
y_mouse = 0
sling_x, sling_y = 150, 490
sling2_x, sling2_y = 170, 490
counter = 0
restart_counter = False
delete_all = False

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


# Return the vector of the points:
# p0 = (xo,yo), p1 = (x1,y1)
def vector(p0, p1):
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)


# Return the unit vector of the points
def unit_vector(v):
    # v = (a,b)
    h = ((v[0]**2)+(v[1]**2))**0.5
    if h == 0:
        h = 0.000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)


# distance between points
def distance(x0, y0, x, y):
    dx = x - x0
    dy = y - y0
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d


def sling_action():
    """Set up sling behavior"""
    global mouse_distance
    global rope_lenght
    global angle
    global x_mouse
    global y_mouse

    # Fixing ball to the sling rope
    v = vector((sling_x, sling_y), (x_mouse, y_mouse))
    uv = unit_vector(v)
    uv1 = uv[0]
    uv2 = uv[1]
    mouse_distance = distance(sling_x, sling_y, x_mouse, y_mouse)
    pu = (uv1*rope_lenght+sling_x, uv2*rope_lenght+sling_y)
    bigger_rope = 100
    x_ball = x_mouse - 15
    y_ball = y_mouse - 15
    if mouse_distance > rope_lenght:
        pux, puy = pu
        pux -= 15
        puy -= 15
        pul = pux, puy
        pu2 = (uv1*bigger_rope+sling_x, uv2*bigger_rope+sling_y)
        pygame.draw.line(screen, ROPE_BACK_COLOR, (sling2_x, sling2_y), pu2, 5)
        screen.blit(ball_img, pul)
        pygame.draw.line(screen, ROPE_FRONT_COLOR, (sling_x, sling_y), pu2, 5)
    else:
        mouse_distance += 10
        pu3 = (uv1*mouse_distance+sling_x, uv2*mouse_distance+sling_y)
        pygame.draw.line(screen, ROPE_BACK_COLOR, (sling2_x, sling2_y), pu3, 5)
        screen.blit(ball_img, (x_ball, y_ball))
        pygame.draw.line(screen, ROPE_FRONT_COLOR, (sling_x, sling_y), pu3, 5)

    # Angle of impulse
    dy = y_mouse - sling_y
    dx = x_mouse - sling_x
    if dx == 0:
        dx = 0.00000000000001
    angle = math.atan((float(dy))/dx)


while True:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and mouse_pressed:
            # Release new ball
            mouse_pressed = False
            x0 = 164
            y0 = 163
            if mouse_distance > rope_lenght:
                mouse_distance = rope_lenght
            if x_mouse < sling_x:
                ball = Ball(mouse_distance, angle, x0, y0, space)
                balls.append(ball)
            else:
                ball = Ball(-mouse_distance, angle, x0, y0, space)
                balls.append(ball)

        elif keys[pygame.K_UP]:
            delete_all = True

    # Get mouse position
    x_mouse, y_mouse = pygame.mouse.get_pos()

    # Draw background
    screen.fill(WHITE)
    screen.blit(background, (-50, -50))

    balls_to_remove = []

    # Draw back side of the sling shot
    screen.blit(sling_shot_back, (140, 470))

    # Trace from the ball
    counter += 1
    if restart_counter:
        counter = 0
        restart_counter = False

    # Draw sling behavior
    if mouse_pressed:
        sling_action()
    elif len(balls) == 0:
        pygame.draw.line(screen, ROPE_BACK_COLOR, (sling_x, sling_y + 2), (sling2_x, sling2_y), 5)

    for ball in balls:
        # Balls to remove
        if ball.body.position.y < 60 or delete_all:
            balls_to_remove.append(ball)

        # Position of the ball
        p = ball.body.position
        p = Vec2d(to_pygame(p))

        # Draw the trail
        for point in ball.ball_path:
            pygame.draw.circle(screen, ball.path_color, point, 3, 0)

        # Add / Remove the trail
        if counter >= 3:
            ball.ball_path.append(p + (0, 50))
            restart_counter = True
            if len(ball.ball_path) >= 20:
                ball.ball_path.pop(0)

        # Rotate of the ball image and set coordinates
        angle_degrees = math.degrees(ball.body.angle) + 180
        rotated_logo_img = pygame.transform.rotate(ball_img, angle_degrees)
        offset = Vec2d(rotated_logo_img.get_size()) / 2.
        p = p - offset + (0, 50)
        # Draw sprite ball
        screen.blit(rotated_logo_img, p)

    delete_all = False

    # Remove balls
    for ball in balls_to_remove:
        space.remove(ball.shape, ball.shape.body)
        balls.remove(ball)

    # Draw back side of the sling shot
    screen.blit(sling_shot_front, (140, 470))

    # space.debug_draw(draw_options) # to display the physical representation

    # Update physics
    dt = 1.0 / FPS / 2.
    for x in range(2):
        space.step(dt)

    # Flip screen
    pygame.display.flip()
    clock.tick(FPS)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
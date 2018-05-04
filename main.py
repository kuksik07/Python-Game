import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import sys, random, time, math
from game_objects import *
from level import *
from settings import *  # All sprites, colors, etc. - are there

# Pygame
pygame.init()
pygame.display.set_caption("Balls vs bricks")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

# Physics
space = pymunk.Space()
space.gravity = (0.0, -700.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)
# Update physics per second
dt = 1.0 / FPS / 2.
upd = dt

balls = []
bricks = []
ticks_to_next_ball = 10
rope_lenght = 90
mouse_distance = 0
angle = 0
x_mouse = 0
y_mouse = 0
sling_x, sling_y = 150, 490
sling2_x, sling2_y = 170, 490
counter = 0
score = 0
game_state = 0
effect_volume1 = 0.5
effect_volume2 = 0.2
music_volume = 0.5
restart_counter = False
mouse_pressed = False
audio = True
music = True
# Fonts
normal_font = pygame.font.SysFont("arial", 14, bold=False)
font = pygame.font.Font("assets/Chicle-Regular.ttf", 30)
font2 = pygame.font.Font("assets/Chicle-Regular.ttf", 42)

# Static floor
static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
static_lines = [pymunk.Segment(static_body, (0.0, 060.0), (1200.0, 060.0), 0.0),
                pymunk.Segment(static_body, (1200.0, 060.0), (1200.0, 800.0), 0.0)]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 2

space.add(static_lines)


def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)


def vector(p0, p1):
    """Return the vector of the points:
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


def distance(x0, y0, x, y):
    """Distance between points"""
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


def draw_level_failed():
    """Draw level failed"""
    global game_state
    failed_caption = font2.render("Level Failed", 1, WHITE)
    if level.number_of_balls <= 0 < len(bricks) and\
            time.time() - t1 > 5 and game_state != 1:
        game_state = 2
        screen.blit(failed_caption, (525, 200))
        screen.blit(repeat, (575, 300))


def draw_level_complete():
    """Draw level complete"""
    global game_state
    global score
    level_complete_caption = font2.render("Level Complete!", 1, WHITE)
    if level.number_of_balls >= 0 and len(bricks) == 0 and game_state != 1:
        game_state = 3
        screen.blit(level_complete_caption, (475, 200))
        screen.blit(repeat, (525, 300))
        screen.blit(resume, (625, 300))


def restart():
    """Delete all objects of the level"""
    balls_to_remove = []
    bricks_to_remove = []
    for ball in balls:
        balls_to_remove.append(ball)
    for ball in balls_to_remove:
        space.remove(ball.shape, ball.shape.body)
        balls.remove(ball)
    for brick in bricks:
        bricks_to_remove.append(brick)
    for brick in bricks_to_remove:
        space.remove(brick.shape, brick.shape.body)
        bricks.remove(brick)


def post_solve_ball_brick(arbiter, space, _):
    """Collision between ball and brick"""
    global score
    brick_to_remove = []
    if arbiter.total_impulse.length > 1200:
        a, b = arbiter.shapes
        for brick in bricks:
            if b == brick.shape:
                # Song
                brick_crashed_song = pygame.mixer.Sound(brick_crashed)
                brick_crashed_song.play()
                brick_crashed_song.set_volume(effect_volume1)
                brick_to_remove.append(brick)
                number_of_the_ball = level.count_of_balls - level.number_of_balls
                if number_of_the_ball > 0:
                    score += round(5000 / number_of_the_ball)

        for brick in brick_to_remove:
            bricks.remove(brick)

        space.remove(b, b.body)


def post_solve_brick_floor(arbiter, space, _):
    """Collision between ball and brick"""
    global score
    brick_to_remove = []
    a, b = arbiter.shapes
    for brick in bricks:
        if a == brick.shape and (not brick.isBase or
                                 (brick.isBase and math.fabs(round(math.degrees(brick.shape.body.angle)) == 90))):
            # Song
            brick_crashed_song = pygame.mixer.Sound(brick_crashed)
            brick_crashed_song.play()
            brick_crashed_song.set_volume(effect_volume1)

            brick_to_remove.append(brick)
            space.remove(a, a.body)
            number_of_the_ball = level.count_of_balls - level.number_of_balls
            if number_of_the_ball > 0:
                score += round(5000 / number_of_the_ball)
    for brick in brick_to_remove:
        bricks.remove(brick)


def post_solve_ball_floor(arbiter, space, _):
    """Collision between ball and floor"""
    if arbiter.total_impulse.length > 2000:
        a, b = arbiter.shapes
        for ball in balls:
            if a == ball.shape:
                # Song
                jump_song = pygame.mixer.Sound(jump)
                jump_song.play()
                jump_song.set_volume(effect_volume2)


# ball and brick collision
space.add_collision_handler(0, 1).post_solve = post_solve_ball_brick
# brick and static line collision
space.add_collision_handler(1, 2).post_solve = post_solve_brick_floor
# ball and brick collision
space.add_collision_handler(0, 2).post_solve = post_solve_ball_floor

# Song
pygame.mixer.music.load(bg_song)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(music_volume)

# Build the level
level = Level(bricks, space)
level.load_level()

while True:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1\
                and (x_mouse < 400 and y_mouse > 100) and game_state == 0:
            mouse_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and mouse_pressed:
            # Release new ball
            mouse_pressed = False
            if level.number_of_balls > 0:
                level.number_of_balls -= 1
                x0 = 164
                y0 = 163
                if mouse_distance > rope_lenght:
                    mouse_distance = rope_lenght
                # Song
                throw_song = pygame.mixer.Sound(throw)
                throw_song.play()
                throw_song.set_volume(effect_volume2)

                if x_mouse < sling_x:
                    ball = Ball(mouse_distance, angle, x0, y0, space)
                    balls.append(ball)
                else:
                    ball = Ball(-mouse_distance, angle, x0, y0, space)
                    balls.append(ball)
                if level.number_of_balls == 0:
                    t1 = time.time()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (10 <= x_mouse <= 60) and (10 <= y_mouse <= 60):
                # Pause button
                upd = 0
                game_state = 1
            if game_state == 0:
                # Play game
                upd = dt
            if game_state == 1:
                if (425 <= x_mouse <= 475) and (300 <= y_mouse <= 350):
                    # Resume button
                    upd = dt
                    game_state = 0
                if (525 <= x_mouse <= 575) and (300 <= y_mouse <= 350):
                    # Repeat button
                    restart()
                    level.load_level()
                    game_state = 0
                    score = 0
                if (625 <= x_mouse <= 675) and (300 <= y_mouse <= 350):
                    # Audio button
                    audio = not audio
                    if audio:
                        effect_volume1 = 0.2
                        effect_volume2 = 0.5
                    else:
                        effect_volume1 = effect_volume2 = 0
                if (725 <= x_mouse <= 775) and (300 <= y_mouse <= 350):
                    # Music button
                    music = not music
                    if music:
                        music_volume = 0.5
                    else:
                        music_volume = 0
                    pygame.mixer.music.set_volume(music_volume)
            if game_state == 2:
                # When level failed
                if (575 <= x_mouse <= 625) and (300 <= y_mouse <= 350):
                    # Repeat button
                    restart()
                    level.load_level()
                    game_state = 0
                    score = 0
            if game_state == 3:
                # When level complete
                if (525 <= x_mouse <= 575) and (300 <= y_mouse <= 350):
                    # Repeat button
                    restart()
                    level.load_level()
                    game_state = 0
                    score = 0
                if (625 <= x_mouse <= 675) and (300 <= y_mouse <= 350):
                    # Next button
                    restart()
                    level.number += 1
                    game_state = 0
                    level.load_level()
                    score = 0

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

    # Draw the balls who are waiting
    if level.number_of_balls > 0:
        for i in range(level.number_of_balls - 1):
            x = 110 - (i * 32.5)
            screen.blit(ball_img, (x, 570))

    # Draw sling behavior
    if mouse_pressed and level.number_of_balls > 0:
        sling_action()
    else:
        if level.number_of_balls > 0:
            screen.blit(ball_img, (150, 475))
        else:
            pygame.draw.line(screen, ROPE_BACK_COLOR, (sling_x, sling_y + 2), (sling2_x, sling2_y), 5)

    for ball in balls:
        # Balls to remove
        if ball.body.position.y < 60:
            balls_to_remove.append(ball)

        # Position of the ball
        p = ball.body.position
        p = Vec2d(to_pygame(p))

        # Draw the trail
        for point in ball.ball_path:
            pygame.draw.circle(screen, WHITE, point, 3, 0)

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

    # Draw bricks
    for brick in bricks:
        brick.draw_brick(screen)

    # Remove balls
    for ball in balls_to_remove:
        space.remove(ball.shape, ball.shape.body)
        balls.remove(ball)

    # Draw back side of the sling shot
    screen.blit(sling_shot_front, (140, 470))

    # space.debug_draw(draw_options)  # to display the physical representation

    # Draw icons
    screen.blit(pause, (10, 10))
    if game_state == 1:
        pause_caption = font2.render("_____\n\nPAUSE\n\n_____", 1, WHITE)
        screen.blit(pause_caption, (435, 200))
        screen.blit(resume, (425, 300))
        screen.blit(repeat, (525, 300))
        if audio:
            screen.blit(audio_on, (625, 300))
        else:
            screen.blit(audio_off, (625, 300))
        if music:
            screen.blit(music_on, (725, 300))
        else:
            screen.blit(music_off, (725, 300))

    # Draw fps
    fps_caption = normal_font.render("FPS", 1, WHITE)
    fps_value = normal_font.render(str(round(clock.get_fps())), 1, WHITE)
    screen.blit(fps_caption, (1175, 5))
    screen.blit(fps_value, (1185, 20))

    # Draw score
    score_value = font.render(str(score), 1, WHITE)
    if score == 0:
        screen.blit(score_value, (590, 20))
    else:
        screen.blit(score_value, (580, 20))

    draw_level_complete()
    draw_level_failed()

    # Draw cursor
    if not mouse_pressed:
        screen.blit(cursor, (x_mouse, y_mouse))
    else:
        screen.blit(cursor_pressed, (x_mouse, y_mouse))

    # Update physics
    for x in range(2):
        space.step(upd)

    # Flip screen
    pygame.display.flip()
    clock.tick(FPS)

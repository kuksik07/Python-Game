import pygame

# Size of the screen
SCREEN_SIZE = (WIDTH, HEIGHT) = (1200, 650)

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
ROPE_BACK_COLOR = (68, 36, 103)
ROPE_FRONT_COLOR = (97, 63, 121)

# Clock tick
FPS = 50

# Sprites
icon = pygame.image.load('assets/pictures/icon.ico')
background = pygame.image.load('assets/pictures/bg6.png')
cursor = pygame.image.load('assets/pictures/cursor.png')
cursor_pressed = pygame.image.load('assets/pictures/cursor_pressed.png')
ball_img = pygame.image.load('assets/pictures/ball_new.png')
# ball_img = pygame.transform.scale(ball_img, (30, 30))
sling_shot_back = pygame.image.load('assets/pictures/sling-shot-back2.png')
sling_shot_front = pygame.image.load('assets/pictures/sling-shot-front2.png')

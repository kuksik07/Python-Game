import pygame

# Size of the screen
SCREEN_SIZE = (WIDTH, HEIGHT) = (1200, 650)

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ROPE_BACK_COLOR = (68, 36, 103)
ROPE_FRONT_COLOR = (97, 63, 121)

# Clock tick
FPS = 50

# Sprites
background = pygame.image.load('assets/bg6.png')
ball_img = pygame.image.load('assets/ball4.png')
ball_img = pygame.transform.scale(ball_img, (30, 30))
sling_shot_back = pygame.image.load('assets/sling-shot-back2.png')
sling_shot_front = pygame.image.load('assets/sling-shot-front2.png')

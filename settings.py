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
sling_shot_back = pygame.image.load('assets/pictures/sling-shot-back2.png')
sling_shot_front = pygame.image.load('assets/pictures/sling-shot-front2.png')

# Sound
brick_crashed = 'assets/sound/glassy-tap.wav'
throw = 'assets/sound/stuff-up.wav'
jump = 'assets/sound/jump.ogg'
bg_song = 'assets/sound/bg.mp3'

# Icons
music_on = pygame.image.load('assets/pictures/icons/musicOn.png')
music_off = pygame.image.load('assets/pictures/icons/musicOff.png')
audio_on = pygame.image.load('assets/pictures/icons/audioOn.png')
audio_off = pygame.image.load('assets/pictures/icons/audioOff.png')
pause = pygame.image.load('assets/pictures/icons/pause.png')
repeat = pygame.image.load('assets/pictures/icons/return.png')
resume = pygame.image.load('assets/pictures/icons/resume.png')

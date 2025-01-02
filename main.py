import sys
import pygame
import math
import random

pygame.init()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Window variables
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
screen.fill(WHITE)
pygame.display.set_caption('Cool math game!')

# Global variables
running = True


# Font setup
font = pygame.font.Font("STIXTwoMath-Regular.ttf", 50)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()

        self.score = 0

    def update(self):
        pass


class Question:
    def __init__(self):
        pass


class FinalQuestion(Question):
    def __init__(self):
        super().__init__()


bg = pygame.image.load("bg.png").convert()
tiles = math.ceil(SCREEN_WIDTH / bg.get_width()) + 1
scroll = 0

all_sprites = pygame.sprite.Group()

player = Player()

player.rect.center = (screen_rect.center[0] - 500, screen_rect.center[1])
all_sprites.add(player)

# Game loop
while running:
    events = pygame.event.get()

    # Draw background
    for i in range(tiles):
        screen.blit(bg, (i * bg.get_width() + scroll, 0))
    scroll -= 5
    if abs(scroll) > bg.get_width():
        scroll = 0

    for event in events:
        # Manage input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    all_sprites.draw(screen)


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()

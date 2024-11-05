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
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60
FPSObj = pygame.time.Clock()
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.fill(WHITE)
pygame.display.set_caption('Cool math game!')

# Global variables
running = True
SCORE = 0


class BackgroundMoving():
    def __init__(self):
        pass

    def update(self):
        pass

    def render(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = pygame.image.load("Player.png")
        # self.surf = pygame.Surface((40, 75))
        # self.rect = self.surf.get_rect(center = (160, 520))

    def update(self):
        pass


class Question:
    def __init__(self):
        pass


class FinalQuestion(Question):
    def __init__(self):
        super().__init__()


bg = BackgroundMoving()
player = Player()

# Game loop
while running:
    events = pygame.event.get()

    for event in events:
        # Manage input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    FPSObj.tick(FPS)

pygame.quit()
sys.exit()

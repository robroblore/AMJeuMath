import sys
import pygame
import math
import random

# ∫ √

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
FONT_SIZE = 72
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
screen.fill(WHITE)
pygame.display.set_caption('Cool math game!')

# Global variables
running = True

# Font setup
font = pygame.font.Font("STIXTwoMath-Regular.ttf", FONT_SIZE)

QUESTIONS = dict()

with open("QUESTIONS.txt", "r", encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.split(":")
        QUESTIONS[line[0]] = line[1].rstrip()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()

        self.question = ""
        self.answer = ""

        self.input = ""

        self.score = 0

    def generateQuestion(self):
        self.question = random.choice(list(QUESTIONS.keys()))
        self.answer = QUESTIONS[self.question]

    def checkAnswer(self):
        if self.input == self.answer:
            self.score += 1
            self.generateQuestion()
        else:
            self.score -= 1

        self.input = ""

bg = pygame.image.load("bg.png").convert()
tiles = math.ceil(SCREEN_WIDTH / bg.get_width()) + 1
scroll = 0

all_sprites = pygame.sprite.Group()

player = Player()
player.generateQuestion()
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
            elif event.key == pygame.K_RETURN:
                player.checkAnswer()
            elif event.key == pygame.K_BACKSPACE:
                player.input = player.input[:-1]
            else:
                player.input += event.unicode

        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    all_sprites.draw(screen)

    # Draw text
    input_text = font.render(player.input, True, BLACK)
    input_text_rect = input_text.get_rect(center=screen_rect.center)
    input_text_rect.y += 200
    screen.blit(input_text, input_text_rect)

    score_text = font.render(str(player.score), True, BLACK)
    score_text_rect = score_text.get_rect()
    score_text_rect.topright = (screen_rect.right - 10, 10)
    screen.blit(score_text, score_text_rect)

    question_text = font.render(player.question, True, BLACK)
    question_text_rect = question_text.get_rect(center=screen_rect.center)
    question_text_rect.y -= 200
    screen.blit(question_text, question_text_rect)


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()

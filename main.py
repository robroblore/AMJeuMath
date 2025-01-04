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
PINK = (255, 16, 240)

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
font = pygame.font.Font("assets/STIXTwoMath-Regular.ttf", FONT_SIZE)

QUESTIONS = dict()

with open("QUESTIONS.txt", "r", encoding='utf-8') as file:
    for line in file.readlines():
        line = line.split(":")
        QUESTIONS[line[0]] = line[1].rstrip()


class Player(pygame.sprite.Sprite):
    def __init__(self, skin="Robert"):
        super().__init__()
        self.image = pygame.image.load(f"assets/skins/Skin{skin}.png")
        self.image = pygame.transform.scale(self.image, (516, 688))
        self.rect = self.image.get_rect()

        self.offset = {"Katha": 600, "Robert": 460, "Siem": 360}[skin]

        self.death = pygame.image.load(f"assets/skins/Mort{skin}.png")

        self.question = ""
        self.answer = ""

        self.input = ""

        self.hp = 3
        self.score = 0

    def generateQuestion(self):
        self.question = random.choice(list(QUESTIONS.keys()))
        self.answer = QUESTIONS[self.question]

    def checkAnswer(self):
        # Cuz as we all know, 42 is the answer to everything
        if self.input == self.answer or self.input == "42":
            self.score += 1
            self.generateQuestion()
        else:
            self.hp -= 1

            if self.hp == 0:
                self.image = self.death
                self.image = pygame.transform.scale(self.image, (516, 688))

        # Little easter egg :)
        if self.input == "69":
            print("Nice")

        self.input = ""


bg = pygame.image.load("assets/bg.png").convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
tiles = math.ceil(SCREEN_WIDTH / bg.get_width()) + 1
scroll = 0

all_sprites = pygame.sprite.Group()

# Load images
images = [
    pygame.image.load("assets/skins/SkinKatha.png"),
    pygame.image.load("assets/skins/SkinRobert.png"),
    pygame.image.load("assets/skins/SkinSiem.png")
]

# Image dimensions
image_width = 516
image_height = 688

# Scale images to 516x688
images = [pygame.transform.scale(img, (image_width, image_height)) for img in images]

# Calculate spacing between images
spacing = (SCREEN_WIDTH - (image_width * 3)) // 4

# Image positions
image_positions = [
    (spacing, ((SCREEN_HEIGHT - image_height) // 2) + 290),
    (spacing * 2 + image_width, ((SCREEN_HEIGHT - image_height) // 2) + 150),
    (spacing * 3 + image_width * 2, ((SCREEN_HEIGHT - image_height) // 2) + 50)
]

skin_select_image = pygame.image.load("assets/SkinSelect.png")
skin_select_image = pygame.transform.scale(skin_select_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


while True:
    events = pygame.event.get()

    br = False

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if mouse_x < SCREEN_WIDTH // 3:
                player = Player("Katha")
            elif mouse_x < 2 * SCREEN_WIDTH // 3:
                player = Player("Robert")
            else:
                player = Player("Siem")

            br = True

    if br:
        break

    screen.blit(skin_select_image, (0, 0))

    # Draw images
    for idx, pos in enumerate(image_positions):
        screen.blit(images[idx], pos)

    pygame.display.update()
    clock.tick(FPS)

player.generateQuestion()
player.rect.midleft = (0, player.offset * (SCREEN_WIDTH / 1280))  # Still needs work but im too lazy lol
all_sprites.add(player)

# Game loop
while running:
    events = pygame.event.get()

    # Draw background
    for i in range(tiles):
        screen.blit(bg, (i * bg.get_width() + scroll, 0))
    if player.hp > 0:
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
            elif player.hp > 0:
                player.input += event.unicode

        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    all_sprites.draw(screen)

    # Draw text
    input_text = font.render(player.input, True, BLACK)
    input_text_rect = input_text.get_rect(center=screen_rect.center)
    input_text_rect.y += 69
    screen.blit(input_text, input_text_rect)

    if player.hp > 0:
        score_text = font.render(str(player.score), True, BLACK)
        score_text_rect = score_text.get_rect()
        score_text_rect.topright = (screen_rect.right - 10, 10)
        screen.blit(score_text, score_text_rect)

    question_text = font.render(player.question, True, BLACK)
    question_text_rect = question_text.get_rect(center=screen_rect.center)
    question_text_rect.y -= 200
    screen.blit(question_text, question_text_rect)

    if player.hp == 0:
        game_over_text = font.render("YOU DIED!", True, RED)
        screen.blit(game_over_text, game_over_text.get_rect(center=screen_rect.center))

        score_text = font.render("Final score: " + str(player.score), True, BLACK)
        score_text_rect = score_text.get_rect(center=screen_rect.center)
        score_text_rect.y += 100
        screen.blit(score_text, score_text_rect)

    # Draw hp
    hp_image = pygame.image.load(f"assets/hearths/{player.hp}.png")
    hp_image = pygame.transform.scale(hp_image, (774, 1032))
    hp_image_rect = hp_image.get_rect()
    hp_image_rect.topleft = (-250, -200)
    screen.blit(hp_image, hp_image_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()

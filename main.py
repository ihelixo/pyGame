import pygame
import random
import os
from pygame.constants import K_DOWN, K_UP, K_LEFT, K_RIGHT, QUIT

pygame.init()

FPS = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_PLAYER_WHITE = (255, 255, 255)
COLOR_BACKGROUND_BLACK = (0, 0, 0)
COLOR_ENEMY_RED = (255, 0, 0)
COLOR_BONUS_BLUE = (0, 0, 255)

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = 'Goose'
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

player_size = (20, 20)
player = pygame.transform.scale(pygame.image.load('player.png'),
                                (100, 80)).convert_alpha()
player_rect = player.get_rect(center=(50, 300))
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]
playing = True


def creata_bonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png'), (50, 80)).convert_alpha()
    bonus_rect = pygame.Rect(random.randint(100, HEIGHT-50), 50, *bonus.get_size())
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]


def creata_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png'), (80, 50)).convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(50, 550), *enemy.get_size())
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = CREATE_ENEMY + 1
pygame.time.set_timer(CREATE_BONUS, 1000)
CREATE_IMAGES = CREATE_ENEMY + 2
pygame.time.set_timer(CREATE_IMAGES, 200)

bonuses = []
images_index = 0
score = 0
enemies = []

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False

        if event.type == CREATE_ENEMY:
            enemies.append(creata_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(creata_bonus())

        if event.type == CREATE_IMAGES:
            player = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[images_index])),
                                            (100, 80))
            images_index += 1
            if images_index >= len(PLAYER_IMAGES):
                images_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move
    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))
    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        if player_rect.colliderect(enemy[1]):
            playing = False

    main_display.blit(player, player_rect)
    main_display.blit(FONT.render(str(score), True, COLOR_BACKGROUND_BLACK), (WIDTH - 50, 20))

    pygame.display.flip()
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

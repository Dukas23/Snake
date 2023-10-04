import pygame as pg
from pygame.math import Vector2 as V2
from random import randint

pg.init()

WIDTH = 600
HEIGHT = 600

SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

GRID_SIZE = 20
SNAKE_SPEED = 10

snake = [V2(7, 7)]
direction = V2(1, 0)

def draw_snake(SNAKE):
    for segment in SNAKE:
        x_2 = int(segment.x * GRID_SIZE)
        y_2 = int(segment.y * GRID_SIZE)
        pg.draw.rect(SCREEN, GREEN, (x_2, y_2, GRID_SIZE, GRID_SIZE))

def generate_food():
    while True:
        x_1 = randint(0, WIDTH//GRID_SIZE - 1)
        y_1 = randint(0, HEIGHT//GRID_SIZE - 1)
        food_position=V2(x_1, y_1)
        if food_position not in snake:
            return food_position

food = generate_food()

GAME_OVER = False
clock = pg.time.Clock()

while not GAME_OVER:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            GAME_OVER = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and direction != V2(0, 1):
                direction = V2(0, -1)
            if event.key == pg.K_DOWN and direction != V2(0, -1):
                direction = V2(0, 1)
            if event.key == pg.K_LEFT and direction != V2(1, 0):
                direction = V2(-1, 0)
            if event.key == pg.K_RIGHT and direction != V2(-1, 0):
                direction = V2(1, 0)

    # Mover snake
    snake.insert(0, snake[0] + direction)

    # Comprobar colisión bordes
    if snake[0].x < 0 or snake[0].x >= WIDTH//GRID_SIZE:
        GAME_OVER = True
    if snake[0].y < 0 or snake[0].y >= HEIGHT//GRID_SIZE:
        GAME_OVER = True

    # Comprobar colisión consigo mismo
    if len(snake) > 1 and snake[0] in snake[1:]:
        GAME_OVER = True

    # Comer comida
    if snake[0] == food:
        food = generate_food()
    else:
        snake.pop()

    SCREEN.fill(BLACK)

    draw_snake(snake)

    x = int(food.x * GRID_SIZE)
    y = int(food.y * GRID_SIZE)
    pg.draw.rect(SCREEN, RED, (x, y, GRID_SIZE, GRID_SIZE))

    pg.display.update()
    clock.tick(SNAKE_SPEED)

pg.quit()
# End-of-file (EOF)
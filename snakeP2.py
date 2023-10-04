import pygame as pg
from pygame.math import Vector2 as V2
from random import randint

pg.init()

WIDTH = 100
HEIGHT = 100

SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
TABLERO=[[0 for x in range(WIDTH)] for y in range(HEIGHT)]

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

GRID_SIZE = 5
SNAKE_SPEED = 10 

snake = [V2(7, 7)]
direction = V2(1, 0) 

def imprimir_tablero(tablero):
    for fila in tablero:
        fila_str = " ".join(map(str, fila))
        print("{" + fila_str + "}")

def draw_snake(SNAKE):
    
    # Poner a 0 celdas de serpiente anterior
    for segment in snake[1:]:  
        x = int(segment.x)
        y = int(segment.y)
        TABLERO[x][y] = 0


    for segment in SNAKE:
        x = int(segment.x)
        y = int(segment.y)
        TABLERO[x][y] = 1

    for x in range(WIDTH):
        for y in range(HEIGHT):
            if TABLERO[x][y] == 1:
                for segment in SNAKE:
                    x_1 = int(segment.x * GRID_SIZE)
                    y_1 = int(segment.y * GRID_SIZE)
                    pg.draw.rect(SCREEN, GREEN, (x_1, y_1, GRID_SIZE, GRID_SIZE))

def generate_food():
    x_2 = randint(0, WIDTH//GRID_SIZE - 1)
    y_2 = randint(0, HEIGHT//GRID_SIZE - 1)
    return V2(x_2, y_2)

food = generate_food()

game_over = False
clock = pg.time.Clock()

while not game_over:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True
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
        game_over = True 
    if snake[0].y < 0 or snake[0].y >= HEIGHT//GRID_SIZE:
        game_over = True

    # Comprobar colisión consigo mismo 
    if len(snake) > 1 and snake[0] in snake[1:]:
        game_over = True

    # Comer comida
    if snake[0] == food:
        food = generate_food() 
    else:
        snake.pop()

    SCREEN.fill(BLACK)

    draw_snake(snake)

    x = int(food.x * GRID_SIZE)
    y = int(food.y * GRID_SIZE)
    TABLERO[x][y]=2
    pg.draw.rect(SCREEN, RED, (x, y, GRID_SIZE, GRID_SIZE))


    imprimir_tablero(TABLERO)

    pg.display.update()
    clock.tick(SNAKE_SPEED) 
pg.quit()
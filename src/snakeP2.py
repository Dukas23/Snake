import pygame as pg
from pygame.math import Vector2 as V2
from random import randint
import numpy as np
import heapq
#
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
        food_position = V2(x_1, y_1)
        if food_position not in snake:
            return food_position


food = generate_food()

# Matriz para el algoritmo de Dijkstra
distances = np.inf * np.ones((WIDTH//GRID_SIZE, HEIGHT//GRID_SIZE))
distances[int(food.x)][int(food.y)] = 0


def dijkstra():
    queue = [(0, tuple(map(int, food)))]
    while queue:
        dist, pos = heapq.heappop(queue)
        pos = V2(*pos)
        for neighbor in [pos + V2(1, 0), pos + V2(-1, 0), pos + V2(0, 1), pos + V2(0, -1)]:
            if 0 <= neighbor.x < WIDTH//GRID_SIZE and 0 <= neighbor.y < HEIGHT//GRID_SIZE:
                new_dist = dist + 1
                if new_dist < distances[int(neighbor.x)][int(neighbor.y)]:
                    distances[int(neighbor.x)][int(neighbor.y)] = new_dist
                    heapq.heappush(
                        queue, (new_dist, tuple(map(int, neighbor))))


dijkstra()

GAME_OVER = False
clock = pg.time.Clock()

while not GAME_OVER:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            GAME_OVER = True

    # Movimiento automático basado en Dijkstra
    head = snake[0]
    neighbors = [head + V2(1, 0), head + V2(-1, 0),
                 head + V2(0, 1), head + V2(0, -1)]
    min_distance = np.inf
    next_direction = direction
    for neighbor in neighbors:
        if (
            0 <= neighbor.x < WIDTH//GRID_SIZE
            and 0 <= neighbor.y < HEIGHT//GRID_SIZE
            and distances[int(neighbor.x)][int(neighbor.y)] < min_distance
        ):
            min_distance = distances[int(neighbor.x)][int(neighbor.y)]
            next_direction = neighbor - head

    direction = next_direction

    # Mover serpiente
    snake.insert(0, snake[0] + direction)

    # Comprobar colisión con bordes
    if snake[0].x < 0 or snake[0].x >= WIDTH//GRID_SIZE:
        GAME_OVER = True
    if snake[0].y < 0 or snake[0].y >= HEIGHT//GRID_SIZE:
        GAME_OVER = True

    # Comprobar colisión consigo misma
    if len(snake) > 1 and snake[0] in snake[1:]:
        GAME_OVER = True

    # Comer comida
    if snake[0] == food:
        food = generate_food()
        dijkstra()  # Recalcular la ruta después de comer
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

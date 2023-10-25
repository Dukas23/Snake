from random import randint
from collections import deque
import random
import pygame as pg
from pygame.math import Vector2 as V2


pg.init()

WIDTH = 600
HEIGHT = 600
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRID_SIZE = 20
SNAKE_SPEED = 30

snake = [V2(7, 7)]
direction = V2(1, 0)
# * Solucionar problemas como faltantes ejecutar para recordar


def draw_snake(SNAKE):
    for segment in SNAKE:
        x_2 = int(segment.x * GRID_SIZE)
        y_2 = int(segment.y * GRID_SIZE)
        pg.draw.rect(SCREEN, GREEN, (x_2, y_2, GRID_SIZE, GRID_SIZE))


def is_obstacle(pos, snake):
    return (
        pos.x < 0
        or pos.x >= WIDTH // GRID_SIZE
        or pos.y < 0
        or pos.y >= HEIGHT // GRID_SIZE
        or pos in snake
    )


def generate_food(snake):
    while True:
        x_1 = randint(0, WIDTH // GRID_SIZE - 1)
        y_1 = randint(0, HEIGHT // GRID_SIZE - 1)
        food_position = V2(x_1, y_1)
        if not is_obstacle(food_position, snake):
            return food_position


food = generate_food(snake)

GAME_OVER = False
clock = pg.time.Clock()


def bfs(start, target, obstacles):
    start = (int(start.x), int(start.y))
    target = (int(target.x), int(target.y))
    obstacles = set([(int(pos.x), int(pos.y)) for pos in obstacles])

    queue = deque([(start, [])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == target:
            return [V2(pos[0], pos[1]) for pos in path]

        for neighbor in [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1)
        ]:
            if (
                neighbor not in visited
                and neighbor not in obstacles
                and 0 <= neighbor[0] < WIDTH // GRID_SIZE
                and 0 <= neighbor[1] < HEIGHT // GRID_SIZE
            ):
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return []


def move_along_body(snake, head, direction):
    possible_moves = [
        head + V2(1, 0),
        head + V2(-1, 0),
        head + V2(0, 1),
        head + V2(0, -1),
    ]

    valid_moves = [
        move for move in possible_moves if not is_obstacle(move, snake)]

    if not valid_moves:
        # Si no hay movimientos válidos, devolver la dirección opuesta (retroceder)
        return -direction
    else:
        # Elegir el movimiento que aleje más a la serpiente de su cola
        return max(valid_moves, key=lambda move: (move - snake[-1]).length())


def find_longest_path_to_tail(snake, head, tail):
    tail_direction = tail - head
    possible_moves = [
        head + V2(1, 0),
        head + V2(-1, 0),
        head + V2(0, 1),
        head + V2(0, -1),
    ]

    valid_moves = [
        move for move in possible_moves if not is_obstacle(move, snake)]

    if not valid_moves:
        # Si no hay movimientos válidos, devolver la dirección opuesta (retroceder)
        return -tail_direction
    else:
        # Elegir el movimiento que se aleje más del tail
        return max(valid_moves, key=lambda move: (tail - move).length())


def decide_direction(snake, head, food, direction):
    # Calcular el camino hacia la comida
    path_to_food = bfs(head, food, snake[1:])

    if path_to_food:
        return path_to_food[0] - head

    # Calcular el camino hacia la cola
    tail_direction = find_longest_path_to_tail(snake, head, snake[-1])

    if tail_direction:
        return tail_direction
    else:
        # Si no puede encontrar una ruta hacia la comida ni hacia la cola,
        # intenta moverse en una dirección válida que no cause colisión
        possible_moves = [
            V2(1, 0),
            V2(-1, 0),
            V2(0, 1),
            V2(0, -1),
        ]

        valid_moves = [
            move for move in possible_moves if not is_obstacle(head + move, snake)]

        if valid_moves:
            return random.choice(valid_moves)
        else:
            # Si no hay movimientos válidos, moverse en la dirección opuesta
            return -direction


while not GAME_OVER:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            GAME_OVER = True

    head = snake[0]

    if head == food:
        # Generar nueva comida
        food = generate_food(snake)

    # Decidir la dirección a seguir
    direction = decide_direction(snake, head, food, direction)

    # Mover la serpiente
    snake.insert(0, snake[0] + direction)

    if (
        snake[0].x < 0
        or snake[0].x >= WIDTH // GRID_SIZE
        or snake[0].y < 0
        or snake[0].y >= HEIGHT // GRID_SIZE
    ):
        GAME_OVER = True

    if len(snake) > 1 and snake[0] in snake[1:]:
        GAME_OVER = True

    if snake[0] == food:
        food = generate_food(snake)
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

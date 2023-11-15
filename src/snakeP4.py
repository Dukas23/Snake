import random
import pygame as pg
from pygame.math import Vector2 as V2
from random import randint
from collections import deque

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

def a_star(start, target, obstacles):
    start = (int(start[0]), int(start[1]))
    target = (int(target[0]), int(target[1]))
    obstacles = [(int(pos[0]), int(pos[1])) for pos in obstacles]

    open_set = [(start, 0, abs(start[0] - target[0]) + abs(start[1] - target[1]))]
    closed_set = set()
    came_from = {}

    while open_set:
        current, g_score, f_score = min(open_set, key=lambda x: x[2])

        if current == target:
            path = []
            while current in came_from:
                path.append(V2(current[0], current[1]))
                current = came_from[current]
            return path[::-1]

        open_set.remove((current, g_score, f_score))
        closed_set.add(current)

        for neighbor in [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1)
        ]:
            if (
                neighbor not in closed_set
                and neighbor not in obstacles
                and 0 <= neighbor[0] < WIDTH // GRID_SIZE
                and 0 <= neighbor[1] < HEIGHT // GRID_SIZE
            ):
                tentative_g_score = g_score + 1
                if neighbor not in [n[0] for n in open_set] or tentative_g_score < g_score:
                    came_from[neighbor] = current
                    g_score = tentative_g_score
                    f_score = g_score + abs(neighbor[0] - target[0]) + abs(neighbor[1] - target[1])
                    open_set.append((neighbor, g_score, f_score))

    return []

def find_longest_path_to_tail(snake, head, tail):
    tail_direction = tail - head
    possible_moves = [
        head + V2(1, 0),
        head + V2(-1, 0),
        head + V2(0, 1),
        head + V2(0, -1),
    ]

    valid_moves = [move for move in possible_moves if not is_obstacle(move, snake)]

    if not valid_moves:
        return []
    
    max_length = 0
    best_move = None
    for move in valid_moves:
        path_to_tail = a_star(move, tail, snake[1:])
        if path_to_tail and len(path_to_tail) > max_length:
            max_length = len(path_to_tail)
            best_move = move

    return best_move

def verify_future_path(snake, head, direction):
    future_head = (head.x + direction.x, head.y + direction.y)
    obstacles = [(int(pos.x), int(pos.y)) for pos in snake]
    new_path = a_star(future_head, food, obstacles)

    if new_path:
        return True
    else:
        return False

while not GAME_OVER:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            GAME_OVER = True

    head = snake[0]

    if head == food:
        food = generate_food(snake)

    path_to_food = a_star(head, food, snake[1:])

    if path_to_food:
        direction = path_to_food[0] - head
    else:
        tail = snake[-1]
        tail_direction = find_longest_path_to_tail(snake, head, tail)

        if tail_direction and verify_future_path(snake, head, direction):
            direction = tail_direction
        elif not verify_future_path(snake, head, direction):
            possible_moves = [
                V2(1, 0),
                V2(-1, 0),
                V2(0, 1),
                V2(0, -1),
            ]

            valid_moves = [move for move in possible_moves if not is_obstacle(head + move, snake)]

            if valid_moves:
                direction = random.choice(valid_moves)
            else:
                # Si no hay movimientos válidos, moverse en la dirección opuesta
                direction = -direction

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

from random import randint
from collections import deque
import random
from pygame.math import Vector2 as V2


class Model:
    def __init__(self, width, height, grid_size, snake_speed):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.snake_speed = snake_speed
        self.snake = [V2(7, 7)]
        self.direction = V2(1, 0)
        self.food = self.generate_food()
        self.game_over = False

    def generate_food(self):
        while True:
            position_x_food = randint(0, self.width // self.grid_size - 1)
            position_y_food = randint(0, self.height // self.grid_size - 1)
            food_position = V2(position_x_food, position_y_food)
            if not self.is_obstacle(food_position, self.snake):
                return food_position

    def is_obstacle(self, pos, snake):
        return (
            pos.x < 0
            or pos.x >= self.width // self.grid_size
            or pos.y < 0
            or pos.y >= self.height // self.grid_size
            or pos in snake
        )

    def check_collision(self):
        head_snake = self.snake[0]
        if len(self.snake) > 1 and head_snake in self.snake[1:]:
            self.game_over = True

    def move_snake(self):
        head = self.snake[0]
        new_head = head + self.direction
        if self.is_obstacle(new_head, self.snake):
            self.game_over = True
        else:
            self.snake.insert(0, new_head)
            if new_head == self.food:
                self.food = self.generate_food()
            else:
                self.snake.pop()

    def bfs(self, start, target, obstacles):
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
                    and 0 <= neighbor[0] < self.width // self.grid_size
                    and 0 <= neighbor[1] < self.height // self.grid_size
                ):
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []

    def find_longest_path_to_tail(self, snake, head, tail):
        tail_direction = tail - head
        possible_moves = [
            head + V2(1, 0),
            head + V2(-1, 0),
            head + V2(0, 1),
            head + V2(0, -1),
        ]

        valid_moves = [
            move for move in possible_moves if not self.is_obstacle(move, snake)]

        if not valid_moves:
            # Si no hay movimientos válidos, devolver la dirección opuesta (retroceder)
            return -tail_direction
        else:
            # Elegir el movimiento que se aleje más del tail
            return max(valid_moves, key=lambda move: (tail - move).length())

    def decide_direction(self, snake, head, food, direction):
        # Calcular el camino hacia la comida
        path_to_food = self.bfs(head, food, snake[1:])

        if path_to_food:
            return path_to_food[0] - head

        # Calcular el camino hacia la cola
        tail_direction = self.find_longest_path_to_tail(snake, head, snake[-1])

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
                move for move in possible_moves if not self.is_obstacle(head + move, snake)]

            if valid_moves:
                return random.choice(valid_moves)
            else:
                # Si no hay movimientos válidos, moverse en la dirección opuesta
                return -direction

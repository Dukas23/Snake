import pygame as pg
from pygame.math import Vector2 as V2
from random import randint
import heapq
#!codigo completamente malo
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

def calcular_camino_dijkstra(grafo, inicio, objetivo):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    cola = [(0, inicio)]

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        if nodo_actual == objetivo:
            break

        if distancia_actual > distancias[nodo_actual]:
            continue

        for vecino in grafo[nodo_actual]:
            nueva_distancia = distancia_actual + 1  
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                heapq.heappush(cola, (nueva_distancia, vecino))

    # Calcular camino completo
    camino = []
    nodo_actual = objetivo

    while nodo_actual != inicio:
        camino.append(nodo_actual)
        for vecino in grafo[nodo_actual]:
            if distancias[vecino] < distancias[nodo_actual]:
                nodo_actual = vecino
                break

    camino.reverse()
    return camino

def draw_snake(SNAKE):
    for segment in SNAKE:
        x_2 = int(segment.x * GRID_SIZE)
        y_2 = int(segment.y * GRID_SIZE)
        pg.draw.rect(SCREEN, GREEN, (x_2, y_2, GRID_SIZE, GRID_SIZE))
        
def generate_food():
    x_1 = randint(0, WIDTH//GRID_SIZE - 1)
    y_1 = randint(0, HEIGHT//GRID_SIZE - 1)
    food_position = V2(x_1, y_1)
    return food_position

food = generate_food()

GAME_OVER = False
clock = pg.time.Clock()

# Crear grafo
grafo = {}
for y in range(HEIGHT // GRID_SIZE):
    for x in range(WIDTH // GRID_SIZE):
        nodo = (x, y)
        vecinos = []

        if x > 0:
            vecinos.append((x - 1, y))
        if x < (WIDTH // GRID_SIZE - 1):
            vecinos.append((x + 1, y))

        if y > 0:
            vecinos.append((x, y - 1))
        if y < (HEIGHT // GRID_SIZE - 1):
            vecinos.append((x, y + 1))

        grafo[nodo] = vecinos

while not GAME_OVER:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            GAME_OVER = True

    inicio = (int(snake[0].x // GRID_SIZE), int(snake[0].y // GRID_SIZE))
    objetivo = (int(food.x // GRID_SIZE), int(food.y // GRID_SIZE)) 
    camino = calcular_camino_dijkstra(grafo, inicio, objetivo)

    if camino:
        siguiente = V2(camino[0][0] - inicio[0], camino[0][1] - inicio[1])
        snake.insert(0, snake[0] + siguiente)
    else:
        # Si no hay camino, la serpiente sigue en la misma dirección
        snake.insert(0, snake[0] + direction)

   # Comer comida
    if snake[0] == food:
        food = generate_food()
    else:
        snake.pop()

    # Dibujar y actualizar pantalla
    SCREEN.fill(BLACK)
    draw_snake(snake)

    x = int(food.x * GRID_SIZE)
    y = int(food.y * GRID_SIZE)
    pg.draw.rect(SCREEN, RED, (x, y, GRID_SIZE, GRID_SIZE))
    pg.display.update()
    clock.tick(SNAKE_SPEED) 

pg.quit()

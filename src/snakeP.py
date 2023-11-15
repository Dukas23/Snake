from random import randint
import pygame as pg
from pygame.math import Vector2 as V2


def main():
    pg.init()

    # screen size
    width = 600
    height = 600

    screen = pg.display.set_mode((width, height))
    
    # declaration of variables
    red = (255, 0, 0)

    grid_size = 20
    snake_speed = 10

    snake = [V2(7, 7)]
    direction = V2(1, 0)

    count = 0
    font = pg.font.Font(None, 36)

    snake_img = pg.image.load("../img/snke.jpg")
    snake_img.set_colorkey((238, 238, 238) and (
        255, 255, 255) and (239, 239, 239) and (128, 128, 128))
    snake_img.set_alpha(128)
    snake_img = pg.transform.scale(snake_img, (grid_size, grid_size))

    background_img = pg.image.load("../img/background.jpg")
    background_img = pg.transform.scale(background_img, (width, height))

    food = generate_food(snake, width, height, grid_size)

    GAME_OVER = False
    clock = pg.time.Clock()

    # main loop
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
        if snake[0].x < 0 or snake[0].x >= width//grid_size:
            GAME_OVER = True
        if snake[0].y < 0 or snake[0].y >= height//grid_size:
            GAME_OVER = True

        # Comprobar colisión consigo mismo
        if len(snake) > 1 and snake[0] in snake[1:]:
            GAME_OVER = True

        # Comer comida
        if snake[0] == food:
            count += 1
            food = generate_food(snake, width, height, grid_size)
        else:
            snake.pop()

        screen.blit(background_img, (0, 0))

        draw_snake(snake, screen, grid_size, snake_img)
        draw_score(font, count, screen)

        draw_food(food, screen, red, grid_size)

        pg.display.update()
        clock.tick(snake_speed)

    if GAME_OVER:
        show_game_over_screen(font, screen, width, height, clock)

    pg.quit()
    # End-of-file (EOF)


def draw_snake(SNAKE, screen, grid_size, snake_img):
    for i, segment in enumerate(SNAKE):
        snake_position_in_x = int(segment.x * grid_size)
        snake_position_in_y = int(segment.y * grid_size)
        screen.blit(snake_img, (snake_position_in_x, snake_position_in_y))


def draw_food(position_food, screen, color, grid_size):
    position_in_x = int(position_food.x * grid_size)
    position_in_y = int(position_food.y * grid_size)
    pg.draw.rect(screen, color, (position_in_x,
                 position_in_y, grid_size, grid_size))


def generate_food(snake, width, height, grid_size):
    while True:
        food_position_in_x = randint(0, width//grid_size - 1)
        fodd_position_in_y = randint(0, height//grid_size - 1)
        food_position = V2(food_position_in_x, fodd_position_in_y)
        if food_position not in snake:
            return food_position


def show_game_over_screen(font, SCREEN, WIDTH, HEIGHT, clock):
    game_over_text = font.render("¡Game Over!", True, (255, 255, 255))
    restart_text = font.render(
        "Presiona 'S' para reiniciar", True, (255, 255, 255))
    exit_text = font.render("Presiona 'N' para salir", True, (255, 255, 255))

    SCREEN.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
    SCREEN.blit(restart_text, (WIDTH // 2 - 160, HEIGHT // 2))
    SCREEN.blit(exit_text, (WIDTH // 2 - 135, HEIGHT // 2 + 50))

    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    main()
                elif event.key == pg.K_n:
                    global GAME_OVER
                    GAME_OVER = True
                    return

        clock.tick(5)


def draw_score(font, score, screen):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


if __name__ == "__main__":
    main()

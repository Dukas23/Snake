from random import randint
import pygame as pg
from pygame.math import Vector2 as V2



def main():
    pg.init()

    WIDTH = 600
    HEIGHT = 600

    SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

    # BLACK = (0, 0, 0)
    # GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    GRID_SIZE = 20
    SNAKE_SPEED = 10

    snake = [V2(7, 7)]
    direction = V2(1, 0)

    COUNT = 0
    font = pg.font.Font(None, 36)

    snake_img = pg.image.load("../img/snke.jpg")
    snake_img.set_colorkey((238, 238, 238) and (
        255, 255, 255) and (239, 239, 239) and (128, 128, 128))
    snake_img.set_alpha(128)
    snake_img = pg.transform.scale(snake_img, (GRID_SIZE, GRID_SIZE))

    background_img = pg.image.load("../img/background.jpg")
    background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))

    def draw_snake(SNAKE):
        for i, segment in enumerate(SNAKE):
            x_2 = int(segment.x * GRID_SIZE)
            y_2 = int(segment.y * GRID_SIZE)
            SCREEN.blit(snake_img, (x_2, y_2))

    def generate_food():
        while True:
            x_1 = randint(0, WIDTH//GRID_SIZE - 1)
            y_1 = randint(0, HEIGHT//GRID_SIZE - 1)
            food_position = V2(x_1, y_1)
            if food_position not in snake:
                return food_position

    def draw_score(score):
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        SCREEN.blit(score_text, (10, 10))

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
            COUNT += 1
            food = generate_food()
        else:
            snake.pop()

        SCREEN.blit(background_img, (0, 0))

        draw_snake(snake)
        draw_score(COUNT)

        x = int(food.x * GRID_SIZE)
        y = int(food.y * GRID_SIZE)
        pg.draw.rect(SCREEN, RED, (x, y, GRID_SIZE, GRID_SIZE))

        pg.display.update()
        clock.tick(SNAKE_SPEED)

    show_game_over_screen(font, SCREEN, WIDTH, HEIGHT, clock)

    pg.quit()
    # End-of-file (EOF)


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


if __name__ == "__main__":
    main()

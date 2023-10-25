import pygame as pg


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run_game(self):
        while not self.model.game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.model.game_over = True

            head_snake = self.model.snake[0]
            food = self.model.food
            direction = self.model.direction

            # Llamar a decide_direction con los argumentos adecuados
            new_direction = self.model.decide_direction(
                self.model.snake, head_snake, food, direction
            )

            self.model.direction = new_direction
            self.model.move_snake()
            self.model.check_collision()
            self.view.update_display()
            self.view.clock.tick(self.model.snake_speed)

import pygame as pg


class View:
    def __init__(self, model):
        self.model = model
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.screen = pg.display.set_mode((model.width, model.height))
        pg.display.set_caption("Snake Game")
        self.clock = pg.time.Clock()

    def draw_snake(self):
        self.screen.fill(self.black)
        for segment in self.model.snake:
            x = int(segment.x * self.model.grid_size)
            y = int(segment.y * self.model.grid_size)
            pg.draw.rect(self.screen, self.green,
                         (x, y, self.model.grid_size, self.model.grid_size))

    def draw_food(self):
        x = int(self.model.food.x * self.model.grid_size)
        y = int(self.model.food.y * self.model.grid_size)
        pg.draw.rect(self.screen, self.red,
                     (x, y, self.model.grid_size, self.model.grid_size))
    
    def draw_score(self, font, score, screen):
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def update_display(self):
        self.draw_snake()
        self.draw_food()
        self.draw_score(self.model.font, self.model.score, self.screen)
        pg.display.update()

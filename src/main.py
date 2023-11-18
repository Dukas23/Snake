import pygame as pg
from Controller.snake_controller import Controller
from View.snake_view import View
from Model.snake_model import Model
import time 

if __name__ == "__main__":
    pg.init()
    WIDTH = 600
    HEIGHT = 600
    GRID_SIZE = 20
    SNAKE_SPEED = 300
    SCORE = 0
    FONT = pg.font.Font(None, 36)
    model = Model(WIDTH, HEIGHT, GRID_SIZE, SNAKE_SPEED, SCORE, FONT)
    view = View(model)
    controller = Controller(model, view)
    controller.run_game()
    time.sleep(5)
    pg.quit()

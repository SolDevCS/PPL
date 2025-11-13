pygame.init()
from dotenv import load_dotenv
from snake import Snake
from ui import Terminal
import pygame
import random
import os

class Game:
    foods = []
    clock = pygame.time.Clock()

    def __init__(self):
        window_size = os.environ.get("WINDOW_SIZE", "1080x720").split("x")
        self.window = pygame.display.set_mode((int(window_size[0]), int(window_size[1])))
        self.cell_size = int(os.environ.get("CELL_SIZE", "50"))
        self.grid = (10, 10)
        self.map = [
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","x","-","-","-","-","-","-","-","o"],
            ["-","x","-","-","-","-","-","-","-","-"],
            ["-","x","x","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","x","x","-","-"],
            ["-","-","-","-","-","-","x","x","-","-"],
            ["-","-","-","-","-","-","x","x","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","o"]
        ]
        self.snake = Snake(self.map)
        self.terminal = Terminal(680, 420, 400, 300)
        self.generate_food()
    
    def generate_food(self):
        self.foods.clear()
        for i in range(len(self.map[0])):
            for j in range(len(self.map)):
                if self.map[j][i] == 'o':
                    self.foods.append((i, j))

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                self.terminal.handle(event)
                self.snake.move_handler(event)
                
            for food in self.foods:
                if food == self.snake.body[-1]:
                    self.snake.body.insert(0, self.snake.body[0])
                    self.foods.remove(food)

            self.draw()
    
    def draw(self):
        self.window.fill((255, 255, 255))
        for i in range(self.grid[0]):
            for j in range(self.grid[1]):
                if self.map[j][i] == 'x':
                    pygame.draw.rect(self.window, (255, 0, 0), (i*self.cell_size, j*self.cell_size, self.cell_size, self.cell_size), 2)
                else:
                    pygame.draw.rect(self.window, (0, 0, 0), (i*self.cell_size, j*self.cell_size, self.cell_size, self.cell_size), 2)
        for food in self.foods:
            pygame.draw.rect(self.window, (255, 0, 0), (food[0]*self.cell_size, food[1]*self.cell_size, self.cell_size, self.cell_size))
        self.snake.draw(self.window)
        self.terminal.draw(self.window)
        pygame.display.update()


if __name__ == '__main__':
    load_dotenv()
    Game().loop()

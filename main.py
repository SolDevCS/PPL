import pygame
from dotenv import load_dotenv
pygame.init()
load_dotenv()
from snake import Snake
from ui import Terminal, TextButton, ToggleButton
from tkinter import filedialog, messagebox
import random
import os

SHELL_EVENT = pygame.USEREVENT + 1

class Game:
    foods = []
    clock = pygame.time.Clock()
    file:str = ""

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
        self.buttons = [
            TextButton(680, 620, 100, 50, self.load, (0, 255, 0), "Load"),
            TextButton(780, 620, 100, 50, self.save, (0, 255, 0), "Save"),
            TextButton(880, 620, 100, 50, self.save_as, (0, 255, 0), "Save As"),
            TextButton(980, 620, 100, 50, lambda: print("Pressed"), (0, 255, 0), "Start"),
            ToggleButton(680, 670, 400, 50, lambda btn: self.terminal.change_mode(btn.down), (0, 255, 0), ("Script Mode", "Shell Mode"))
        ]
        self.snake = Snake(self.map)
        self.terminal = Terminal(680, 0, 400, 620)
        self.generate_food()
    
    def generate_food(self):
        self.foods.clear()
        for i in range(len(self.map[0])):
            for j in range(len(self.map)):
                if self.map[j][i] == 'o':
                    self.foods.append((i, j))

    def loop(self):
        while True:
            consumed = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif event.type == SHELL_EVENT:
                    print(event.dict)
                for button in self.buttons:
                    button.clicked(event, consumed)
                self.terminal.handle(event)
                self.snake.move_handler(event)
                
            for food in self.foods:
                if food == self.snake.body[-1]:
                    self.snake.body.insert(0, (self.snake.body[0][0], self.snake.body[0][1]-1))
                    self.foods.remove(food)

            self.draw()
    
    def load(self):
        print("pressed load")
        if (self.terminal.text):
            response = messagebox.askyesnocancel('Save', 'Do you want to save your current simulation?')
            if (response):
                self.save()

        try:
            asked_file = filedialog.askopenfilename(filetypes=[('Snake Interpreter Files', '*.si')])
            with open(asked_file, 'r') as f:
                read_data = f.read()
            self.file = asked_file
            pygame.display.set_caption(asked_file)
        except FileNotFoundError as e:
            print(e)
            return
        
        self.terminal.text = read_data
        pygame.display.set_caption(asked_file)
    
    def save(self):
        asked_file = filedialog.asksaveasfilename(filetypes=[('Snake Interpreter Files', '*.si')]) if not self.file else self.file
        if (not asked_file):
            return
        file_names = asked_file.split('.')
        if (len(file_names) > 1):
            asked_file = file_names.pop(0)
        data = self.terminal.text
        
        try:
            with open(f'{asked_file}.si', 'r') as f:
                read_data = f.read()
            if (read_data != data):
                print('saving')
                with open(f'{asked_file}.si', 'w') as f:
                    f.write(data)
        except FileNotFoundError as e:
            print('creating file')
            with open(f'{asked_file}.si', 'w') as f:
                f.write(data)
            self.file = asked_file
            pygame.display.set_caption(asked_file)
    
    def save_as(self):
        self.file = ""
        self.save()
    
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
        for button in self.buttons:
            button.draw(self.window)
        pygame.display.update()


if __name__ == '__main__':
    Game().loop()

import pygame
from dotenv import load_dotenv
pygame.init()
load_dotenv()
from snake import Snake
from ui import Terminal, TextButton, ToggleButton
from tkinter import filedialog, messagebox
from threading import Thread
from time import sleep
import random
import os

SHELL_EVENT = pygame.USEREVENT + 1
MOVE_EVENT = pygame.USEREVENT + 2

class Game:
    foods = []
    clock = pygame.time.Clock()
    program:list[str] = []
    labels = {}
    pc:int = 0
    file:str = ""
    execution_thread:Thread

    def __init__(self, window:pygame.Surface, map:list[list[str]], level):
        self.window = window
        self.level = level
        self.cell_size = int(os.environ.get("CELL_SIZE", "50"))
        self.map = map
        self.buttons = [
            TextButton(680, 620, 100, 50, self.load, (0, 255, 0), "Load"),
            TextButton(780, 620, 100, 50, self.save, (0, 255, 0), "Save"),
            TextButton(880, 620, 100, 50, self.save_as, (0, 255, 0), "Save As"),
            TextButton(980, 620, 100, 50, self.start_simulation, (0, 255, 0), "Start"),
            ToggleButton(680, 670, 400, 50, lambda btn: self.terminal.change_mode(btn.down), (0, 255, 0), ("Script Mode", "Shell Mode"))
        ]
        self.generate_snake()
        self.terminal = Terminal(680, 0, 400, 620)
        self.generate_food()
    
    def generate_snake(self):
        head = (0, 2)
        tail = (0, 0)
        for y in range(len(self.map)):
            if "h" in self.map[y]:
                head = (self.map[y].index("h"), y)
            if "t" in self.map[y]:
                tail = (self.map[y].index("t"), y)
        self.snake = Snake(self.map, tail, head)
        self.direction = {'UP':self.snake.up, "LEFT":self.snake.left, "RIGHT":self.snake.right, "DOWN":self.snake.down}
    
    def generate_food(self):
        self.foods.clear()
        for i in range(len(self.map[0])):
            for j in range(len(self.map)):
                if self.map[j][i].upper() == 'O':
                    self.foods.append((i, j))
    
    def start_simulation(self):
        self.generate_snake()
        self.generate_food()
        self.load_program(self.terminal.text.split("\n"))
        self.execution_thread = Thread(target=self.execute_program, daemon=True)
        self.execution_thread.start()
    
    def next_level(self):
        level = self.level + 1
        try:
            with open(f'lvl{level}.txt', 'r') as f:
                game_map = [line.rstrip("\n").split("\t") for line in f.readlines()]
                Game(self.window, game_map, level).loop()
        except FileNotFoundError:
            messagebox.showinfo("Game Finished!", "Congratulations! There are no more levels to play! Wait for more...")
            exit()

    def loop(self):
        while True:
            consumed = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif event.type == SHELL_EVENT:
                    self.load_program([event.dict.get("instruction")])
                    self.execute_program()
                elif event.type == MOVE_EVENT:
                    print(event.dict)
                    self.direction[event.dict.get("direction")]()
                for button in self.buttons:
                    button.clicked(event, consumed)
                self.terminal.handle(event)
                
            if len(self.foods) == 0:
                self.next_level()

            self.draw()
    
    def load_program(self, lines):
        """Reads the script and tokenizes each instruction."""
        self.program = []
        self.labels = {}
        token_counter = 0

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # skip blanks or comments

            parts = line.split()
            opcode = parts[0].upper()

            # Label definition (e.g. LOOP:)
            if opcode.endswith(":"):
                self.labels[opcode[:-1]] = token_counter
                continue

            # Regular instructions
            self.program.append(parts)
            token_counter += 1


    def execute_program(self):
        """Main interpreter loop."""
        self.pc = 0
        loop_stack = []
        print(self.program)
        while self.pc < len(self.program):
            parts = self.program[self.pc]
            opcode = parts[0].upper()

            # --- MOVE direction steps ---
            if opcode == "MOVE":
                if len(parts) != 3:
                    raise SyntaxError(f"Invalid MOVE syntax at line {self.pc+1}")
                direction = parts[1].upper()
                steps = int(parts[2])
                if (self.terminal.shell_mode):
                    pygame.time.set_timer(pygame.event.Event(MOVE_EVENT, {'direction':direction}), 500, steps)
                else:
                    for _ in range(steps):
                        self.direction[direction]()
                        sleep(0.5)
                self.pc += 1

            # --- EAT ---
            elif opcode == "EAT":
                self.snake.eat(self.foods)
                self.pc += 1

            # --- LOOP count ---
            elif opcode == "LOOP":
                if len(parts) != 2:
                    raise SyntaxError(f"Invalid LOOP syntax at line {self.pc+1}")
                count = int(parts[1])
                loop_stack.append({"start": self.pc + 1, "remaining": count})
                self.pc += 1

            # --- ENDLOOP ---
            elif opcode == "ENDLOOP":
                if not loop_stack:
                    raise SyntaxError(f"ENDLOOP found without LOOP at line {self.pc+1}")
                loop = loop_stack[-1]
                loop["remaining"] -= 1
                if loop["remaining"] > 0:
                    self.pc = loop["start"]  # go back inside loop
                else:
                    loop_stack.pop()
                    self.pc += 1

            # --- Unknown opcode ---
            else:
                raise SyntaxError(f"Unknown opcode '{opcode}' at line {self.pc+1}")
    
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
        for i in range(len(self.map[0])):
            for j in range(len(self.map)):
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
    window_size = os.environ.get("WINDOW_SIZE", "1080x720").split("x")
    window = pygame.display.set_mode((int(window_size[0]), int(window_size[1])))
    game_map = []
    level = 5
    with open(f'lvl{level}.txt', 'r') as f:
        game_map = [line.rstrip("\n").split("\t") for line in f.readlines()]
    Game(window, game_map, level).loop()

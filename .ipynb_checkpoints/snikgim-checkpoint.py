import re
import sys
import copy

# Define constants
DIRECTIONS = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

# Lexer: Tokenizes input lines
def lexer(line):
    tokens = re.findall(r"[A-Z]+|\d+", line.upper())
    return tokens

# 5.1 Lexer
def tokenize_script(script):
    lines = script.strip().split('\n')
    tokenized = []
    for i, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        tokens = lexer(line)
        tokenized.append((i, tokens))
    return tokenized

# Example
script = """MOVE RIGHT 3
MOVE UP 2
EAT
"""
tokenize_script(script)

# 5.2 Parser
def parse(tokens):
    parsed = []
    for line_no, parts in tokens:
        if parts[0] == "MOVE":
            if len(parts) != 3 or parts[1] not in DIRECTIONS:
                raise SyntaxError(f"Invalid MOVE syntax at line {line_no}")
            parsed.append(("MOVE", parts[1], int(parts[2])))
        elif parts[0] == "EAT":
            if len(parts) != 1:
                raise SyntaxError(f"Invalid EAT syntax at line {line_no}")
            parsed.append(("EAT",))
        elif parts[0] == "LOOP":
            if len(parts) != 4:
                raise SyntaxError(f"Invalid LOOP syntax at line {line_no}")
            parsed.append(("LOOP", int(parts[1]), int(parts[2]), int(parts[3])))
        else:
            raise SyntaxError(f"Unknown opcode '{parts[0]}' at line {line_no}")
    return parsed

# 5.3 Executor
class SnakeGame:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        self.snake = [(height // 2, width // 2)]
        self.fruit = (1, 1)
        self.grid[self.fruit[0]][self.fruit[1]] = 'F'
        self.update_grid()

    def update_grid(self):
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) == self.fruit:
                    self.grid[i][j] = 'F'
                elif (i, j) in self.snake:
                    self.grid[i][j] = 'S'
                else:
                    self.grid[i][j] = '.'

    def display(self):
        for row in self.grid:
            print(' '.join(row))
        print()

    def move(self, direction, steps):
        dx, dy = DIRECTIONS[direction]
        for _ in range(steps):
            head_x, head_y = self.snake[0]
            new_head = (head_x + dx, head_y + dy)
            if not (0 <= new_head[0] < self.height and 0 <= new_head[1] < self.width):
                raise RuntimeError("Snake hit the wall!")
            if new_head in self.snake:
                raise RuntimeError("Snake bit itself!")
            self.snake.insert(0, new_head)
            self.snake.pop()
            self.update_grid()
            self.display()

    def eat(self):
        if self.snake[0] == self.fruit:
            self.snake.append(self.snake[-1])  # grow
            print("Fruit eaten! Snake grew.")
            self.fruit = (self.height - 2, self.width - 2)
            self.update_grid()
            self.display()
        else:
            raise RuntimeError("No fruit to eat here!")

# 5.4 Interpreter
def run_interpreter(script):
    tokens = tokenize_script(script)
    parsed = parse(tokens)
    game = SnakeGame()

    i = 0
    while i < len(parsed):
        cmd = parsed[i]
        if cmd[0] == "MOVE":
            game.move(cmd[1], cmd[2])
        elif cmd[0] == "EAT":
            game.eat()
        elif cmd[0] == "LOOP":
            start, end, count = cmd[1], cmd[2], cmd[3]
            for _ in range(count):
                for j in range(start - 1, end):
                    inner_cmd = parsed[j]
                    if inner_cmd[0] == "MOVE":
                        game.move(inner_cmd[1], inner_cmd[2])
                    elif inner_cmd[0] == "EAT":
                        game.eat()
        i += 1
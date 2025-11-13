import pygame
import os

STRAIGHT = pygame.image.load("./assets/straight.png")
CORNER = pygame.image.load("./assets/corner.png")
TAIL = pygame.image.load("./assets/tail.png")
HEAD = pygame.image.load("./assets/head.png")

class Snake:
    def __init__(self,  map:list, tail:tuple[int, int]=(0, 0), head:tuple[int, int]=(0, 2),):
        if (head[0] != tail[0] and head[1] != tail[1]):
            raise ValueError("Head and Tail has to be in the same axis.")
        self.map = map
        self.cell_size = int(os.environ.get("CELL_SIZE", "50"))
        self.body = [tail]
        width = abs(head[0]-tail[0])-1
        height = abs(head[1]-tail[1])-1
        if (width>0):
            for i in range(1, width+1):
                self.body.append((tail[0]+i, tail[1]))
        else:
            for i in range(1, height+1):
                self.body.append((tail[0], tail[1]+i))
        self.body.append(head)
    
    def get_next_step(self) -> dict:
        return {pygame.K_UP:(self.body[-1][0], self.body[-1][1] - 1), pygame.K_DOWN:(self.body[-1][0], self.body[-1][1] + 1), pygame.K_LEFT:(self.body[-1][0] - 1, self.body[-1][1]), pygame.K_RIGHT:(self.body[-1][0] + 1, self.body[-1][1])}
    
    def move_handler(self, event:pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            next_step = self.get_next_step()
            if event.key == pygame.K_UP and next_step[pygame.K_UP] not in self.body and self.map[next_step[pygame.K_UP][1]][next_step[pygame.K_UP][0]] != 'x':
                self.body.append((self.body[-1][0], self.body[-1][1] - 1))
                self.body.pop(0)
            if event.key == pygame.K_DOWN and next_step[pygame.K_DOWN] not in self.body and self.map[next_step[pygame.K_DOWN][1]][next_step[pygame.K_DOWN][0]] != 'x':
                self.body.append((self.body[-1][0], self.body[-1][1] + 1))
                self.body.pop(0)
            if event.key == pygame.K_LEFT and next_step[pygame.K_LEFT] not in self.body and self.map[next_step[pygame.K_LEFT][1]][next_step[pygame.K_LEFT][0]] != 'x':
                self.body.append((self.body[-1][0] - 1, self.body[-1][1]))
                self.body.pop(0)
            if event.key == pygame.K_RIGHT and next_step[pygame.K_RIGHT] not in self.body and self.map[next_step[pygame.K_RIGHT][1]][next_step[pygame.K_RIGHT][0]] != 'x':
                self.body.append((self.body[-1][0] + 1, self.body[-1][1]))
                self.body.pop(0)
    
    def sprite_for_cell(self, body:int):
        _prev, _body, _next = self.body[body-1], self.body[body], self.body[body+1]

        dx_prev, dy_prev = _body[0] - _prev[0], _body[1] - _prev[1]
        dx_next, dy_next = _next[0] - _body[0], _next[1] - _body[1]

        if (dx_prev * dx_next, dy_prev * dy_next) in [(1, 0), (-1, 0)]:
            return pygame.transform.rotozoom(STRAIGHT, 90, 1.0)
        elif (dx_prev * dx_next, dy_prev * dy_next) in [(0, 1), (0, -1)]:
            return STRAIGHT
        elif (dx_prev, dy_prev) == (0, -1) and (dx_next, dy_next) == (-1, 0) or (dx_next, dy_next) == (0, 1) and (dx_prev, dy_prev) == (1, 0):
            return (255, 0, 0) # down-left or left-down
        elif (dx_prev, dy_prev) == (1, 0) and (dx_next, dy_next) == (0, -1) or (dx_next, dy_next) == (-1, 0) and (dx_prev, dy_prev) == (0, 1):
            return (0, 255, 0) # right-down or down-right
        elif (dx_prev, dy_prev) == (-1, 0) and (dx_next, dy_next) == (0, 1) or (dx_next, dy_next) == (1, 0) and (dx_prev, dy_prev) == (0, -1):
            return (0, 0, 255) # right-down or down-right
        else:
            return (0, 0, 0) # right-up
    
    def head_for_cell(self):
        head = self.body[-1]
        
    
    def draw(self, window:pygame.Surface):
        head = self.body[-1]
        tail = self.body[0]

        pygame.draw.rect(window, (0, 255, 0), (tail[0]*self.cell_size, tail[1]*self.cell_size, self.cell_size, self.cell_size))
        for i in range(1, len(self.body)-1):
            part = self.body[i]
            pygame.draw.rect(window, self.sprite_for_cell(i), (part[0]*self.cell_size, part[1]*self.cell_size, self.cell_size, self.cell_size))
        pygame.draw.rect(window, (0, 200, 0), (head[0]*self.cell_size, head[1]*self.cell_size, self.cell_size, self.cell_size))


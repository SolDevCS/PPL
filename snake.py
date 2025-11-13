import pygame
import os

cell_size = os.environ.get("CELL_SIZE", "50")
VERTICAL = pygame.transform.scale(pygame.image.load("./assets/straight.png"), (int(cell_size), int(cell_size)))
HORIZONTAL = pygame.transform.rotozoom(VERTICAL, 90, 1.0)
DOWN_RIGHT = pygame.transform.scale(pygame.image.load("./assets/corner.png"), (int(cell_size), int(cell_size)))
RIGHT_UP = pygame.transform.rotozoom(DOWN_RIGHT, 90, 1.0)
LEFT_UP = pygame.transform.rotozoom(DOWN_RIGHT, 180, 1.0)
LEFT_DOWN = pygame.transform.rotozoom(DOWN_RIGHT, 270, 1.0)
DOWN_TAIL = pygame.transform.scale(pygame.image.load("./assets/tail.png"), (int(cell_size), int(cell_size)))
RIGHT_TAIL = pygame.transform.rotozoom(DOWN_TAIL, 90, 1.0)
UP_TAIL = pygame.transform.rotozoom(DOWN_TAIL, 180, 1.0)
LEFT_TAIL = pygame.transform.rotozoom(DOWN_TAIL, 270, 1.0)
UP_HEAD = pygame.transform.scale(pygame.image.load("./assets/head.png"), (int(cell_size), int(cell_size)))
LEFT_HEAD = pygame.transform.rotozoom(UP_HEAD, 90, 1.0)
DOWN_HEAD = pygame.transform.rotozoom(UP_HEAD, 180, 1.0)
RIGHT_HEAD = pygame.transform.rotozoom(UP_HEAD, 270, 1.0)

class Snake:
    def __init__(self,  map:list, tail:tuple[int, int]=(0, 0), head:tuple[int, int]=(0, 2)):
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
                self.up()
            if event.key == pygame.K_DOWN and next_step[pygame.K_DOWN] not in self.body and self.map[next_step[pygame.K_DOWN][1]][next_step[pygame.K_DOWN][0]] != 'x':
                self.down()
            if event.key == pygame.K_LEFT and next_step[pygame.K_LEFT] not in self.body and self.map[next_step[pygame.K_LEFT][1]][next_step[pygame.K_LEFT][0]] != 'x':
                self.left()
            if event.key == pygame.K_RIGHT and next_step[pygame.K_RIGHT] not in self.body and self.map[next_step[pygame.K_RIGHT][1]][next_step[pygame.K_RIGHT][0]] != 'x':
                self.right()
    
    def up(self):
        self.body.append((self.body[-1][0], self.body[-1][1] - 1))
        self.body.pop(0)
    
    def down(self):
        self.body.append((self.body[-1][0], self.body[-1][1] + 1))
        self.body.pop(0)
    
    def left(self):
        self.body.append((self.body[-1][0] - 1, self.body[-1][1]))
        self.body.pop(0)
    
    def right(self):
        self.body.append((self.body[-1][0] + 1, self.body[-1][1]))
        self.body.pop(0)
    
    def eat(self):
        pass
    
    def sprite_for_cell(self, body:int):
        _prev, _body, _next = self.body[body-1], self.body[body], self.body[body+1]

        dx_prev, dy_prev = _body[0] - _prev[0], _body[1] - _prev[1]
        dx_next, dy_next = _next[0] - _body[0], _next[1] - _body[1]

        if (dx_prev * dx_next, dy_prev * dy_next) in [(1, 0), (-1, 0)]:
            return HORIZONTAL
        elif (dx_prev * dx_next, dy_prev * dy_next) in [(0, 1), (0, -1)]:
            return VERTICAL
        elif (dx_prev, dy_prev) == (0, -1) and (dx_next, dy_next) == (-1, 0) or (dx_next, dy_next) == (0, 1) and (dx_prev, dy_prev) == (1, 0):
            return LEFT_DOWN # down-left or left-down
        elif (dx_prev, dy_prev) == (1, 0) and (dx_next, dy_next) == (0, -1) or (dx_next, dy_next) == (-1, 0) and (dx_prev, dy_prev) == (0, 1):
            return LEFT_UP # right-down or down-right
        elif (dx_prev, dy_prev) == (-1, 0) and (dx_next, dy_next) == (0, 1) or (dx_next, dy_next) == (1, 0) and (dx_prev, dy_prev) == (0, -1):
            return DOWN_RIGHT # left-up or up-left
        else:
            return RIGHT_UP # right-up or up-right
    
    def head_for_cell(self):
        prev = self.body[-2]
        head = self.body[-1]
        dx, dy = head[0] - prev[0], head[1] - prev[1]
        

        if dx > 0:
            return RIGHT_HEAD
        elif dx < 0:
            return LEFT_HEAD
        elif dy > 0:
            return DOWN_HEAD
        else:
            return UP_HEAD
    
    def tail_for_cell(self):
        body = self.body[1]
        tail = self.body[0]
        dx, dy = body[0] - tail[0], body[1] - tail[1]
        

        if dx > 0:
            return LEFT_TAIL
        elif dx < 0:
            return RIGHT_TAIL
        elif dy > 0:
            return UP_TAIL
        else:
            return DOWN_TAIL
        
    
    def draw(self, window:pygame.Surface):
        head = self.body[-1]
        tail = self.body[0]

        tail_image = self.tail_for_cell()
        window.blit(tail_image, tail_image.get_rect(topleft=(tail[0]*self.cell_size, tail[1]*self.cell_size)))
        for i in range(1, len(self.body)-1):
            part = self.body[i]
            body_image= self.sprite_for_cell(i)
            window.blit(body_image, body_image.get_rect(topleft=(part[0]*self.cell_size, part[1]*self.cell_size)))
        head_image = self.head_for_cell()
        window.blit(head_image, head_image.get_rect(topleft=(head[0]*self.cell_size, head[1]*self.cell_size)))


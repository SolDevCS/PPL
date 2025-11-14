import pygame
from typing import Callable

FONT = pygame.font.Font(None, 25)
SHELL_EVENT = pygame.USEREVENT + 1


class Terminal:
    text = ""
    history:list[str] = []
    focused = False
    shell_mode = False
    y_offset = 0
    text_bottom = 0

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def change_mode(self, state):
        self.shell_mode = state
        self.history.clear()
        self.text = ""

    def handle(self, event:pygame.event.Event):
        if (event.type == pygame.MOUSEBUTTONDOWN):
            self.focused = self.rect.collidepoint(event.pos)
        elif (event.type == pygame.MOUSEWHEEL and self.focused):
            if (event.y > 0 and self.y_offset < 0 or event.y < 0 and self.text_bottom > self.rect.height - 10):
                self.y_offset += (event.y * 10)
        if (event.type == pygame.KEYDOWN and self.focused):
            if (event.key == pygame.K_BACKSPACE and len(self.text) > 0):
                self.text = self.text[:len(self.text)-1]
            elif (event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]):
                if (self.shell_mode):
                    self.history.append(self.text)
                    pygame.event.post(pygame.event.Event(SHELL_EVENT, {"instruction":self.text}))
                    self.text = ""
                    return
                else:
                    self.text += "\n"
            elif (event.key != pygame.K_BACKSPACE):
                self.text += event.unicode
    
    def draw(self, window:pygame.Surface):
        pygame.draw.rect(window, (255, 255, 255), self.rect)
        if (self.shell_mode):
            self.text_bottom = self.rect.top + 10
            for i, line in enumerate(self.history):
                text = FONT.render(line, False, (0, 0, 0))
                rect = text.get_rect(topleft=(self.rect.left + 10, self.y_offset + (i*text.get_height()) + self.rect.top + 10))
                window.blit(text, rect)
                if i == len(self.history)-1:
                    self.text_bottom = rect.bottom
            shell_text = FONT.render(f">>>{self.text}", False, (0, 0, 0))
            rect = shell_text.get_rect(topleft=(self.rect.left + 10, self.text_bottom))
            self.text_bottom += rect.height
            window.blit(shell_text, rect)
        else:
            for i, line in enumerate(self.text.split("\n")):
                text = FONT.render(f"{i+1}: {line}", False, (0, 0, 0))
                rect = text.get_rect(topleft=(self.rect.left + 10, self.y_offset + (i*text.get_height()) + self.rect.top + 10))
                window.blit(text, rect)
                if i == len(self.text.split("\n"))-1:
                    self.text_bottom = rect.bottom
        pygame.draw.rect(window, (120, 120, 120), self.rect, 10)
        

class ButtonBehavior:
    def __init__(self, left:float, top:float, width:float, height:float, on_press:Callable|None, args:tuple=()):
        self.rect = pygame.Rect(left, top, width, height)
        self.clickable:bool = True
        self.args = args
        self.on_press = on_press
        self.inside = False
    
    def clicked(self, event:pygame.event.Event, consumed:list) -> bool:
        mouse = pygame.mouse.get_pos()
        if (event.type == pygame.MOUSEMOTION and self.rect.collidepoint(mouse) and self.clickable):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.inside = True
        elif (self.inside and not self.rect.collidepoint(mouse)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.inside = False
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event not in consumed):
            if (self.rect.collidepoint(mouse) and self.clickable):
                if (self.on_press):
                    if (self.args):
                        self.on_press(*self.args)
                    else:
                        self.on_press()
                consumed.append(event)
                return True
        return False


class TextButton(ButtonBehavior):
    def __init__(self, left: float, top: float, width: float, height: float, on_press: Callable, background_color:tuple[int, int, int], content:str, args:tuple=()):
        super().__init__(left, top, width, height, on_press, args)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 100))
        self.background_color = background_color
        self.content = content
    
    def get_text(self) -> tuple[pygame.Surface, pygame.Rect]:
        text = FONT.render(self.content, True, (0, 0, 0))
        return (text, text.get_rect(center=self.rect.center))
    
    def draw(self, window:pygame.Surface) -> None:
        pygame.draw.rect(window, self.background_color, self.rect)
        if (not self.clickable):
            window.blit(self.surface, self.rect)
        if (self.content):
            text, rect = self.get_text()
            window.blit(text, rect)


class ToggleButton(ButtonBehavior):
    def __init__(self, left:float, top:float, width:float, height:float, on_toggle:Callable, background_color:tuple[int, int, int], content:tuple[str, str]):
        super().__init__(left, top, width, height, None)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 80))
        self.background_color = background_color
        self.on_toggle = on_toggle
        self.content = content
        self.down = False
    
    def get_text(self) -> tuple[pygame.Surface, pygame.Rect]:
        text = FONT.render(self.content[0], True, (0, 0, 0)) if not self.down else FONT.render(self.content[1], True, (0, 0, 0))
        return (text, text.get_rect(center=self.rect.center))
    
    def clicked(self, event:pygame.event.Event, consumed:list) -> bool:
        if (super().clicked(event, consumed)):
            self.down = not self.down
            if (self.on_toggle):
                self.on_toggle(self)
            return True
        return False
    
    def draw(self, window:pygame.Surface) -> None:
        pygame.draw.rect(window, self.background_color, self.rect)
        if (self.content):
            text, rect = self.get_text()
            window.blit(text, rect)

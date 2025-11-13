import pygame


class Terminal:
    text = ""
    focused = False

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 25)

    def handle(self, event:pygame.event.Event):
        if (event.type == pygame.MOUSEBUTTONDOWN):
            self.focused = self.rect.collidepoint(event.pos)
        if (event.type == pygame.KEYDOWN and self.focused):
            if (event.key == pygame.K_BACKSPACE and len(self.text) > 0):
                self.text = self.text[:len(self.text)-1]
            else:
                self.text += event.unicode
        
    
    def draw(self, window:pygame.Surface):
        pygame.draw.rect(window, (255, 255, 255), self.rect)
        pygame.draw.rect(window, (120, 120, 120), self.rect, 10)
        text = self.font.render(self.text, False, (0, 0, 0))
        window.blit(text, (self.rect.left + 10, self.rect.top + 10))
        

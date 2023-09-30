import pygame

class Button:
    def __init__(self, pos, size, color, value, text = "", text_color = "black", text_size = 10):
        self.value = value
        self.pos = list(pos)
        self.size = list(size)
        self.color = color
        self.text = text
        self.font = pygame.font.Font("Data/Pixeltype.ttf", text_size)
        self.text_color = text_color
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.color = 'red'
        if pygame.Rect.collidepoint(self.rect(), mouse_pos):
            self.color = 'blue'
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0]:
                return self.value
        return None

    def rect(self):
        return pygame.Rect(self.pos, self.size)
    
    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect())
        string = self.font.render(self.text, True, self.text_color)
        srect = string.get_rect(center = self.rect().center)
        screen.blit(string, srect )
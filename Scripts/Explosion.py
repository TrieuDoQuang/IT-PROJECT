import pygame

class Explosion:
    def __init__(self, pos, size, dame, owner):
        self.pos = pos
        self.size = size
        self.dame = dame
        self.owner = owner
        self.done = False
        self.surf = pygame.Surface(self.size)
    
    def rect(self):
        return self.surf.get_rect(center = self.pos)
    
    def update(self):
        self.done = True
    
    def render(self, surf, offset):
        surf.blit(self.surf, (self.rect().left - offset[0], self.rect().top - offset[1]))
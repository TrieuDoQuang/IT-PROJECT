import pygame
from Scripts.Entities import PhysicsEntity

class Player(PhysicsEntity):
    def __init__(self, e_type, pos, size, assets, Health = 400, size_mul = 2):
        super().__init__(e_type, pos, size, assets, Health)
        self.size_mul = size_mul
    
    def update(self, tilemap):
        super().update(tilemap)
        self.animations_offset = list(self.animations_offset)
        self.animations_offset[1] = -23
    
    def render(self, surf, offset = (0,0)):
       img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.size_mul , self.animation.IMG().get_height() * self.size_mul))
       surf.blit(pygame.transform.flip(img, self.flip, False), (self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))
    

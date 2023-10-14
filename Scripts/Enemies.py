from Entities import *
import pygame

class Skeleton(PhysicsEntity):
    def __init__(self, e_type, pos, size, assets, Health=100, speed=1.5, scale = 1):
        super().__init__(e_type, pos, size, assets, Health, speed)
        self.scale = scale
    
    def update(self, tilemap):
        return super().update(tilemap)

    def render(self, surf, offset = (0,0)):
        #HITBOX DEBUG
        #    ac = pygame.Surface(self.size)
        #    pos = (self.rect().x - offset[0] , self.rect().y - offset[1])
        #    surf.blit(ac, pos)
        
        img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.scale , self.animation.IMG().get_height() * self.scale))
        return super().render(surf, offset)
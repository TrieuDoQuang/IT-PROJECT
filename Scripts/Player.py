import pygame
from Scripts.Entities import PhysicsEntity

class Player(PhysicsEntity):
    def __init__(self, e_type, pos, size, assets, Health = 400, size_mul = 1, animoffset = (-3, -3)):
        super().__init__(e_type, pos, size, assets, Health)
        self.size_mul = size_mul
        self.animations_offset = list(animoffset)
        self.Air_time = 0
        self.Wall_slide = False
        self.reload_time = 800
        self.reloading = 0
        self.invs = 1000
    
    def update(self, tilemap):
        super().update(tilemap)
        self.Air_time += 1

        if self.Coll['bottom']:
            self.Air_time = 0

        self.Wall_slide = False
        if self.Coll['right'] or self.Coll['left'] and self.Air_time > 4:
            self.Wall_slide = True
            self.Vel.y = min(self.Vel.y, 0.5)
            if self.Coll['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')

        if self.Walljump and self.Air_time > 45:
            self.Air_time = 4
            self.Vel.y = -2.5
            if self.Coll['right']:
                self.Vel.x = -2.5
            else:
                self.Vel.x = 2.5

        if not self.Wall_slide:
            if self.Air_time > 4:
                self.set_action('jump')
            elif self.Dir.x != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
        
        
        return False
    
    def render(self, surf, offset = (0,0)):
       img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.size_mul , self.animation.IMG().get_height() * self.size_mul))
       surf.blit(pygame.transform.flip(img, self.flip, False), (self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))
    

import pygame, random
from Scripts.Entities import *

class Zombie(PhysicsEntity):
    def __init__(self, game, e_type, pos, size, assets, Health = 150, speed=1.5, scale = 1, animations_offset=(0, 0)):
        super().__init__(e_type, pos, size, assets, Health, speed)
        self.scale = scale
        self.animations_offset = animations_offset
        self.walking = 0
        self.Air_time = 0
        self.game = game
        self.weapon = Wep_Ene('rifle', Loffset=(100, 10), Roffset=(15, 10), scale=1)

    def walk(self, tilemap):
        if not self.walking:
            self.walking = random.randint(30, 120)
        if tilemap.solid_check((self.pos[0], self.pos[1]), self.size, self.flip):
            if self.Coll['left'] or self.Coll['right']:
                self.flip = not self.flip
        else:
            self.flip = not self.flip
        self.Dir.x = (-1 if self.flip else 1)
    
    def attack(self):
        self.weapon.attack(self.game, self)
        self.walking = 0

    def update(self, tilemap, player):
        super().update(tilemap)
        self.Air_time += 1
        if self.Coll['bottom']:
            self.Air_time = 0

        # self.dbg = tilemap.solid_check(
        #     (self.pos[0], self.pos[1]), self.size, self.flip)

        self.walking = max(0, self.walking - 1)
        if self.walking == 0:
            self.Dir.x = 0
        else:
            if self.Air_time < 1:
                self.walk(tilemap)

        if abs(player.rect().x - self.rect().x) <= 224:
            if self.rect().bottom - player.rect().bottom  < 64 and self.rect().bottom - player.rect().bottom >= 0:
                if self.rect().x - player.rect().x > 0:
                    self.flip = True
                if self.rect().x - player.rect().x < 0:
                    self.flip = False
                self.attack()
        self.weapon.update(self.rect(), self.flip)

        if self.action == 'idle' and self.Air_time < 1 and self.weapon.action == 'idle':
            chance = random.randint(0, 100)
            if chance < 10:
                self.walk(tilemap)

        if self.Dir.x != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset=(0, 0)):
        img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.scale, self.animation.IMG().get_height() * self.scale))
        surf.blit(pygame.transform.flip(img, self.flip, False),(self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))
        self.weapon.render(surf, self.flip, offset)
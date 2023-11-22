import pygame, random
from Scripts.Entities import *

pygame.mixer.init()
class Cat(PhysicsEntity):
    def __init__(self, game, e_type, pos, size, assets, Health = 150, speed=1.5, scale = 1, animations_offset=(0, 0)):
        super().__init__(e_type, pos, size, assets, Health, speed)
        self.scale = scale
        self.animations_offset = animations_offset
        self.game = game

        self.walking = 0
        self.laying = 0
        self.licking = 0
        self.strecthing = 0

        self.timer = pygame.time.get_ticks()
        self.delay = 1000

        self.meow1 = pygame.mixer.Sound('Data/sfx/moew1.mp3')
        self.meow1.set_volume(0.5)
        self.meow2 = pygame.mixer.Sound('Data/sfx/moew2.mp3')
        self.meow2.set_volume(0.1)

        self.air_time = 0
    
    def DMG(self, dmg):
        pass

    def walk(self, tilemap):
        self.set_action('walking')
        if not self.walking:
            self.walking = random.randint(50, 200)
        if tilemap.solid_check((self.pos[0], self.pos[1]), self.size, self.flip):
            if self.Coll['left'] or self.Coll['right']:
                self.flip = not self.flip
        else:
            self.flip = not self.flip
        if self.air_time <= 4:
            self.Dir.x = (-1 if self.flip else 1)
    
    def lay(self):
        self.set_action('laying')
        if not self.laying:
            self.laying = random.randint(300, 500)
    
    def lick(self):
        self.set_action('licking')
        if not self.licking:
            self.laying = random.randint(300, 400)
    
    def stretch(self):
        self.set_action('stretch')
        if not self.strecthing:
            self.strecthing = random.randint(100, 150)
    
    def move(self, tilemap):
        chance = random.randint(0, 100)
        if chance < 10:
            self.lay()
        elif chance < 20:
            self.set_action('sitting')
        elif chance < 30:
            self.walk(tilemap)
        
        if chance < 20:
            choice = random.choice(['moew1', 'meow2'])
            if choice == 'moew1':
                self.meow1.play()
            elif choice == 'meow2':
                self.meow2.play()

    def update(self, tilemap):
        super().update(tilemap)
        self.air_time += 1
        if self.Coll['bottom']:
            self.air_time = 0

        now = pygame.time.get_ticks()

        if self.action == 'idle':
            if now - self.timer >= self.delay:
                self.move(tilemap)
                self.timer = pygame.time.get_ticks()

        if self.action == 'sitting':
            if self.animation.done:
                choice =  random.choice(['lick', 'stretch'])
                if choice == 'lick':
                    self.lick()
                elif choice == 'stretch':
                    self.stretch()

        self.walking = max(self.walking - 1, 0)
        self.laying = max(self.laying - 1, 0)
        self.licking = max(self.licking - 1, 0)
        self.strecthing = max(self.strecthing - 1, 0)

        if self.walking != 0:
            self.walk(tilemap)
        else:
            self.Dir.x = 0

        if self.Dir.x == 0:
            if self.walking == 0 and self.laying == 0 and self.licking == 0 and self.strecthing == 0:
                if self.action == 'laying':
                    self.set_action('wakeup')
                elif self.action == 'wakeup':
                    if self.animation.done:
                        self.set_action('idle')
                elif self.action == 'sitting':
                    pass
                else:
                    self.set_action('idle')
    
    def render(self, surf, offset=(0, 0)):
        # rect = pygame.Surface((self.rect().width, self.rect().height))
        # surf.blit(rect, (self.rect().x - offset[0], self.rect().y - offset[1]))

        img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.scale, self.animation.IMG().get_height() * self.scale))
        surf.blit(pygame.transform.flip(img, self.flip, False),(self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))
from Scripts.Entities import *
import pygame, random

class Skeleton(PhysicsEntity):
    def __init__(self, e_type, pos, size, assets, Health=100, speed=1.5, scale = 1, animations_offset=(0, 0)):
        super().__init__(e_type, pos, size, assets, Health, speed)
        self.scale = scale
        self.animations_offset = animations_offset
        self.walking = 0
        self.Air_time = 0
        self.attacking = 0

    def walk(self, tilemap):
        if not self.walking:
            self.walking = random.randint(30, 120)
        if tilemap.solid_check((self.pos[0], self.pos[1]), self.size, self.flip):
            if self.Coll['left'] or self.Coll['right']:
                self.flip = not self.flip
        else:
            self.flip = not self.flip
        self.Dir.x = ( -1 if self.flip else 1)
    
    def attack(self):
        self.attacking = 100

    
    def update(self, tilemap, player):

        self.Air_time += 1
        if self.Coll['bottom']:
            self.Air_time = 0

        self.dbg = tilemap.solid_check((self.pos[0], self.pos[1]), self.size, self.flip)

        self.walking = max(0, self.walking - 1)
        if self.walking == 0:
            self.Dir.x = 0
        else:
            self.walk(tilemap)
        
        if abs(player.rect().x - self.rect().x) < 90:
            if self.rect().x - player.rect().x > 0:
                self.flip = True
            if self.rect().x - player.rect().x < 0:
                self.flip = False
            self.attack()
        
        self.attacking = max(0, self.attacking - 1)

        chance = random.random() * 0.001
        if chance < 0.00005 and self.action == 'idle' and self.Air_time < 4:
                self.walk(tilemap)

        super().update(tilemap)

        if self.attacking:
            self.set_action('attack')
        elif self.Dir.x != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset = (0,0)):
        #HITBOX DEBUG
        ac = pygame.Surface(self.size)
        pos = (self.rect().x - offset[0] , self.rect().y - offset[1])
        surf.blit(ac, pos)
        if self.dbg:
            rect = pygame.Rect(self.dbg['pos'][0] * 32 -offset[0], self.dbg['pos'][1] *32 - offset[1], 32, 32)
            ac2 = pygame.Surface((32, 32))
            surf.blit(ac2, rect)

        img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.scale , self.animation.IMG().get_height() * self.scale))
        surf.blit(pygame.transform.flip(img, self.flip, False), (self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))

class Thug(PhysicsEntity):
    def __init__(self, e_type, pos, size, assets, Health=100, speed=1.5, scale = 1, animations_offset=(0, 0)):
        super().__init__(e_type, pos, size, assets, Health, speed)
        self.scale = scale
        self.animations_offset = animations_offset
        self.walking = 0
        self.Air_time = 0
        self.attacking = 0

    def walk(self, tilemap):
        if not self.walking:
            self.walking = random.randint(30, 120)
        if tilemap.solid_check((self.pos[0], self.pos[1]), self.size, self.flip):
            if self.Coll['left'] or self.Coll['right']:
                self.flip = not self.flip
        else:
            self.flip = not self.flip
        self.Dir.x = (-1 if self.flip else 1)

    # def attack(self):
    #     self.attacking = 100

    def update(self, tilemap, player):

        self.Air_time += 1
        if self.Coll['bottom']:
            self.Air_time = 0

        self.dbg = tilemap.solid_check(
            (self.pos[0], self.pos[1]), self.size, self.flip)

        self.walking = max(0, self.walking - 1)
        if self.walking == 0:
            self.Dir.x = 0
        else:
            self.walk(tilemap)

        # if abs(player.rect().x - self.rect().x) < 90:
        #     if self.rect().x - player.rect().x > 0:
        #         self.flip = True
        #     if self.rect().x - player.rect().x < 0:
        #         self.flip = False
        #     self.attack()

        # self.attacking = max(0, self.attacking - 1)

        chance = random.random() * 0.001
        if chance < 0.00005 and self.action == 'idle' and self.Air_time < 4:
            self.walk(tilemap)

        super().update(tilemap)

        # if self.attacking:
        #     self.set_action('attack')
        if self.Dir.x != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset=(0, 0)):
        #HITBOX DEBUG
        ac = pygame.Surface(self.size)
        pos = (self.rect().x - offset[0] , self.rect().y - offset[1])
        surf.blit(ac, pos)
        if self.dbg:
            rect = pygame.Rect(self.dbg['pos'][0] * 32 -offset[0], self.dbg['pos'][1] *32 - offset[1], 32, 32)
            ac2 = pygame.Surface((32, 32))
            surf.blit(ac2, rect)

        img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.scale, self.animation.IMG().get_height() * self.scale))
        surf.blit(pygame.transform.flip(img, self.flip, False),(self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))

class Wizard(PhysicsEntity):
    def __init__(self, e_type, pos, size, assets, Health=100, speed=1.5, scale = 1, animations_offset=(0, 0)):
        super().__init__(e_type, pos, size, assets, Health, speed)
        self.scale = scale
        self.animations_offset = animations_offset
        self.walking = 0
        self.Air_time = 0
        self.attacking = 0

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
        self.attacking = 120

    def update(self, tilemap, player):

        self.Air_time += 1
        if self.Coll['bottom']:
            self.Air_time = 0

        self.dbg = tilemap.solid_check(
            (self.pos[0], self.pos[1]), self.size, self.flip)

        self.walking = max(0, self.walking - 1)
        if self.walking == 0:
            self.Dir.x = 0
        else:
            self.walk(tilemap)

        if abs(player.rect().x - self.rect().x) < 90:
            if self.rect().x - player.rect().x > 0:
                self.flip = True
            if self.rect().x - player.rect().x < 0:
                self.flip = False
            self.attack()

        self.attacking = max(0, self.attacking - 1)

        chance = random.random() * 0.001
        if chance < 0.00005 and self.action == 'idle' and self.Air_time < 4:
            self.walk(tilemap)

        super().update(tilemap)

        if self.attacking:
            self.set_action('attack')
        if self.Dir.x != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset=(0, 0)):
        #HITBOX DEBUG
        ac = pygame.Surface(self.size)
        pos = (self.rect().x - offset[0] , self.rect().y - offset[1])
        surf.blit(ac, pos)
        if self.dbg:
            rect = pygame.Rect(self.dbg['pos'][0] * 32 -offset[0], self.dbg['pos'][1] *32 - offset[1], 32, 32)
            ac2 = pygame.Surface((32, 32))
            surf.blit(ac2, rect)

        img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.scale, self.animation.IMG().get_height() * self.scale))
        surf.blit(pygame.transform.flip(img, self.flip, False),(self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))

class Zombie(PhysicsEntity):
    def __init__(self, e_type, pos, size, assets, Health=100, speed=1.5, scale = 1, animations_offset=(0, 0)):
        super().__init__(e_type, pos, size, assets, Health, speed)
        self.scale = scale
        self.animations_offset = animations_offset
        self.walking = 0
        self.Air_time = 0
        self.attacking = 0

    def walk(self, tilemap):
        if not self.walking:
            self.walking = random.randint(30, 120)
        if tilemap.solid_check((self.pos[0], self.pos[1]), self.size, self.flip):
            if self.Coll['left'] or self.Coll['right']:
                self.flip = not self.flip
        else:
            self.flip = not self.flip
        self.Dir.x = (-1 if self.flip else 1)

    # def attack(self):
    #     self.attacking = 100

    def update(self, tilemap, player):

        self.Air_time += 1
        if self.Coll['bottom']:
            self.Air_time = 0

        self.dbg = tilemap.solid_check(
            (self.pos[0], self.pos[1]), self.size, self.flip)

        self.walking = max(0, self.walking - 1)
        if self.walking == 0:
            self.Dir.x = 0
        else:
            self.walk(tilemap)

        # if abs(player.rect().x - self.rect().x) < 90:
        #     if self.rect().x - player.rect().x > 0:
        #         self.flip = True
        #     if self.rect().x - player.rect().x < 0:
        #         self.flip = False
        #     self.attack()

        # self.attacking = max(0, self.attacking - 1)

        chance = random.random() * 0.001
        if chance < 0.00005 and self.action == 'idle' and self.Air_time < 4:
            self.walk(tilemap)

        super().update(tilemap)

        # if self.attacking:
        #     self.set_action('attack')
        if self.Dir.x != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset=(0, 0)):
        #HITBOX DEBUG
        # ac = pygame.Surface(self.size)
        # pos = (self.rect().x - offset[0] , self.rect().y - offset[1])
        # surf.blit(ac, pos)
        # if self.dbg:
        #     rect = pygame.Rect(self.dbg['pos'][0] * 32 -offset[0], self.dbg['pos'][1] *32 - offset[1], 32, 32)
        #     ac2 = pygame.Surface((32, 32))
        #     surf.blit(ac2, rect)

        # img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.scale, self.animation.IMG().get_height() * self.scale))
        # surf.blit(pygame.transform.flip(img, self.flip, False),(self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))
        img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.scale, self.animation.IMG().get_height() * self.scale))
        img_m15 = pygame.transform.scale(self.assets['weapons/M15'], (self.assets['weapons/M15'].get_width() * 1.5, self.assets['weapons/M15'].get_height() * 1.5))
        rect = self.rect()        
        if self.flip:
            surf.blit(pygame.transform.flip(img, self.flip, False),(self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))
            surf.blit(pygame.transform.flip(img_m15, self.flip, False),(rect.centerx - offset[0] - 50, rect.centery -  offset[1]))
        else:
            surf.blit(pygame.transform.flip(img, self.flip, False),(self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))
            surf.blit(pygame.transform.flip(img_m15, self.flip, False),(rect.centerx - offset[0], rect.centery - offset[1] - 3))



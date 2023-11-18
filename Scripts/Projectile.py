import pygame, math, copy
from Scripts.Assets import Assets
from Scripts.Particles import Smoke_Trail

pygame.mixer.init()

class Projectile:
    def __init__(self, game, type, pos, vel, speed, size, angle, owner = 'player', dame = 10, showtime = 250, scale = 1, explosion = False):
        self.type = type
        self.game = game
        self.pos = list(pos)
        self.vel = vel
        self.speed = speed
        self.angle = angle
        self.dame = dame
        self.img = Assets['bullet' + '/' + self.type]
        self.owner = owner
        self.size = size
        self.alive_time = 2000
        self.timer = pygame.time.get_ticks()
        self.kill = [False]
        self.showtime = showtime
        self.flip = False
        self.scale = scale
        self.explosion = explosion
    
    def update(self):
        self.current_time = pygame.time.get_ticks()
        rad = math.radians(self.angle)
        dy = - math.tan(rad) * self.vel
        self.dir = pygame.Vector2(self.vel, dy)
        if self.dir.magnitude():
            self.dir = pygame.Vector2.normalize(self.dir)

        self.dir *= self.speed
        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]
        self.flip = False
        if self.vel < 0:
            self.flip = True
        self.destroy()
    
    def rect(self):
        return pygame.Rect(self.pos, self.size)

    def destroy(self):
        if self.current_time - self.timer >= self.alive_time:
            self.kill[0] = True

    def render(self, surf, offset = (0,0)):
        if self.current_time - self.timer >= self.showtime:
            # black = pygame.Surface(self.size)
            # rect = pygame.Rect((self.pos[0] - offset[0], self.pos[1] - offset[1]), self.size)
            # surf.blit(black, rect)
            img_1 = pygame.transform.scale(self.img, (self.img.get_width() * self.scale,self.img.get_height() * self.scale))
            img = pygame.transform.rotate(img_1, self.angle)
            img.set_colorkey('black')
            surf.blit(img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class Rocket_ammo(Projectile):
    def __init__(self, game, pos, vel, speed, size, angle, owner='player', dame=10, showtime=250, scale=1):
        super().__init__(game, 'rocket' , pos, vel, speed, size, angle, owner, dame, showtime, scale, explosion=True)
        self.part_check = False
    
    def update(self):
        super().update()
        if not self.part_check:
            self.game.Particles.append(Smoke_Trail(self.game, self.pos, self.dir, 4, 0.5, self.kill, self.size))
            self.part_check = True

class Small_ammo(Projectile):
    def __init__(self, game, pos, vel, speed, size, angle, owner='player', dame=10, showtime=250, scale=1):
        super().__init__(game, 'small', pos, vel, speed, size, angle, owner, dame, showtime, scale)

class Small_Ene_ammo(Projectile):
    def __init__(self, game, pos, vel, speed, size, angle, owner='Ene', dame=10, showtime=250, scale=1):
        super().__init__(game, 'small', pos, vel, speed, size, angle, owner, dame, showtime, scale)

class FireBall(Projectile):
    def __init__(self, game, pos, vel, speed, size, angle, owner='Ene', dame=10, showtime=250, scale=1, explosion=True, offset = (0,0)):
        super().__init__(game,'fireball', pos, vel, speed, size, angle, owner, dame, showtime, scale, explosion)
        self.animation = self.game.assets['bullet/' + self.type].copy()
        self.offset = offset
        self.firesfx = pygame.mixer.Sound('Data/sfx/fire.mp3')
        self.firesfx.set_volume(0.1)
        self.firesfx.play(loops=1)
    
    def update(self):
        super().update()
        self.animation.update()
        if self.kill[0] == True:
            self.firesfx.stop()
    
    def render(self, surf, offset=(0, 0)):
        if self.current_time - self.timer >= self.showtime:
            # black = pygame.Surface(self.size)
            # rect = pygame.Rect((self.pos[0] - offset[0], self.pos[1] - offset[1]), self.size)
            # surf.blit(black, rect)

            img_1 = self.animation.IMG()
            img = pygame.transform.scale(img_1, (img_1.get_width() * self.scale, img_1.get_height() * self.scale))
            img.set_colorkey('black')
            surf.blit(pygame.transform.flip(img, True if self.vel == -1 else False, False), (self.pos[0] + self.offset[0] - offset[0], self.pos[1] + self.offset[1] - offset[1]))

class Soul_bullet(Projectile):
    def __init__(self, game, pos, vel, speed, size, angle, owner='Ene', dame=10, showtime=250, scale=1, explosion=True, offset = (0,0)):
        super().__init__(game,'soul', pos, vel, speed, size, angle, owner, dame, showtime, scale, explosion)
        self.animation = self.game.assets['bullet/' + self.type].copy()
        self.offset = offset
    
    def update(self):
        super().update()
        self.animation.update()
    
    def render(self, surf, offset=(0, 0)):
        if self.current_time - self.timer >= self.showtime:
            # black = pygame.Surface(self.size)
            # rect = pygame.Rect((self.pos[0] - offset[0], self.pos[1] - offset[1]), self.size)
            # surf.blit(black, rect)

            img_1 = self.animation.IMG()
            img = pygame.transform.scale(img_1, (img_1.get_width() * self.scale, img_1.get_height() * self.scale))
            img.set_colorkey('black')
            surf.blit(pygame.transform.flip(img, True if self.vel == -1 else False, False), (self.pos[0] + self.offset[0] - offset[0], self.pos[1] + self.offset[1] - offset[1]))
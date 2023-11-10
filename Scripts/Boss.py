import pygame
import random
import math, copy
from Scripts.Drops import BossDropHandler
from Scripts.Projectile import Soul_bullet, FireBall
from Scripts.Particles import *

# hit_sound = pygame.mixer.Sound('data/sfx/hit.wav')
# hit_sound.set_volume(0.2)

# Dash_sound = pygame.mixer.Sound('data/sfx/dash.wav')
# Dash_sound.set_volume(0.1)

# Fire_sound = pygame.mixer.Sound('data/sfx/fire.mp3')
# Fire_sound.set_volume(0.3)

class Boss:
    def __init__(self, game, pos, type, name, size, Health = 10000, dmg = 50, scale = 1, anim_offset=(0,0)):
        self.name = name
        self.game = game
        self.type = type
        self.health = Health
        self.health_max = Health
        self.size = list(size)
        self.anim_offset = anim_offset
        self.pos = list(pos)
        self.bound = [0,0,0,0]
        self.bound[0] = self.pos[0] + 250
        self.bound[1] = self.pos[0] - 250
        self.bound[2] = self.pos[1] + 250
        self.bound[3] = self.pos[1] - 250
        self.flip = False

        self.action = ''
        self.set_action('idle')

        self.Dir = pygame.math.Vector2()
        self.Dead = False
        self.Dead_2 = False
        self.attack_frame = 0
        self.dmg = dmg

        self.Dest = self.pos.copy()

        self.invs = 1000
        self.hurt_frame = 0

        self.cool_down = 2000
        self.cool_frame = 0

        self.Recover_cooldown = 400
        self.Recover_frame = 0

        self.Death_delay = 2500
        self.Death_frame = 0

        self.now = 0
        self.scale = scale
        self.Player_invs = 1000

        self.Hurt_anim = True
        self.Hurt = False 
        self.flash_frame = 0
        self.flash_delay = 100
    
    def DMG(self, health):
        self.health -= health
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self):
        self.now = pygame.time.get_ticks()
        if self.rect().colliderect(self.game.Player.rect()):
            if self.game.Player.is_dash:
                if self.action != 'death':
                    if self.now - self.hurt_frame >= self.invs:
                        BossDropHandler(self.game, list(self.rect().center))
                        self.game.target = self

                        if self.Hurt_anim:
                            self.set_action('hit')
                        self.hurt_frame = pygame.time.get_ticks()
                        self.Recover_frame = pygame.time.get_ticks()
                        self.DMG(100)
                        self.Hurt = True
                        self.flash_frame = pygame.time.get_ticks()
                        self.game.Particles.append(Blood_explode(self.game, self.rect().center, 5, 0.05, 15))
                        self.game.Particles.append(Shock_waves(self.rect().center, 30, 'white', 5, amounts= 2))
                        # for i in range(100):
                        #     angle = random.random() * math.pi * 2
                        #     Pvel = [ math.cos(angle) * 1, math.sin(angle) * 1]
                        #     self.game.Particles.append(Particles(self.game.assets, 'blood', self.rect().center, velocity= Pvel, frame= random.randint(0, 30)))

        self.pos[0] += self.Dir.x
        self.pos[1] += self.Dir.y

        if self.health <= 0:
            self.Dead_2 = True
            if self.Death_frame == 0:
                self.Death_frame = pygame.time.get_ticks()
            self.set_action('death')
            if self.now - self.Death_frame >= self.Death_delay:
                self.Dead = True

        if self.action == 'hit':
            if self.now - self.Recover_frame >= self.Recover_cooldown:
                self.set_action('idle')

        if abs(int(self.pos[0] - self.Dest[0])) <= 5:
            self.Dir.x = 0
        else:
            self.Dir.x = (self.Dest[0] - self.pos[0]) / 10

        if abs(int(self.pos[1] - self.Dest[1])) <= 5:
            self.Dir.y = 0
        else:
            self.Dir.y = (self.Dest[1] - self.pos[1]) / 10
        
        if self.Dir.x > 0:
            self.flip = False
        elif self.Dir.x < 0:
            self.flip = True
        
        if self.action != 'hit' and self.action != 'death':
            if "attack" not in self.action:
                if self.Dir.x == 0 and self.Dir.y == 0:
                    self.set_action('idle')

        # if self.Dir.x > 0:
        #     self.flip = False
        #     self.Dir.x = max(self.Dir.x - 1, 0)
        # if self.Dir.x < 0:
        #     self.flip = True
        #     self.Dir.x = min(self.Dir.x + 1, 0 )
        # if self.Dir.x == 0:
        #     self.set_action('idle')

        self.animation.update()
    
    def render(self, surf, offset = (0,0)):
        # rect = self.rect()
        # surf_rect = pygame.Surface((rect.width, rect.height))
        # surf.blit(surf_rect, (rect.x - offset[0], rect[1] - offset[1]) )

        img1 = self.animation.IMG()
        img2 = pygame.transform.scale(img1, (img1.get_width() * self.scale, img1.get_height() * self.scale))
        surf.blit(pygame.transform.flip(img2, self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
    
    def rect(self):
        return pygame.Rect(self.pos, self.size)

class Evil_wizard(Boss):
    def __init__(self, game, pos, name, size, Health = 10000, scale = 3, anim_offset = (0, 0)):
        super().__init__(game, pos, 'Evil', name, size, Health, scale=scale, anim_offset=anim_offset)
        self.attack_delay = 2000
        self.attack_frame = 0

        self.Burn_delay = 100
        self.Burn_frame = 0

        self.size_bck = self.size[0]
    def rect(self):
        if self.action == 'attack1':
            if self.flip:
                return pygame.Rect(self.pos[0] - self.size[0] + 80, self.pos[1], self.size[0], self.size[1])
            else:
                return pygame.Rect(self.pos, self.size)
        else:
            return pygame.Rect(self.pos, self.size)
    
    def update(self):
        if self.action == 'attack1':
            self.size[0] = self.size_bck + 120
        else:
            self.size[0] = self.size_bck
        super().update()
        self.Move()
        if self.rect().colliderect(self.game.Player.rect()):
            if self.action == 'attack1':
                if self.now - self.Burn_frame >= self.Burn_delay:
                    # hit_sound.play()
                    if not self.game.Player.is_dash:
                        self.game.Player.DMG(3)
                    self.Burn_frame = pygame.time.get_ticks()
            elif self.action == 'hit' or self.action == 'death':
                pass
            else:
                if self.now -self.attack_frame >= self.Player_invs:
                    # hit_sound.play()
                    self.attack_frame = pygame.time.get_ticks()
                    if not self.game.Player.is_dash:
                        self.game.Player.DMG(self.dmg)
        
        if self.action != 'hit' and self.action != 'death':
            if self.action == 'attack1':
                if self.Dir.x == 0 and self.Dir.y == 0:
                    if self.now - self.attack_frame >= self.attack_delay:
                        self.set_action('idle')
                        self.Hurt = False
        
    def Move(self):
        now = pygame.time.get_ticks()
        if self.action == 'idle':
            if now - self.cool_frame >= self.cool_down:
                self.cool_frame = pygame.time.get_ticks()
                chance = random.randint(0, 100)
                if chance <= 50:
                    self.attack_frame = pygame.time.get_ticks()
                    self.set_action('attack1')
                    # Dash_sound.play()
                    # Fire_sound.play()
                    #X AXIS
                    self.Dest[0] = self.game.Player.pos[0]
                    #Y AXIS
                    self.Dest[1] = self.game.Player.pos[1] - 20
                elif chance <= 85:
                    self.set_action('move')
                    # Dash_sound.play()
                    #X AXIS
                    if self.pos[0] + 200 >= self.bound[0]:
                        self.Dest[0] = self.pos[0] + random.randrange(-200, -50, 10)
                    elif self.pos[0] - 200 <= self.bound[1]:
                        self.Dest[0] = self.pos[0] + random.randrange(50, 200, 10)
                    else:
                        step = random.randrange(-200, 200, 10)
                        if step >= 0 and step < 50:
                            step = 50
                        elif step < 0 and step > -50:
                            step = -50
                        self.Dest[0] = self.pos[0] + step

                    #Y AXIS
                    if self.pos[1] + 100 >= self.bound[2]:
                        self.Dest[1] = self.pos[1] + random.randrange(-100, -50, 10)
                    elif self.pos[1] - 100 <= self.bound[3]:
                        self.Dest[1] = self.pos[1] + random.randrange(50, 100, 10)
                    else:
                        step = random.randrange(-100, 100, 10)
                        if step >= 0 and step < 50:
                            step = 50
                        elif step < 0 and step > -70:
                            step = -70
                        self.Dest[1] = self.pos[1] + step

class Ghost(Boss):
    def __init__(self, game, pos, name, size, Health = 10000, scale = 3, anim_offset = (0, 0)):
        super().__init__(game, pos, 'Ghost', name, size, Health, scale=scale, anim_offset=anim_offset)
        self.attack_delay = 2000
        self.attack_frame = 0

        self.Soul_ball_delay = 1000
        self.Soul_ball_frame = 0
        self.bound[0] = self.pos[0] + 500
        self.bound[1] = self.pos[0] - 500
        self.bound[2] = self.pos[1] + 350
        self.bound[3] = self.pos[1] - 350

        self.charging = False
    
    def update(self):
        super().update()
        self.Move()
        if self.action == 'hit':
            if self.charging:
                self.charging = False
                self.game.Projectile.append(Soul_bullet(self.game, (self.rect().centerx, self.rect().centery -10 ), -1 if self.flip else 1, 8, (40, 30), 0, scale=2, offset= (-60, -80) if not self.flip else (-80, -80), showtime=100))
        
        if self.rect().colliderect(self.game.Player.rect()):
            if self.action == 'hit' or self.action == 'death':
                pass
            else:
                if self.now -self.attack_frame >= self.Player_invs:
                    # hit_sound.play()
                    self.attack_frame = pygame.time.get_ticks()
                    if not self.game.Player.is_dash:
                        self.game.Player.DMG(self.dmg)
        
        if self.action != 'hit' and self.action != 'death':
            if self.action == 'attack1':
                if self.charging:
                    if self.now - self.Soul_ball_frame >= self.Soul_ball_delay:
                        self.game.Projectile.append(Soul_bullet(self.game, (self.rect().centerx, self.rect().centery -30 ), -1 if self.flip else 1, 8, (70, 60), 0, scale=4, offset=(-140, -160) if not self.flip else (-160, -160), showtime=100))
                        self.Soul_ball_frame = pygame.time.get_ticks()
                        self.charging = False
                if self.Dir.x == 0 and self.Dir.y == 0:
                    if self.now - self.attack_frame >= self.attack_delay:
                        self.set_action('idle')
                        self.Hurt = False
        
    def Move(self):
        now = pygame.time.get_ticks()
        if self.action == 'idle':
            if now - self.cool_frame >= self.cool_down:
                self.cool_frame = pygame.time.get_ticks()
                chance = random.randint(0, 100)
                if chance <= 50:
                    self.attack_frame = pygame.time.get_ticks()
                    self.set_action('attack1')
                    self.charging = True
                    # Dash_sound.play()
                    # Fire_sound.play()
                    self.Soul_ball_frame = pygame.time.get_ticks()
                    if self.rect().centery != self.game.Player.rect().centery:
                        self.Dest[1] = self.game.Player.rect().centery - 100
                    
                    flip = self.rect().centerx - self.game.Player.rect().centerx
                    if flip > 0:
                        self.flip = True
                    elif flip < 0:
                        self.flip = False

                elif chance <= 85:
                    self.set_action('move')
                    # Dash_sound.play()
                    #X AXIS
                    if self.pos[0] + 200 >= self.bound[0]:
                        self.Dest[0] = self.pos[0] + random.randrange(-400, -50, 10)
                    elif self.pos[0] - 200 <= self.bound[1]:
                        self.Dest[0] = self.pos[0] + random.randrange(50, 400, 10)
                    else:
                        step = random.randrange(-200, 200, 10)
                        if step >= 0 and step < 50:
                            step = 50
                        elif step < 0 and step > -50:
                            step = -50
                        self.Dest[0] = self.pos[0] + step

                    #Y AXIS
                    if self.pos[1] + 100 >= self.bound[2]:
                        self.Dest[1] = self.pos[1] + random.randrange(-200, -50, 10)
                    elif self.pos[1] - 100 <= self.bound[3]:
                        self.Dest[1] = self.pos[1] + random.randrange(50, 200, 10)
                    else:
                        step = random.randrange(-100, 100, 10)
                        if step >= 0 and step < 50:
                            step = 50
                        elif step < 0 and step > -70:
                            step = -70
                        self.Dest[1] = self.pos[1] + step

class Groudon(Boss):
    def __init__(self, game, pos, name, size, Health=10000, dmg=50, scale=1, anim_offset=(0, 0)):
        super().__init__(game, pos, 'Groudon', name, size, Health, dmg, scale, anim_offset)
        self.attack_delay = 1000
        self.attack_frame = 0

        self.gravity = 2
        self.size_bck = self.size[0]

        self.Hurt_anim = False
        self.Hurt = False

        self.fire_ball_frame = 0
        self.fire_ball_delay = 1200

    def rect(self):
        if self.action == 'attack2' or self.action == 'attack1':
                if not self.flip:
                    return pygame.Rect(self.pos[0] - self.size[0] + 120, self.pos[1], self.size[0], self.size[1])
                else:
                    return pygame.Rect(self.pos, self.size)
        else:
            return pygame.Rect(self.pos, self.size)
    
    def update(self):
        if self.action == 'attack2' or self.action == 'attack1':
            self.size[0] = self.size_bck + 100
        else:
            self.size[0] = self.size_bck

        super().update()
        ##Gravity
        self.gravity = min(self.gravity + 1, 10)
        self.Dir.y = self.gravity
        entity_rect = self.rect()
        for rect in self.game.tilemap.physic_rects_around(self.pos, self.size):
            if entity_rect.colliderect(rect):
                if self.Dir.y > 0:
                    entity_rect.bottom = rect.top
                    self.gravity = 0
                    self.Dir.y = 0
                self.pos[1] = entity_rect.y
        ##FLIP SINCE THIS SPRITE IS INVERTED
        if self.Dir.x > 0:
            self.flip = True
        elif self.Dir.x < 0:
            self.flip = False

        self.move()
        
        #Change the move speed 
        if abs(self.Dest[0] - self.rect().centerx) <= 100:
            self.Dir.x = 0
        else:
            if (self.Dest[0] - self.rect().centerx) < 0:
                self.Dir.x = -2.5
            elif (self.Dest[0] - self.rect().centerx) > 0:
                self.Dir.x = 2.5
        
        if self.rect().colliderect(self.game.Player.rect()):
            if "attack" in self.action:
                if self.now - self.attack_frame >= self.Player_invs:
                    # hit_sound.play()
                    self.attack_frame = pygame.time.get_ticks()
                    if not self.game.Player.is_dash:
                        self.game.Player.DMG(self.dmg)
                        self.game.Particles.append(Blood_explode(self.game, self.game.Player.rect().center, 5, 0.05, 15))
            elif self.action == 'death':
                pass
            else:
              pass
        
        if self.action != 'death':
            if "attack" not in self.action:
                if self.Dir.x == 0:
                    self.set_action('idle')
            elif "attack" in self.action:
                if self.rect().centerx - self.game.Player.rect().centerx > 0:
                    self.flip = False
                elif self.rect().centerx - self.game.Player.rect().centerx < 0:
                    self.flip = True

                if self.action == 'attack3':
                    if self.now - self.fire_ball_frame >= self.fire_ball_delay:
                        self.fire_ball_frame = pygame.time.get_ticks()
                        self.game.Projectile.append(FireBall(self.game, (self.rect().centerx, self.rect().centery -70 ), 1 if self.flip else -1, 8, (130, 120), 0, scale=4, offset=(-140, -160), showtime=100))

                if self.animation.done:
                    self.set_action('idle')
        
    def move(self):
        now = pygame.time.get_ticks()
        if self.action == 'idle':
            if abs(self.rect().centerx - self.game.Player.rect().centerx) <= 150:
                attacks = random.choice(['attack1', 'attack2'])
                self.set_action(attacks)
                self.attack_frame = pygame.time.get_ticks()
            elif now - self.cool_frame >= self.cool_down:
                self.cool_frame = pygame.time.get_ticks()
                chance = random.randint(0, 100)
                if chance <= 30:
                    self.set_action('attack3')
                    self.fire_ball_frame = pygame.time.get_ticks()
                elif chance <= 95:
                    self.set_action('move')
                    self.Dest[0] = self.game.Player.pos[0]
    
    def render(self, surf, offset = (0,0)):
        # rect = self.rect()
        # surf_rect = pygame.Surface((rect.width, rect.height))
        # surf.blit(surf_rect, (rect.x - offset[0], rect[1] - offset[1]) )

        img1 = self.animation.IMG()
        img2 = pygame.transform.scale(img1, (img1.get_width() * self.scale, img1.get_height() * self.scale))
        if not self.Hurt:
            surf.blit(pygame.transform.flip(img2, self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
        else:
            if self.now - self.flash_frame >= self.flash_delay: 
                self.Hurt = False
                self.flash_frame = pygame.time.get_ticks()
            mask = pygame.mask.from_surface(img2)
            Overlay = mask.to_surface(setcolor='white', unsetcolor=(0, 0, 0, 0))
            surf.blit(pygame.transform.flip(Overlay, self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Death(Boss):
    def __init__(self, game, pos, name, size, Health=10000, dmg=50, scale=1, anim_offsetL=(0, 0), anim_offseR=(0, 0) ):
        super().__init__(game, pos, 'Death', name, size, Health, dmg, scale, anim_offsetL)
        self.anim_offsetL = list(anim_offsetL)
        self.anim_offsetR = list(anim_offseR)

        self.attack_delay = 1000
        self.attack_frame = 0

        self.gravity = 2
        self.size_bck = self.size[0]

        self.Hurt_anim = False
        self.Hurt = False

        self.Spell_frame = 0
        self.Spell_delay = 1200

    def rect(self):
        if self.action == "attack1":
            if not self.flip:
                return pygame.Rect(self.pos[0] - self.size[0] + 120, self.pos[1], self.size[0], self.size[1])
            else:
                return pygame.Rect(self.pos, self.size)
        else:
            return pygame.Rect(self.pos, self.size)
    
    def update(self):
        if self.action == "attack1":
            self.size[0] = self.size_bck + 130
        else:
            self.size[0] = self.size_bck

        super().update()
        ##Gravity
        self.gravity = min(self.gravity + 1, 10)
        self.Dir.y = self.gravity
        entity_rect = self.rect()
        for rect in self.game.tilemap.physic_rects_around(self.pos, self.size):
            if entity_rect.colliderect(rect):
                if self.Dir.y > 0:
                    entity_rect.bottom = rect.top
                    self.gravity = 0
                    self.Dir.y = 0
                self.pos[1] = entity_rect.y

        ##FLIP SINCE THIS SPRITE IS INVERTED
        if self.Dir.x > 0:
            self.flip = True
            self.anim_offset = self.anim_offsetR
        elif self.Dir.x < 0:
            self.anim_offset = self.anim_offsetL
            self.flip = False

        self.move()
        
        #Change the move speed 
        if abs(self.Dest[0] - self.rect().centerx) <= 100:
            self.Dir.x = 0
        else:
            if (self.Dest[0] - self.rect().centerx) < 0:
                self.Dir.x = -4.5
            elif (self.Dest[0] - self.rect().centerx) > 0:
                self.Dir.x = 4.5
        
        if self.rect().colliderect(self.game.Player.rect()):
            if "attack" in self.action:
                if self.now - self.attack_frame >= self.Player_invs - 100:
                    # hit_sound.play()
                    self.attack_frame = pygame.time.get_ticks()
                    if not self.game.Player.is_dash:
                        self.game.Player.DMG(self.dmg)
                        self.game.Particles.append(Blood_explode(self.game, self.game.Player.rect().center, 5, 0.05, 15))
            elif self.action == 'death':
                pass
            else:
              pass

        if self.action != 'death':
            if "attack" not in self.action:
                if self.Dir.x == 0:
                    self.set_action('idle')
            elif "attack" in self.action:
                if self.rect().centerx - self.game.Player.rect().centerx > 30:
                    self.flip = False
                    self.anim_offset = copy.deepcopy(self.anim_offsetL)
                    self.anim_offset[0] += 30
                elif self.rect().centerx - self.game.Player.rect().centerx < 0:
                    self.flip = True
                    self.anim_offset = self.anim_offsetR

                if self.action == 'attack2':
                    if self.now - self.Spell_frame >= self.Spell_delay:
                        self.Spell_frame = pygame.time.get_ticks()
                        self.game.Particles.append(Dark_spell(self.game, (60, 30), self.game.Player.rect(), 30))

                if self.animation.done:
                    self.set_action('idle')
    def move(self):
        now = pygame.time.get_ticks()
        if self.action == 'idle':
            if abs(self.rect().centerx - self.game.Player.rect().centerx) <= 150:
                self.set_action('attack1')
                self.attack_frame = pygame.time.get_ticks()
            if now - self.cool_frame >= self.cool_down:
                self.cool_frame = pygame.time.get_ticks()
                chance = random.randint(0, 100)
                if chance <= 30:
                    self.set_action('attack2')
                    self.Spell_frame = pygame.time.get_ticks()
                elif chance <= 90:
                    self.set_action('move')
                    self.Dest[0] = self.game.Player.pos[0]
    
    def render(self, surf, offset = (0,0)):
        # rect = self.rect()
        # surf_rect = pygame.Surface((rect.width, rect.height))
        # surf.blit(surf_rect, (rect.x - offset[0], rect[1] - offset[1]) )

        img1 = self.animation.IMG()
        img2 = pygame.transform.scale(img1, (img1.get_width() * self.scale, img1.get_height() * self.scale))
        if not self.Hurt:
            surf.blit(pygame.transform.flip(img2, self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
        else:
            if self.now - self.flash_frame >= self.flash_delay: 
                self.Hurt = False
                self.flash_frame = pygame.time.get_ticks()
            mask = pygame.mask.from_surface(img2)
            Overlay = mask.to_surface(setcolor='white', unsetcolor=(0, 0, 0, 0))
            surf.blit(pygame.transform.flip(Overlay, self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
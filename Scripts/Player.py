import pygame
from Scripts.Entities import PhysicsEntity

class Player(PhysicsEntity):
    def __init__(self, e_type, pos, size, assets, Health = 400, speed = 2, size_mul = 1, animoffset = (-3, -3)):
        super().__init__(e_type, pos, size, assets, Health, speed= speed)
        self.size_mul = size_mul
        self.animations_offset = list(animoffset)
        self.Air_time = 0
        self.Wall_slide = False
        self.reload_time = 800
        self.reloading = 0
        self.Walljump = False
        self.spped_bck = speed
        self.invs = 1000
        self.is_dash = False
        self.is_shield = False
        self.is_attack = False
        self.att_consecutive = 0
        
        #TIMER
        self.dash_timer = pygame.time.get_ticks()
        self.dash_delay = 2000
        self.att_timer = pygame.time.get_ticks()
        self.att_delay = 700
    
    def Movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.Dir.x = -1
        elif keys[pygame.K_d]:
            self.Dir.x = 1
        else:
            self.Dir.x = 0
        
        if keys[pygame.K_LSHIFT]:
            self.dash()
        if keys[pygame.K_j]:
            self.attack()

        if keys[pygame.K_w]:
            self.jump()
        elif keys[pygame.K_s]:
            self.Dir.y = 1
            self.shield()
        else:
            self.Dir.y = 0
            self.speed = self.spped_bck
            self.is_shield = False

    def jump(self):
        if self.jumps:
            self.Vel.y = -1 * 3
            self.jumps -= 1
        if self.Coll['right'] or self.Coll['left']:
            self.Walljump = True

    def dash(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.dash_timer >= self.dash_delay:
            if not self.Wall_slide and not self.is_shield:
                if self.flip:
                    self.dash_timer = pygame.time.get_ticks()
                    self.Vel.x = -5
                    self.is_dash = True
                else:
                    self.dash_timer = pygame.time.get_ticks()
                    self.Vel.x = 5
                    self.is_dash = True

    def shield(self):
        # if not self.is_dash and self.Air_time < 4 and self.Dir.x == 0:
        #     self.is_shield = True
        if self.Air_time < 4:
            self.is_shield = True
            self.Dir.x = 0
            self.speed = 0
            self.Vel.x = 0

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.att_timer >= self.att_delay:
            self.att_timer = pygame.time.get_ticks()
            temp = 'attack' + str(self.att_consecutive)
            self.is_attack = True
            self.att_consecutive = (self.att_consecutive + 1) % 2
            self.set_action(temp)

    def update(self, tilemap):
        super().update(tilemap)
        current_time = pygame.time.get_ticks()
        if current_time - self.att_timer >= self.att_delay:
            self.is_attack = False
        
        self.Walljump = False
        self.Movement()
        self.Air_time += 1

        if self.Vel.x == 0:
            self.is_dash = False
        
        if self.Coll['bottom']:
            self.Air_time = 0

        self.Wall_slide = False
        if self.Coll['right'] or self.Coll['left']:
            if self.Air_time > 4:
                self.Wall_slide = True
                self.is_dash = False
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

        if not self.Wall_slide and not self.is_attack:
            if self.is_dash:
                self.set_action('dash')
            elif self.Air_time > 65:
                self.set_action('fall')
            elif self.Air_time > 4:
                self.set_action('jump')
            elif self.is_shield:
                self.set_action('shield')
            elif self.Dir.x != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
    
    def render(self, surf, offset = (0,0)):
       #HITBOX DEBUG
    #    ac = pygame.Surface(self.size)
    #    pos = (self.rect().x - offset[0] , self.rect().y - offset[1])
    #    surf.blit(ac, pos)

       img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.size_mul , self.animation.IMG().get_height() * self.size_mul))
       surf.blit(pygame.transform.flip(img, self.flip, False), (self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))
    

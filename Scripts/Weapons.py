import pygame, math, copy
from Scripts.Assets import Assets
from Scripts.Projectile import *

class Weapon:
    def __init__(self, type, size, pos, pivot, projectile, dame = 100, scale = 1, offsetL = (0,0), offsetR = (0,0), delay = 500, ammo = 50):
        self.type = type
        self.pos = pos
        self.size = size
        self.pivot = pivot
        self.dame = dame
        self.scale = scale
        self.offsetL = offsetL
        self.offsetR = offsetR
        self.offset = (0,0)
        self.action = ''
        self.set_action('idle')
        self.angle = 0
        self.delay = delay
        self.timer= 0
        self.ammo = ammo
        self.projectile = projectile
        self.flip = 1

    def rect(self):
        return pygame.Rect(self.pos, self.size)
    
    def attack(self, game):
        pass
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = Assets[self.type + '/' + self.action].copy()
 
    def rotate(self, player):
        origin = [self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]]
        img_org = self.animation.IMG()
        img = pygame.transform.scale(img_org, (img_org.get_width() * self.scale, img_org.get_height() * self.scale))
        image_rect = img.get_rect(topleft = (origin[0] - self.pivot[0], origin[1] - self.pivot[1]))
        offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(- (self.angle))
        rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
        if player.flip:
            img = pygame.transform.flip(img,  False, True)
        rotated_image = pygame.transform.rotate(img, self.angle).convert_alpha()
        rotated_image_rect = rotated_image.get_rect(center = (rotated_image_center[0], rotated_image_center[1]))
        return rotated_image, rotated_image_rect
    
    def update(self, offset, player):
        pos = copy.copy(self.pos)
        pos[0] += self.offset[0]
        pos[1] += self.offset[1]
        mouse_pos = pygame.mouse.get_pos()
        dy = round(mouse_pos[1] + offset[1] - pos[1],1)
        dx = round(mouse_pos[0] + offset[0] - pos[0],1)
        rads = math.atan2(-dy, dx)
        rads %= 2*math.pi
        degs = round(math.degrees(rads))
        self.angle = degs
        self.flip = 1
        if self.angle > 90 and self.angle < 270:
            self.flip = -1
        if player.flip:
            self.offset = self.offsetL
        else:
            self.offset = self.offsetR
        self.animation.update()

    def render(self, surf, player, offset= (0,0)):
        if not player.is_dash and not player.Wall_slide:
            rotate_img, rotated_image_rect = self.rotate(player)
            surf.blit(rotate_img, (rotated_image_rect.x - offset[0], rotated_image_rect.y - offset[1]))

    def addBullets(self, amount):
        self.ammo += amount

class Pistol(Weapon):
    def __init__(self, size, pos, pivot, projectile,  dame= 50, scale=1, offsetL=(0, 0), offsetR=(0, 0), delay= 1000, ammo=50):
        super().__init__('pistol', size, pos, pivot, projectile, dame, scale, offsetL, offsetR, delay, ammo)
    
    def update(self, offset, player):
        super().update(offset, player)
        if self.action == 'shoot' and self.animation.done:
            self.set_action('idle')
    
    def attack(self, game):
        if self.ammo:
            if not game.Player.is_dash and not game.Player.Wall_slide:
                current = pygame.time.get_ticks()
                if current - self.timer >= self.delay:
                    self.set_action('shoot')
                    self.projectile.append(Small_ammo(game, (game.Player.rect().centerx ,game.Player.rect().centery - 15), self.flip, 8, (15, 10), self.angle, dame = self.dame, showtime= 100))
                    self.ammo -= 1
                    self.timer = pygame.time.get_ticks()
class Rifle(Weapon):
    def __init__(self, size, pos, pivot, projectile,  dame = 20, scale=1, offsetL=(0, 0), offsetR=(0, 0), delay= 400, ammo=50):
        super().__init__('rifle', size, pos, pivot, projectile, dame, scale, offsetL, offsetR, delay, ammo)
    
    def update(self, offset, player):
        super().update(offset, player)
        if self.action == 'shoot' and self.animation.done:
            self.set_action('idle')
    
    def attack(self, game):
        if self.ammo:
            if not game.Player.is_dash and not game.Player.Wall_slide:
                current = pygame.time.get_ticks()
                if current - self.timer >= self.delay:
                    self.set_action('shoot')
                    self.projectile.append(Small_ammo(game, (game.Player.rect().centerx,game.Player.rect().centery - 10 ), self.flip, 8, (15, 10), self.angle, dame = self.dame, showtime= 150))
                    self.ammo -= 1
                    self.timer = pygame.time.get_ticks()

class Launcher(Weapon):
    def __init__(self, size, pos, pivot, projectile,  dame = 500, scale=1, offsetL=(0, 0), offsetR=(0, 0), delay= 1500, ammo=50):
        super().__init__('launcher', size, pos, pivot, projectile, dame, scale, offsetL, offsetR, delay, ammo)
    
    def update(self, offset, player):
        super().update(offset, player)
        if self.action == 'shoot' and self.animation.done:
            self.set_action('idle')
    
    def attack(self, game):
        if self.ammo:
            if not game.Player.is_dash and not game.Player.Wall_slide:
                current = pygame.time.get_ticks()
                if current - self.timer >= self.delay:
                    self.set_action('shoot')
                    self.projectile.append(Rocket_ammo(game, (game.Player.rect().centerx - 5,game.Player.rect().centery - 10), self.flip, 8, (20, 12), self.angle, dame = self.dame, showtime= 120, scale=0.4))
                    self.ammo -= 1
                    self.timer = pygame.time.get_ticks()

class Wep_Ene:
    def __init__(self, type, Loffset = (0,0), Roffset=(0,0), scale = 1, delay = 1000, dame = 10):
        self.type = type
        self.action = ''
        self.Loffset = Loffset
        self.Roffset = Roffset
        self.set_action('idle')
        self.scale = scale
        self.dame = dame
        self.delay = delay
        self.timer = pygame.time.get_ticks()
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = Assets[self.type + '/' + self.action].copy()
    
    def attack(self, game, ene):
        current = pygame.time.get_ticks()
        if current - self.timer >= self.delay:
            self.timer = pygame.time.get_ticks()
            self.set_action('shoot')
            game.Projectile.append(Small_Ene_ammo(game, (ene.rect().centerx, ene.rect().centery), -1 if ene.flip else 1, 8, (15, 10), 0, dame = self.dame, showtime= 100))

    def update(self, rect, flip):
        if flip:
            self.pos = [rect.centerx - self.Loffset[0], rect.centery -self.Loffset[1]]
        else:
            self.pos = [rect.centerx - self.Roffset[0], rect.centery -self.Roffset[1]]

        if self.action == 'shoot':
            if self.animation.done:
                self.set_action('idle')
        self.animation.update()

    def render(self, surf, flip, offset=(0,0)):
        img = self.animation.IMG()
        img2 = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        surf.blit(pygame.transform.flip(img2, flip, False),(self.pos[0] - offset[0], self.pos[1] -  offset[1]))
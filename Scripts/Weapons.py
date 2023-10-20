import pygame, math, copy
from Scripts.Assets import Assets

class Weapon:
    def __init__(self, type, size, pos, pivot, dame = 100, scale = 1, offsetL = (0,0), offsetR = (0,0), delay = 500, ammo = 50):
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

    def rect(self):
        return pygame.Rect(self.pos, self.size)
    
    def attack(self):
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
        if player.flip:
            self.offset = self.offsetL
        else:
            self.offset = self.offsetR
        self.animation.update()

    def render(self, surf, player, offset= (0,0)):
        if not player.is_dash and not player.Wall_slide:
            rotate_img, rotated_image_rect = self.rotate(player)
            surf.blit(rotate_img, (rotated_image_rect.x - offset[0], rotated_image_rect.y - offset[1]))

class Pistol(Weapon):
    def __init__(self, size, pos, pivot, dame=100, scale=1, offsetL=(0, 0), offsetR=(0, 0), delay=500, ammo=50):
        super().__init__('pistol', size, pos, pivot, dame, scale, offsetL, offsetR, delay, ammo)
    
    def update(self, offset, player):
        super().update(offset, player)
        if self.action == 'shoot' and self.animation.done:
            self.set_action('idle')
    
    def attack(self):
        current = pygame.time.get_ticks()
        if current - self.timer >= self.delay:
            self.set_action('shoot')
            self.timer = pygame.time.get_ticks()

class Rifle(Weapon):
    def __init__(self, size, pos, pivot, dame=100, scale=1, offsetL=(0, 0), offsetR=(0, 0), delay=500, ammo=50):
        super().__init__('rifle', size, pos, pivot, dame, scale, offsetL, offsetR, delay, ammo)
    
    def update(self, offset, player):
        super().update(offset, player)
        if self.action == 'shoot' and self.animation.done:
            self.set_action('idle')
    
    def attack(self):
        current = pygame.time.get_ticks()
        if current - self.timer >= self.delay:
            self.set_action('shoot')
            self.timer = pygame.time.get_ticks()


import pygame

class PhysicsEntity():
    def __init__(self, e_type ,pos, size, assets, Health = 100, speed = 1.5):
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.assets = assets
        self.Vel = pygame.math.Vector2()
        self.Dir = pygame.math.Vector2()
        self.Coll = {'left': False, 'right': False, "top": False, 'bottom': False}
        self.speed = speed

        self.action = ''
        self.animations_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

        self.jumps = 1

        self.Dead = False
        self.Health = Health
        self.Max_Health = Health
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def DMG(self ,dmg):
        self.Health -= dmg
        if self.Health <= 0:
            self.Dead = True
    
    def FALL_DEAD(self):
        if self.pos[1] > 736 + 320:
            self.Dead = True
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap):     
            
        self.Coll = {'left': False, 'right': False, "top": False, 'bottom': False}
        frame_movement = self.Vel  +  self.Dir
        self.pos[0] += frame_movement.x * self.speed
        entity_rect = self.rect()
        for rect in tilemap.physic_rects_around(self.pos, self.size):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.Coll['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.Coll['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement.y
        entity_rect = self.rect()
        for rect in tilemap.physic_rects_around(self.pos, self.size):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.Coll['bottom'] = True
                    self.jumps = 1
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.Coll['top'] = True
                self.pos[1] = entity_rect.y

        if self.Dir.x > 0:
            self.flip = False
        elif self.Dir.x < 0:
            self.flip = True
    
        self.Vel.y = min(5, self.Vel.y + 0.1)
        if self.Coll['bottom'] or self.Coll['top']:
            self.Vel.y = 0

        if self.Vel.x < 0:
            self.Vel.x = min(self.Vel.x + 0.1, 0)
        else:
            self.Vel.x = max(self.Vel.x - 0.1, 0)

        self.animation.update()
        self.FALL_DEAD()

    def render(self, surf, offset = (0,0)):
        surf.blit(pygame.transform.flip(self.animation.IMG(), self.flip, False), (self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))
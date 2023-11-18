from Scripts.Assets import *
import random, math, copy

pygame.mixer.init()
class Leaf:
    def __init__(self, assets, pos, velocity=[0, 0], frame=0, scale = 2):
        self.assets = assets
        self.type = 'leaf'
        self.pos = list(pos)
        self.Vel = list(velocity)
        self.animation = self.assets['Particles' + '/' + self.type].copy()
        self.animation.frame = frame
        self.scale = scale

    def update(self):
        kill = False
        if self.animation.done:
            kill = True

        self.pos[0] += self.Vel[0]
        self.pos[1] += self.Vel[1]

        self.animation.update()

        return kill

    def render(self, surf, offset=(0, 0)):
        img = self.animation.IMG()
        image = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        image.set_colorkey(0, 0)
        surf.blit(image, (self.pos[0] - offset[0] - img.get_width() //
                  2, self.pos[1] - offset[1] - img.get_height() // 2))

class Leafs:
    def __init__(self, game, leaf_spawner):
        self.type = 'leaf'
        self.leaf_spawner = leaf_spawner
        self.game = game
        self.amounts = 0
        self.leafs = []
    
    def update(self):
       # Particles leaf random
        for rect in self.leaf_spawner:
            if random.random() * 15000 < rect.width * rect.height:
                pos = (rect.x + random.random() * (rect.width + 64), rect.y + random.random() * (rect.height + 64))
                self.leafs.append(Leaf(self.game.assets, pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
        
        for leaf in self.leafs.copy():
                kill = leaf.update()
                leaf.pos[0] += math.sin(leaf.animation.frame * (math.pi / 360)) * 0.3
                if kill:
                    self.leafs.remove(leaf)
        return False

    def render(self, display, offset=(0,0)):
        for leaf in self.leafs:
            leaf.render(display, offset)

class Smoke_Part:
    def __init__(self, game, pos, size, vel, decay_rate, speed):
        self.game = game
        self.pos = list(pos)
        self.size = size
        vec2 = pygame.Vector2(list(vel))
        self.vel = vec2
        if vec2.magnitude():
            self.vel = vec2.normalize()
        self.speed = speed
        self.decay = decay_rate
        self.done = False
        self.color = [255,255,255]
    
    def rect(self):
        surf = pygame.Surface((self.size, self.size))
        return surf.get_rect(center = self.pos)
    
    def update(self):
        self.pos[0] += self.vel[0] * self.speed
        entity_rect = self.rect()
        for rect in self.game.tilemap.physic_rects_around(self.pos, (3, 3)):
            if entity_rect.colliderect(rect):
                if self.vel[0] > 0:
                    entity_rect.right = rect.left
                elif self.vel[0] < 0:
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x
                self.vel[0] *= -1
                break

        self.pos[1] += self.vel[1] * self.speed
        entity_rect = self.rect()
        for rect in self.game.tilemap.physic_rects_around(self.pos, (3, 3)):
            if entity_rect.colliderect(rect):
                if self.vel[1] > 0:
                    entity_rect.bottom = rect.top
                elif self.vel[1] < 0:
                    entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y
                self.vel[1] *= -1
                break

        self.size -= self.decay
        if self.size < 0:
            self.done = True
        
        self.speed += 0.01
        if self.color[0] > 120:
            self.color[0] -= 3.1
        if self.color[1] > 120:
            self.color[1] -= 3.2
        if self.color[2] > 120:
            self.color[2] -= 3

    
    def render(self, surf, offset):
        pygame.draw.circle(surf, self.color, (self.pos[0] - offset[0], self.pos[1] - offset[1]), self.size)

class Smoke_explode:
    def __init__(self, game, pos, speed, decay_rate, amounts):
        self.type = 'smoke'
        self.game = game
        self.pos = list(pos)
        self.speed = speed
        self.decay = decay_rate
        self.amounts = amounts
        self.count = 0
        self.parts = []
        self.done = False
    
    def update(self):
        if self.count <= self.amounts:
            pos = copy.deepcopy(self.pos)
            self.parts.append(Smoke_Part(self.game, pos, random.randint(50, 71), (random.randint(-10, 10)/10, random.randint(-10, 10)/10), self.decay, random.randint(1,self.speed)))
            self.count +=1

        for i in self.parts.copy():
            i.update()
            if i.done:
                self.parts.remove(i)

        count2 =  len(self.parts)
        if count2 == 0 and self.count >= self.amounts:
            self.done = True
            return True
        return False
    
    def render(self, surf, offset):
        for i in sorted(self.parts, key= lambda i:i.size):
            i.render(surf, offset)

class Smoke_Trail:
    def __init__(self, game, pos, Vel, speed, decay_rate, kill, obj_size):
        self.type = 'smoke'
        self.game = game
        self.pos = pos
        self.speed = speed
        self.vel = list(Vel)
        self.decay = decay_rate
        self.kill = kill
        self.amounts = 0
        self.parts = []
        self.done = False
        self.obj_size = obj_size

    def update(self):
        if not self.kill[0]:
            pos = list(copy.deepcopy(self.pos))
            pos[0] += self.obj_size[0]/2
            pos[1] += self.obj_size[1]/2 + 7
            self.parts.append(Smoke_Part(self.game, pos, random.randint(2, 5), (-self.vel[0], random.randint(-10, 10)/10), self.decay, random.randint(1, self.speed)))

        for i in self.parts.copy():
            i.update()
            if i.done:
                self.parts.remove(i)

        if self.kill[0]:
            self.done = True
            return True
        return False
    
    def render(self, surf, offset):
        for i in sorted(self.parts, key= lambda i:i.size):
            i.render(surf, offset)

class Blode_Part:
    def __init__(self, game, pos, size, vel , decay_rate, speed):
        self.game = game
        self.pos = pos
        self.size = size
        vec2 = pygame.Vector2(list(vel))
        self.vel = vec2
        if vec2.magnitude():
            self.vel = vec2.normalize()
        self.decay = decay_rate
        self.speed = speed
        self.gravity = 7
        self.done = False
        self.color = [255, 0, 0]
    
    def update(self):
        self.gravity = min(self.gravity + 0.2, 10)
        self.speed = max(self.speed - 0.2, 0)
        self.pos[0] += -self.vel[0] * self.speed
        entity_rect = self.rect()
        for rect in self.game.tilemap.physic_rects_around(self.pos, (3, 3)):
            if entity_rect.colliderect(rect):
                if self.vel[0] > 0:
                    entity_rect.left = rect.right
                elif self.vel[0] < 0:
                    entity_rect.right = rect.left
                self.pos[0] = entity_rect.x
                self.speed = 0
                break

        self.pos[1] += self.vel[1] * self.gravity
        entity_rect = self.rect()
        for rect in self.game.tilemap.physic_rects_around(self.pos, (3, 3)):
            if entity_rect.colliderect(rect):
                if self.vel[1] > 0:
                    entity_rect.bottom = rect.top
                self.pos[1] = entity_rect.y
                self.gravity = 0
                break

        if self.vel.y <= 0:
            self.vel.y += 0.5

        self.size -= self.decay
        if self.size < 0:
            self.done = True
        self.color_change((102, 0, 0), 50)
             
    def color_change(self, target_color, speed):
        if self.color[0] != target_color[0]:
            self.color[0] += (target_color[0] - self.color[0])/speed
        if self.color[1] != target_color[1]:
            self.color[1] += (target_color[1] - self.color[1])/speed
        if self.color[2] != target_color[2]:
            self.color[2] += (target_color[2] - self.color[2])/speed

    def rect(self):
        surf = pygame.Surface((self.size, self.size))
        return surf.get_rect(center = self.pos)

    def render(self, surf, offset):
        pygame.draw.circle(surf, self.color, (self.pos[0] - offset[0], self.pos[1] - offset[1]), self.size)

class Blood_spill:
    def __init__(self, game, pos, vel, speed, decay_rate, amounts):
        self.type = 'blood'
        self.game = game
        self.pos = list(pos)
        self.vel = vel
        self.decay = decay_rate
        self.speed = speed
        self.amounts = amounts
        self.done = False
        self.count = 0
        self.parts = []
    
    def update(self):
        if self.count <= self.amounts:
            pos = copy.deepcopy(self.pos)
            self.parts.append(Blode_Part(self.game, pos, random.randint(5, 8), (self.vel[0], self.vel[1] + random.randint(-10, 10)), self.decay, random.randint(1, self.speed)))
            self.count += 1
        
        for i in self.parts.copy():
            i.update()
            if i.done:
                self.parts.remove(i)
    
        count2 =  len(self.parts)
        if count2 == 0 and self.count >= self.amounts:
            self.done = True
            return True
        return False
    
    def render(self, surf, offset):
        for i in sorted(self.parts, key= lambda i:i.size):
            i.render(surf, offset)

class Blood_explode:
    def __init__(self, game, pos, speed, decay_rate, amounts):
        self.type = 'blood'
        self.game = game
        self.pos = list(pos)
        self.decay = decay_rate
        self.speed = speed
        self.amounts = amounts
        self.done = False
        self.count = 0
        self.parts = []
    
    def update(self):
        while self.count <= self.amounts:
            pos = copy.deepcopy(self.pos)
            self.parts.append(Blode_Part(self.game, pos, random.randint(5, 8), (random.randint(-10, 10)/10, random.randint(-10, 10)/10), self.decay, random.randint(1, self.speed)))
            self.count += 1
        
        for i in self.parts.copy():
            i.update()
            if i.done:
                self.parts.remove(i)
    
        count2 =  len(self.parts)
        if count2 == 0:
            self.done = True
            return True
        return False
    
    def render(self, surf, offset):
        for i in sorted(self.parts, key= lambda i:i.size):
            i.render(surf, offset)

class Earth_coll:
    def __init__(self, game, pos, size, scale = 1, flip = False):
        self.game = game
        self.pos = pos
        self.action = ''
        self.set_action('earthwall')
        self.done = False
        self.size = size
        self.rect2 = self.rect()
        self.scale = scale
        self.flip = flip
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets['Particles/' + self.action].copy()
    
    def update(self):
        self.animation.update()
        if self.animation.done:
            self.done = True
    
    def rect(self):
        surf = pygame.Surface(self.size)
        return surf.get_rect(midbottom = self.pos)

    def render(self, surf, offset):
        img = self.animation.IMG()
        img2 = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        surf.blit(pygame.transform.flip(img2, self.flip, False), (self.rect2.x - offset[0] - 40, self.rect2.y - offset[1]))
        # surf2 = pygame.Surface(self.size)
        # surf.blit(surf2, (self.rect2.x - offset[0], self.rect2.y - offset[1]))

class Earth_Cols:
    def __init__(self, game, size, rect, vel, amounts):
        self.type = 'earth'
        self.game = game
        self.rect = rect
        self.size = size
        self.vel = vel
        self.amounts = amounts
        self.count = 0
        self.parts = []
        self.done = False
        self.hit = False
        earthsfx = pygame.mixer.Sound('Data/sfx/Earth.wav')
        earthsfx.set_volume(0.1)
        earthsfx.play()
    
    def update(self):
        if self.count <= self.amounts:
            loco = list(self.rect.midbottom)
            loco[0] += self.count * self.size[0] * self.vel
            self.parts.append(Earth_coll(self.game, loco, self.size, scale=2, flip= True if self.vel < 0 else False))
            self.count += 1

        for i in self.parts.copy():
            i.update()
            if i.done:
                self.parts.remove(i)

            if not self.hit:
                if i.rect().colliderect(self.game.Player.rect()):
                    if not self.game.Player.is_dash:
                        self.game.Player.DMG(40)
                        self.game.Particles.append(Blood_explode(self.game, self.game.Player.rect().center, 5, 0.05, 15))
                    self.hit = True
    
        count2 =  len(self.parts)
        if count2 == 0:
            self.done = True
            return True
        return False
    
    def render(self, surf, offset):
        for i in self.parts:
            i.render(surf, offset)

class Dark_spell:
    def __init__(self, game, size, obj_rect, amounts):
        self.type = 'D_Spell'
        self.game = game
        self.obj_rect = obj_rect
        self.size = list(size)
        self.action = ''
        self.set_action('D_spell')
        self.scale = 2.5

        self.amounts = amounts
        self.done = False
        self.hit_frame = 0
        self.hit_delay = 800
        self.speed = 7
        
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets['Particles/' + self.action].copy()
    
    def rect(self):
        pos = list(self.obj_rect.midtop)
        pos[1] -= 60
        pos[0] -= self.obj_rect.width / 2 
        return pygame.Rect(pos, self.size)

    def update(self):
        now = pygame.time.get_ticks()
        self.animation.update()
        self.size[1] += self.speed
        self.speed = max(self.speed - 0.5, 0.5)

        
        if self.rect().colliderect(self.game.Player.rect()):
            if now - self.hit_frame >= self.hit_delay:
                if not self.game.Player.is_dash:
                    self.game.Player.DMG(20)
                    self.game.Particles.append(Blood_explode(self.game, self.game.Player.rect().center, 5, 0.05, 15))
                self.hit_frame = pygame.time.get_ticks()
    
        if self.animation.done:
            self.done = True
            return True
        return False
    
    def render(self, surf, offset):
        # surf2 = pygame.Surface(self.size)
        # surf.blit(surf2, (self.rect().x - offset[0], self.rect().y - offset[1]))

        img = self.animation.IMG()
        img2 = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        surf.blit(img2, (self.rect().x - offset[0] - 130, self.rect().y - offset[1] - 105))

class Laser_line:
    def __init__(self, game, height, rect, vel, amounts, offset = (0,0)):
        self.type = 'laser'
        self.game = game
        self.rect = rect
        self.height = height
        self.vel = vel
        self.amounts = amounts
        self.count = self.amounts
        self.offset = offset
        self.done = False
        self.hit = False
        lasersfx = pygame.mixer.Sound('Data/sfx/laser.wav')
        lasersfx.set_volume(0.1)
        lasersfx.play()
    
    def update(self):
            width = 32 * self.count
            self.surf = pygame.Surface((width, self.height), pygame.SRCALPHA)
            if self.vel < 0:
                self.rect2 = self.surf.get_rect(midright = (self.rect.centerx + self.offset[0], self.rect.centery + self.offset[1]))
            else:
                self.rect2 = self.surf.get_rect(midleft = (self.rect.centerx + self.offset[0], self.rect.centery + self.offset[1]))

            if not self.hit:
                if self.rect2.colliderect(self.game.Player.rect()):
                    self.game.Player.DMG(80)
                    self.game.Particles.append(Blood_explode(self.game, self.game.Player.rect().center, 5, 0.05, 15))
                    self.hit = True

            if self.count <= 0:
                self.done = True
                return True
            self.count -= 0.5
            return False
    
    def render(self, surf, offset):
        if self.count % 2 != 0:
            width = 32 * (self.count - 0.8)
            if width < 0:
                width = 0
            surf2 = pygame.Surface((width, self.height))
            surf2.fill('purple')
            if self.vel < 0:
                rect1 = self.surf.get_rect()
                rect2 = surf2.get_rect(left = rect1.left)
            elif self.vel > 0:
                rect1 = self.surf.get_rect()
                rect2 = surf2.get_rect(right = rect1.right)
            self.surf.blit(surf2, rect2)
            surf.blit(self.surf, (self.rect2.x - offset[0], self.rect2.y - offset[1]))

class Dirt_part:
    def __init__(self, game, pos, size, vel, decay_rate, speed, color1, color2):
        self.game = game
        self.pos = list(pos)
        self.size = size
        vec2 = pygame.Vector2(list(vel))
        self.vel = vec2
        if vec2.magnitude():
            self.vel = vec2.normalize()
        self.decay = decay_rate
        self.speed = speed
        self.gravity = 7
        self.done = False
        self.color1 = color1
        self.color2 = color2

    def update(self):
        self.gravity = min(self.gravity + 0.2, 10)
        self.speed = max(self.speed - 0.2, 0)
        self.pos[0] += -self.vel[0] * self.speed
        self.pos[1] += self.vel[1] * self.gravity
        entity_rect = self.rect()
        for rect in self.game.tilemap.physic_rects_around(self.pos, (3, 3)):
            if entity_rect.colliderect(rect):
                if self.vel[1] > 0:
                    entity_rect.bottom = rect.top
                self.pos[1] = entity_rect.y
                self.gravity = 0
                break

        if self.vel.y <= 0:
            self.vel.y += 0.5

        self.size -= self.decay
        if self.size < 0:
            self.done = True
        self.color_change(self.color2, 5)
             
    def color_change(self, target_color, speed):
        if self.color1[0] != target_color[0]:
            self.color1[0] += (target_color[0] - self.color1[0])/speed
        if self.color1[1] != target_color[1]:
            self.color1[1] += (target_color[1] - self.color1[1])/speed
        if self.color1[2] != target_color[2]:
            self.color1[2] += (target_color[2] - self.color1[2])/speed

    def rect(self):
        surf = pygame.Surface((self.size, self.size))
        return surf.get_rect(center = self.pos)

    def render(self, surf, offset):
        pygame.draw.circle(surf, self.color1, (self.pos[0] - offset[0], self.pos[1] - offset[1]), self.size)

class Dirt_Splater:
    def __init__(self, game, size, rect, vel, amounts, decay, speed, color1 = [86,43,0], color2 = [86,43,0], offset=(0,0)):
        self.type = 'dirt'
        self.game = game
        self.rect = rect
        self.size = size
        self.vel = vel
        self.amounts = amounts
        self.decay = decay
        self.speed = speed
        self.count = 0
        self.parts = []
        self.done = False
        self.offset = offset
        self.color1 = list(color1)
        self.color2 = list(color2)
    
    def update(self):
        if self.count <= self.amounts:
            if self.vel < 0:
                loco = (self.rect.midleft[0] + self.offset[0], self.rect.midleft[1] + self.offset[1])
            elif self.vel > 0:
                loco = (self.rect.midright[0] + self.offset[0], self.rect.midright[1] + self.offset[1])
            vel = [self.vel, random.randint(-10, 10)/10]
            self.parts.append(Dirt_part(self.game, loco, random.randint(2, self.size), vel, self.decay, random.randint(5, self.speed), self.color1, self.color2))
            self.count += 1

        for i in self.parts.copy():
            i.update()
            if i.done:
                self.parts.remove(i)
    
        count2 =  len(self.parts)
        if count2 == 0:
            self.done = True
            return True
        return False
    
    def render(self, surf, offset):
        for i in self.parts:
            i.render(surf, offset)

class Shock_wave:
    def __init__(self, pos, size, color, decay_rate):
        self.pos = pos
        self.color = color
        self.decay_rate = decay_rate
        self.size = size
        self.alpha = 255
        self.done = False
    
    def update(self):
        self.alpha -= self.decay_rate
        self.size += 5
        if self.alpha < 0:
            self.done = True
    
    def render(self, surf, offset):
        img2 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        rect = img2.get_rect()
        pygame.draw.circle(img2, self.color, rect.center, self.size/2, 5)
        img2.set_alpha(self.alpha)
        rect = img2.get_rect(center = self.pos)
        surf.blit(img2, (rect.x - offset[0], rect.y - offset[1]))

class Shock_waves:
    def __init__(self, pos, size, color, decay_rate, amounts):
        self.amounts = 50
        self.amounts2 = amounts
        self.type = 'Shockwave'
        self.pos = pos
        self.color = color
        self.decay_rate = decay_rate
        self.size = size
        self.done = False
        self.count = 0
        self.parts = []
    
    def update(self):
        if self.count <= self.amounts2:
            self.parts.append(Shock_wave(self.pos, random.randint(1, self.size), self.color, self.decay_rate))
            self.count += 1
        
        for part in self.parts.copy():
            part.update()
            if part.done:
                self.parts.remove(part)
        
        count2 =  len(self.parts)
        if count2 == 0:
            self.done = True
            return True
        return False
    
    def render(self, surf, offset):
        for i in self.parts:
            i.render(surf, offset)

class Spark:
    def __init__(self, pos, color, size, angle, speed):
        self.pos = pos
        self.size = size
        self.angle = angle
        self.speed = speed
        self.color = color
        self.done = False
    
    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed
        self.speed = max(0, self.speed -0.05)
        if self.speed == 0:
            self.done = True
    
    def render(self, surf, offset):
        render_points = [
            (self.pos[0] + math.cos(self.angle) * self.speed * self.size - offset[0], self.pos[1] + math.sin(self.angle) *self.speed * self.size -offset[1] ),
            (self.pos[0] + math.cos(self.angle + math.pi * 0.5) * self.speed * self.size//2 - offset[0], self.pos[1] + math.sin(self.angle + math.pi * 0.5) *self.speed * self.size//2 - offset[1] ),
            (self.pos[0] + math.cos(self.angle + math.pi) * self.speed * self.size - offset[0], self.pos[1] + math.sin(self.angle + math.pi) * self.speed * self.size -offset[1] ),
            (self.pos[0] + math.cos(self.angle - math.pi * 0.5) * self.speed * self.size//2 - offset[0], self.pos[1] + math.sin(self.angle - math.pi * 0.5) *self.speed * self.size//2 -offset[1] ),
        ]
        pygame.draw.polygon(surf, self.color, render_points)

class Sparks:
    def __init__(self, pos, size, color, speed, amounts, angle = 0):
        self.type = 'Sparks'
        self.pos = list(pos)
        self.size = size
        self.color = color
        self.speed = speed
        self.amounts = amounts
        self.angle = angle
        self.done = False
        self.count = 0
        self.parts = []
    
    def update(self):
        while self.count <= 30:
            speed = random.random() * self.speed
            if self.angle == 0:
                 angle = random.random() * math.pi * 2
            else:
                angle = self.angle
            pos = copy.deepcopy(self.pos)
            self.parts.append(Spark(pos, self.color, self.size, angle, speed))
            self.count += 1
            if self.count == 31:
                pos = copy.deepcopy(self.pos)
                self.parts.append(Spark(pos, self.color, self.size, 0, speed + 2))
                pos = copy.deepcopy(self.pos)
                self.parts.append(Spark(pos, self.color, self.size, math.pi, speed + 2))
        
        for part in self.parts.copy():
            part.update()
            if part.done:
                self.parts.remove(part)
        
        count2 = len(self.parts)
        if count2 == 0:
            self.done = True
            return True
        return False
    
    def render(self, surf, offset):
        for i in self.parts:
            i.render(surf, offset)

class SpeedLine:
    def __init__(self, pos, size, color, vel, speed):
        self.pos = pos
        self.size = size
        self.vel = vel
        self.speed = speed
        self.color = color
        self.done = False
    
    def update(self):
        self.pos[0] += self.vel * self.speed
        self.speed = max(0, self.speed - 0.1)
        if self.speed == 0:
            self.done = True

    def render(self, surf, offset):
        render_points = [
            (self.pos[0] + math.cos(0) * self.speed * self.size - offset[0], self.pos[1] + math.sin(0) *self.speed * self.size -offset[1] ),
            (self.pos[0] + math.cos(0 + math.pi * 0.5) * 2 - offset[0], self.pos[1] + math.sin(0 + math.pi * 0.5) * 2 - offset[1] ),
            (self.pos[0] + math.cos(0 + math.pi) * self.speed * self.size - offset[0], self.pos[1] + math.sin(0 + math.pi) * self.speed * self.size -offset[1] ),
            (self.pos[0] + math.cos(0 - math.pi * 0.5) * 2 - offset[0], self.pos[1] + math.sin(0 - math.pi * 0.5) * 2 -offset[1] ),
        ]
        pygame.draw.polygon(surf, self.color, render_points)

class SpeedLines:
    def __init__(self, pos, size, rect_size, color, speed, vel, amounts):
        self.type = 'blood'
        self.pos = pos
        self.size = size
        self.rect_size = rect_size
        self.color = color
        self.speed = speed
        self.amounts = amounts
        self.vel = vel
        self.done = False
        self.count = 0
        self.parts = []

    def update(self):
        if self.count <= self.amounts:

            pos = copy.deepcopy(self.pos)
            pos[0] += self.rect_size[0]//2
            pos[1] += random.randint(0, self.rect_size[1])
            size = random.random() * self.size
            speed = random.random() * self.speed + 1
            if self.color == 'speed':
                color = random.choice(['grey', 'white'])
            else:
                color = self.color
            self.parts.append(SpeedLine(pos, size, color, self.vel, speed))
            
            # pos = copy.deepcopy(self.pos)
            # pos[1] += random.randint(0, 64)
            # size = random.random() * self.size
            # speed = random.random() * self.speed + 1
            # self.parts.append(SpeedLine(pos, size, self.color, self.vel, speed))

            self.count += 1
        
        for part in self.parts.copy():
            part.update()
            if part.done:
                self.parts.remove(part)
        
        count2 =  len(self.parts)
        if count2 == 0:
            self.done = True
            return True
        return False
    
    def render(self, surf, offset):
        for i in self.parts:
            i.render(surf, offset)
    
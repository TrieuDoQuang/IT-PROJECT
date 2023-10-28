from Scripts.Assets import *
import random, math, copy

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
            self.parts.append(Smoke_Part(self.game, pos, random.randint(30, 41), (random.randint(-10, 10)/10, random.randint(-10, 10)/10), self.decay, random.randint(1,self.speed)))
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
            self.parts.append(Blode_Part(self.game, pos, random.randint(5, 8), (self.vel.x, self.vel.y + random.randint(-10, 10)), self.decay, random.randint(1, self.speed)))
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
        self.game = game
        self.rect = rect
        self.size = size
        self.vel = vel
        self.amounts = amounts
        self.count = 0
        self.parts = []
        self.done = False
    
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
            if i.rect().colliderect(self.game.Player.rect()):
                self.game.Player.DMG(100)
    
        count2 =  len(self.parts)
        if count2 == 0:
            self.done = True
            return True
        return False
    
    def render(self, surf, offset):
        for i in self.parts:
            i.render(surf, offset)

from Scripts.Assets import *
import random, math

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
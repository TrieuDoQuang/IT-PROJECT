import pygame, random

class Drop:
    def __init__(self, game, pos, type, size, scale = 1):
        self.game = game
        self.pos = pos
        self.type = type
        self.action = ''
        self.size = size
        self.scale = scale
        self.set_action(self.type)
    
    def update(self):
        self.animation.update()
    
    def function(self):
        pass

    def rect(self):
        return pygame.Rect(self.pos, self.size)
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.assets[self.type + '/' + self.action].copy()

    def render(self, surf, offset):
        img = self.animation.IMG()
        img2 = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        surf.blit(img2, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    
def DropHandler(game, pos):
        chance = random.randint(0, 100)
        if chance < 10:
            choice2 = random.choice(['health', 'ammo_pistol'])
            if choice2 == 'health':
                game.Drops.append(Drop_Health(game, pos, (100, 100)))

class Drop_Health(Drop):
    def __init__(self, game, pos, size, scale=1, amount = 100):
        super().__init__(game, pos, 'health', size, scale)
        self.amount = amount
    
    def function(self):
        pass
import pygame

class Projectile:
    def __init__(self, game, type, pos, vel, speed, angle, dame):
        self.type = type
        self.game = game
        self.pos = pos
        self.vel = vel
        self.speed = speed
        self.angle = angle
        self.dame = dame
    
    def update(self):
        pass

    def render(self, surf, offset = (0,0)):
        pass
import pygame
from Scripts.Entities import PhysicsEntity

class Player(PhysicsEntity):
    def __init__(self, e_type, pos, size, assets, Health = 400):
        super().__init__(e_type, pos, size, assets, Health)
    

from Scripts.Utils import Load_IMG, Load_IMGS, Animation
import pygame
pygame.init()
screen = pygame.display.set_mode((1280,736))
Assets= {
    'Clouds' : Load_IMGS('clouds'),
    'stone': Load_IMGS('tiles/stone'),
    'dirt': Load_IMGS('tiles/dirt'),
    'grass': Load_IMGS ('tiles/grass'),
    'Player/idle': Animation(Load_IMGS('entities/player/idle'), dur= 6),
}
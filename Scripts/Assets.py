from Scripts.Utils import Load_IMG, Load_IMGS, Animation
import pygame
pygame.init()
screen_w = 1280
screen_h = 736
screen = pygame.display.set_mode((screen_w,screen_h))

Assets= {
    'BG' : Load_IMG('bg/Background_Day.png'),
    'Clouds' : Load_IMGS('clouds'),
    'stone': Load_IMGS('tiles/stone'),
    'dirt': Load_IMGS('tiles/dirt'),
    'grass': Load_IMGS ('tiles/grass'),
    'Player/idle': Animation(Load_IMGS('entities/player/idle'), dur= 13),
    'Player/jump': Animation(Load_IMGS('entities/player/jump'), dur= 13),
    'Player/run': Animation(Load_IMGS('entities/player/run')),
    # 'Player/slide': Animation(Load_IMGS('entities/player/slide'),),
    'Player/wall_slide': Animation(Load_IMGS('entities/player/wall_slide'),),
}
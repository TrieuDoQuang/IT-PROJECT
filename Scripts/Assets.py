from Scripts.Utils import Load_IMG, Load_IMGS, Animation
import pygame
pygame.init()
screen_w = 1280
screen_h = 736
screen = pygame.display.set_mode((screen_w,screen_h))

Assets= {
    'BG' : Load_IMG('bg/Background_Day.png'),
    'Clouds' : Load_IMGS('clouds'),
    'stone': [Load_IMGS('tiles/stone'), 2],
    'dirt': [Load_IMGS('tiles/dirt'), 2],
    'grass': [Load_IMGS ('tiles/grass'), 2],
    'decor' : [Load_IMGS('tiles/decor'), 2],
    'large_decor' : [Load_IMGS('tiles/large_decor'), 3],
    'Player/idle': Animation(Load_IMGS('entities/player/idle'), dur= 13),
    'Player/jump': Animation(Load_IMGS('entities/player/jump'), dur= 13),
    'Player/run': Animation(Load_IMGS('entities/player/run')),
    # 'Player/slide': Animation(Load_IMGS('entities/player/slide'),),
    'Player/wall_slide': Animation(Load_IMGS('entities/player/wall_slide')),  
}
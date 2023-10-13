from Scripts.Utils import Load_IMG, Load_IMGS, Animation
import pygame
pygame.init()
screen_w = 1280
screen_h = 736
screen = pygame.display.set_mode((screen_w, screen_h))

Assets = {
    'BG': Load_IMG('bg/Background_Day.png'),
    'Clouds': Load_IMGS('clouds'),
    'stone': [Load_IMGS('tiles/stone'), 2],
    'dirt': [Load_IMGS('tiles/dirt'), 2],
    'grass': [Load_IMGS('tiles/grass'), 2],
    'decor': [Load_IMGS('tiles/decor'), 2],
    'large_decor': [Load_IMGS('tiles/large_decor'), 3],
    # Particles
    'Particles/leaf': Animation(Load_IMGS('particles/leaf'), dur=10, loop=False),
    'Particles/particle': Animation(Load_IMGS('particles/particle'), dur=10, loop=False),
    # PLAYER ANIMS
    'Player/idle': Animation(Load_IMGS('entities/player/idle'), dur=13),
    'Player/jump': Animation(Load_IMGS('entities/player/jump'), dur=13, loop=False),
    'Player/run': Animation(Load_IMGS('entities/player/run')),
    'Player/wall_slide': Animation(Load_IMGS('entities/player/wall_slide')),
    'Player/dash': Animation(Load_IMGS('entities/player/dash'), dur=5, loop=False),
    'Player/shield': Animation(Load_IMGS('entities/player/shield'), dur=10, loop=False),
    'Player/hurt': Animation(Load_IMGS('entities/player/hurt'), dur=13, loop=False),
    'Player/fall': Animation(Load_IMGS('entities/player/fall'), dur=10),
    'Player/die': Animation(Load_IMGS('entities/player/die'), dur=13, loop=False),
    'Player/attack0': Animation(Load_IMGS('entities/player/attack1'), dur=7, loop=False),
    'Player/attack1': Animation(Load_IMGS('entities/player/attack2'), dur=8, loop=False),
}

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
    'modular': [Load_IMGS('tiles/modular'), 2],
    'leaf': [Load_IMGS('tiles/leaf'), 1],
    'grass': [Load_IMGS('tiles/grass'), 2],
    'grass2': [Load_IMGS('tiles/grass2'), 2],
    'decor': [Load_IMGS('tiles/decor'), 2],
    'large_decor': [Load_IMGS('tiles/large_decor'), 3],
    # Particles
    'Particles/leaf': Animation(Load_IMGS('particles/leaf'), dur=15, loop=False),
    'Particles/particle': Animation(Load_IMGS('particles/particle'), dur=10, loop=False),

    # PLAYER ANIMS
    'Cursor' : Load_IMG('entities/player/cursor.png'),
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
    # Enemies ANIMS
    # Skeleton
    'Skeleton/idle': Animation(Load_IMGS('entities/enemies/skeleton/idle'), dur=10),
    'Skeleton/run': Animation(Load_IMGS('entities/enemies/skeleton/run'), dur=10),
    'Skeleton/attack': Animation(Load_IMGS('entities/enemies/skeleton/attack'), dur=10, loop=False),
    # Thug
    'Thug/idle': Animation(Load_IMGS('entities/enemies/thug/idle'), dur=13),
    'Thug/run': Animation(Load_IMGS('entities/enemies/thug/run'), dur=10),
    'Thug/attack': Animation(Load_IMGS('entities/enemies/thug/attack'), dur=10, loop=False),
    # Wizard
    'Wizard/idle': Animation(Load_IMGS('entities/enemies/wizard/idle'), dur=13),
    'Wizard/run': Animation(Load_IMGS('entities/enemies/wizard/run'), dur=10),
    'Wizard/attack': Animation(Load_IMGS('entities/enemies/wizard/attack'), dur=10, loop=False),
    # Zombie
    'Zombie/idle': Animation(Load_IMGS('entities/enemies/zombie/idle'), dur=13),
    'Zombie/run': Animation(Load_IMGS('entities/enemies/zombie/run'), dur=7),

    #WEAPONS
    'pistol/idle': Animation(Load_IMGS('weapons/pistol/idle')),
    'pistol/shoot': Animation(Load_IMGS('weapons/pistol/shoot'), dur= 3, loop= False),
    'rifle/idle': Animation(Load_IMGS('weapons/rifle/idle')),
    'rifle/shoot': Animation(Load_IMGS('weapons/rifle/shoot'), dur= 1, loop= False),
    'launcher/idle': Animation(Load_IMGS('weapons/launcher/idle')),
    'launcher/shoot': Animation(Load_IMGS('weapons/launcher/shoot'), dur= 1, loop= False),

    #BOOLETS
    'bullet/small': Load_IMG('weapons/bullets/PistolAmmoBig.png'),
    'bullet/rocket': Load_IMG('weapons/bullets/rocket.png'),
}

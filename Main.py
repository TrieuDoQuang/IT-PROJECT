import pygame
import sys
import random
import math
from Scripts.Buttons import Button
from Scripts.Clouds import Clouds
from Scripts.Player import Player
from Scripts.Assets import *
from Scripts.Tilemap import Tilemap
from Scripts.Particles import *
from Scripts.Enemies import *
from Scripts.Weapons import *

class Game:
    def __init__(self):
        self.assets = Assets
        self.state = "Main_Menu"
        self.block_size = 32
        self.scroll = [0, 0]
        self.Clouds = Clouds(self.assets['Clouds'], count=20, size_mul=2)
        self.hands = []
        self.Player = Player('Player', (250, 100), (25, 64), self.assets, size_mul=1, animoffset=(-32, 0))
        self.Butt_Play = Button((screen_w/2 - 100, 250), (200, 50), 'red', 'Play', 'Play', text_color='white', text_size=35)
        self.Butt_Exit = Button((screen_w/2 - 100, 320), (200, 50), 'red', 'Quit', 'Quit', text_color='white', text_size=35)
        self.tilemap = Tilemap(self, tile_size=32)
        self.transition = -30
        dest = 'Data/Maps/' + str(level) + '.json'
        try:
            self.tilemap.Load(dest)
        except FileNotFoundError:
            pass
        self.temp = 1

        # Particles
        self.Particles = []

        # Projectiles
        self.Projectile = []

        self.Leaf_spawner = []
        for tree in self.tilemap.extract([('large_decor', 2)], True):
            self.Leaf_spawner.append(pygame.Rect(tree['pos'][0] + 4, tree['pos'][1] + 4, 23, 13))
        
        self.Particles.append(Leafs(self, self.Leaf_spawner))

        #Extract Player pos
        for ply in self.tilemap.extract([('Spawner', 0)], keep=False):
            self.Player.pos[0] = ply['pos'][0]
            self.Player.pos[1] = ply['pos'][1]
        
        #WEAPONS
        self.hands.append(Launcher((15, 15), self.Player.pos, (58, 20), self.Projectile, scale= 0.2, offsetR=(20, 15), offsetL=(8, 40)))
        self.hands.append(Rifle((15, 15), self.Player.pos, (30, 15), self.Projectile, scale= 1.2, offsetR=(20, 25), offsetL=(2, 50)))
        self.hands.append(Pistol((15, 15), self.Player.pos, (10, 15), self.Projectile, scale= 1.2, offsetR=(30, 25), offsetL=(5, 30)))
        self.hand_idx = 0
        
        # self.enemies = []
        # self.enemies = [Thug('Thug', (500,0), (24,54), self.assets, scale= 2.5, animations_offset=(-35, -9))]
        # self.enemies = [Wizard('Wizard', (500,0), (40,53), self.assets, scale= 2.5, animations_offset=(-65, -67))]
        # self.enemies = [Skeleton('Skeleton',(500,0), (32,80), self.assets, scale= 3, animations_offset=(-78, -64))]
        self.enemies = [Zombie(self, 'Zombie', (500,0), (40,69), self.assets, scale= 3, animations_offset=(-28, -28))]
        for enemy in self.tilemap.extract([('Spawner', 2)], keep=False):
            self.enemies.append(Skeleton('Skeleton', (enemy['pos'][0],enemy['pos'][1]), (32,80), self.assets, scale= 3, animations_offset=(-78, -64)))

        for enemy in self.tilemap.extract([('Spawner', 4)], keep=False):
            self.enemies.append(Zombie(self, 'Zombie', (500,0), (40,69), self.assets, scale= 3, animations_offset=(-28, -28))) 

    def run(self):
        if self.state == "Main_Menu":
            res = self.Butt_Play.update()
            if res:
                self.state = res
            res = self.Butt_Exit.update()
            if res:
                self.state = res
            self.Butt_Play.render(display)
            self.Butt_Exit.render(display)

        elif self.state == "Play":
            # WIN_CONDITION
            # if not len(self.enemies) and not len(self.Boss):
            #     global level
            #     global max_level
            #     level = min(level + 1, max_level)
            #     self.End = True

            # BACK_GROUND
            display.blit(pygame.transform.scale(
                self.assets['BG'], (screen_w, screen_h)), (0, 0))

            # RENDER SCROLL
            self.scroll[0] += (self.Player.rect().centerx -
                               display.get_width()/2 - self.scroll[0]) / 30  # type: ignore
            self.scroll[1] += (self.Player.rect().centery -
                               display.get_height()/2 - self.scroll[1]) / 20  # type: ignore
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))


            # RENDERS
            self.Clouds.render(display, offset=render_scroll)
            self.Clouds.update()

            # PROJECTILE HANDLER
            for i in self.Projectile.copy():
                i.update()
                i.render(display, offset = render_scroll)
                if i.kill:
                    self.Projectile.remove(i)
                if self.tilemap.Tiles_around(i.pos, i.size):
                    self.Projectile.remove(i)
                if i.owner == 'player':
                    for ene in self.enemies.copy():
                        if ene.rect().colliderect(i.rect()):
                            ene.DMG(i.dame)
                            self.Projectile.remove(i)
                        if ene.Dead:
                            self.enemies.remove(ene)
                else:
                    if self.Player.rect().colliderect(i.rect()):
                        self.Projectile.remove(i)

            self.tilemap.render(display, offset=render_scroll)
            self.Player.update(self.tilemap, offset=render_scroll)
            self.Player.render(display, offset=render_scroll)

            # HAND HANDLER
            self.hands[self.hand_idx].render(display, player= self.Player, offset=render_scroll)
            self.hands[self.hand_idx].update(offset=render_scroll, player=self.Player)
            if click:
                self.hands[self.hand_idx].attack(self)

            #ENEMIES HANDLER
            for i in self.enemies.copy():
                i.update(self.tilemap, self.Player)
                i.render(display, offset=render_scroll)

            # PARTICLES HANDLER
            for Particle in self.Particles.copy():
                kill = Particle.update()
                Particle.render(display, offset=render_scroll)
                if kill:
                    self.Particles.remove(Particle)

            # TRANSITION
            if not self.temp:
                self.transition += 1
            if self.transition < 0:
                self.transition += 1

            if self.transition:
                trans_surf = pygame.Surface(display.get_size())
                pygame.draw.circle(trans_surf, "white", (display.get_width(
                ) / 2, display.get_height() / 2), (30 - abs(self.transition)) * 25)
                trans_surf.set_colorkey("white")
                display.blit(trans_surf, (0, 0))

        elif self.state == "Quit":
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((screen_w, screen_h))
    display = pygame.surface.Surface((screen_w, screen_h))
    clock = pygame.time.Clock()
    level = 0
    click = False

    FPS = 60  # FRAMERATE LIMITER
    game = Game()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.state == 'Play':
                    if event.button == 1:
                        click = True
                    if event.button == 4:
                        game.hand_idx = (game.hand_idx + 1) % len(game.hands)
                    if event.button == 5:
                        game.hand_idx = (game.hand_idx - 1) % len(game.hands)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False

        game.run()
        screen.blit(pygame.transform.scale(
            display, (screen_w, screen_h)), (0, 0))
        pygame.display.flip()

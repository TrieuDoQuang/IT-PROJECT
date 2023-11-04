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
from Scripts.Explosion import *
from Scripts.Drops import DropHandler
from Scripts.Boss import *

class Game:
    def __init__(self):
        self.assets = Assets
        self.state = "Main_Menu"
        self.block_size = 32
        self.scroll = [0, 0]
        self.Clouds = Clouds(self.assets['Clouds'], count=20, size_mul=2)
        self.Particles = []
        self.hands = []
        self.Player = Player(self, 'Player', (250, 100), (25, 64), self.assets, size_mul=1, animoffset=(-32, 0))
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

        # Projectiles
        self.Projectile = []

        # Explosion
        self.explosion = []

        # Leaf Particles
        self.Leaf_spawner = []
        for tree in self.tilemap.extract([('large_decor', 2)], True):
            self.Leaf_spawner.append(pygame.Rect(tree['pos'][0] + 4, tree['pos'][1] + 4, 23, 13))
        
        self.Particles.append(Leafs(self, self.Leaf_spawner))

        #Extract Player pos
        for ply in self.tilemap.extract([('Spawner', 0)], keep=False):
            self.Player.pos[0] = ply['pos'][0]
            self.Player.pos[1] = ply['pos'][1]
        
        #DROPS
        self.Drops = []
        
        #WEAPONS
        self.hands.append(Launcher((15, 15), self.Player.pos, (58, 20), self.Projectile, scale= 0.2, offsetR=(10, 15), offsetL=(8, 35)))
        self.hands.append(Rifle((15, 15), self.Player.pos, (30, 15), self.Projectile, scale= 1.2, offsetR=(20, 25), offsetL=(2, 50)))
        self.hands.append(Pistol((15, 15), self.Player.pos, (10, 15), self.Projectile, scale= 1.2, offsetR=(30, 25), offsetL=(5, 30)))
        self.hand_idx = 0
        
        #ENEMIES
        self.enemies = []
        # self.enemies = [Thug(self, 'Thug', (500,0), (24,54), self.assets, scale= 2.5, animations_offset=(-35, -9))]
        # self.enemies = [Wizard(self, 'Wizard', (500,0), (40,53), self.assets, scale= 2.5, animations_offset=(-65, -67))]
        # self.enemies = [Skeleton(self, 'Skeleton',(500,0), (32,80), self.assets, scale= 3, animations_offset=(-78, -64))]
        # self.enemies = [Zombie(self, 'Zombie', (500,0), (40,69), self.assets, scale= 3, animations_offset=(-28, -28))]

        for enemy in self.tilemap.extract([('Spawner', 2)], keep=False):
            self.enemies.append(Skeleton(self, 'Skeleton', (enemy['pos'][0],enemy['pos'][1]), (32,80), self.assets, scale= 3, animations_offset=(-78, -64)))

        for enemy in self.tilemap.extract([('Spawner', 4)], keep=False):
            self.enemies.append(Zombie(self, 'Zombie', (enemy['pos'][0],enemy['pos'][1]), (40,69), self.assets, scale= 3, animations_offset=(-28, -28)))

        for enemy in self.tilemap.extract([('Spawner', 1)], keep=False):
            self.enemies.append(Thug(self, 'Thug', (enemy['pos'][0],enemy['pos'][1]), (24,54), self.assets, scale= 2.5, animations_offset=(-35, -9)))
        
        for enemy in self.tilemap.extract([('Spawner', 3)], keep=False):
            self.enemies.append(Wizard(self, 'Wizard', (enemy['pos'][0],enemy['pos'][1]), (40,53), self.assets, scale= 2.5, animations_offset=(-65, -67)))
        
        #BOSS
        self.Boss = []
        self.Boss.append(Evil_wizard(self, (100, 100), 'Evil', "Evil_wizard", (80, 150), anim_offset=(-190, -150)))
        if len(self.Boss):
            self.target = self.Boss[0]

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
            pygame.display.set_caption(str(pygame.time.Clock.get_fps(clock)))
            # WIN_CONDITION
            # if not len(self.enemies) and not len(self.Boss):
            #     global level
            #     global max_level
            #     level = min(level + 1, max_level)
            #     self.End = True

            # BACK_GROUND
            display.blit(pygame.transform.scale(self.assets['BG'], (screen_w, screen_h)), (0, 0))
            # display.blit(pygame.transform.scale(pygame.Surface((screen_w, screen_h)), (screen_w, screen_h)), (0, 0))

            # RENDER SCROLL
            self.scroll[0] += (self.Player.rect().centerx - display.get_width()/2 - self.scroll[0]) / 30   # type: ignore
            self.scroll[1] += (self.Player.rect().centery - display.get_height()/2 - self.scroll[1]) / 20  # type: ignore
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # RENDERS
            self.Clouds.render(display, offset=render_scroll)
            self.Clouds.update()

            self.tilemap.render(display, offset=render_scroll)
            self.Player.update(self.tilemap, offset=render_scroll)
                    
            #DROP HANDLER
            for i in self.Drops.copy():
                i.update()
                i.render(display, offset=render_scroll)
                if i.rect().colliderect(self.Player.rect()):
                    i.function()
                    # print("after", self.hands[self.hand_idx].type, " ", self.hands[self.hand_idx].ammo)
                    self.Drops.remove(i)
            
            # PROJECTILE HANDLER
            for i in self.Projectile.copy():
                i.update()
                i.render(display, offset = render_scroll)
                if i.kill[0]:
                    if i.explosion:
                        if i.owner == 'player':
                            self.explosion.append(Explosion(i.rect().center, (200, 200), i.dame, 'Player'))
                        else:
                            self.explosion.append(Explosion(i.rect().center, (200, 200), i.dame, 'Ene'))
                        self.Particles.append(Smoke_explode(self, i.rect().center, 4, 0.5, 20))
                    self.Projectile.remove(i)
                    continue
                elif self.tilemap.Tiles_around(i.pos, i.size):
                    if i.explosion:
                        if i.owner == 'player':
                            self.explosion.append(Explosion(i.pos, (200, 200), i.dame, 'Player'))
                        else:
                            self.explosion.append(Explosion(i.rect().center, (200, 200), i.dame, 'Ene'))
                        self.Particles.append(Smoke_explode(self, i.rect().center, 4, 0.5, 20))
                    self.Particles.append(Dirt_Splater(self, 10, i.rect(), -1 if i.flip else 1, 10, 0.3, 8))
                    i.kill[0] = True
                    self.Projectile.remove(i)
                    continue
                else:
                    if i.owner == 'player':
                        # print("before",self.hands[self.hand_idx].ammo, self.hands[self.hand_idx].type)
                        for ene in self.enemies.copy():
                            if ene.rect().colliderect(i.rect()):
                                ene.DMG(i.dame)
                                if i.explosion:
                                    self.explosion.append(Explosion(i.pos, (200, 200), i.dame, 'Player'))
                                    self.Particles.append(Smoke_explode(self, i.rect().center, 4, 0.5, 20))
                                self.Particles.append(Blood_spill(self, i.rect().center, i.dir, 10, 0.05, 3 ))
                                i.kill[0] = True
                                self.Projectile.remove(i)
                                break
                        for boss in self.Boss.copy():
                            if boss.rect().colliderect(i.rect()):
                                boss.set_action('hit')
                                boss.hurt_frame = pygame.time.get_ticks()
                                boss.Recover_frame = pygame.time.get_ticks()
                                boss.DMG(i.dame)
                                i.kill[0] = True
                    else:
                        if self.Player.rect().colliderect(i.rect()):
                            if i.explosion:
                                self.explosion.append(Explosion(i.pos, (200, 200), i.dame, 'Ene'))
                                self.Particles.append(Smoke_explode(self, i.rect().center, 4, 0.5, 20))
                            if not self.Player.is_dash:
                                self.Player.DMG(i.dame)
                                self.Particles.append(Blood_spill(self, i.rect().center, i.dir, 6, 0.05, 3))
                            else:
                                self.Particles.append(Shock_waves(i.rect().center, 30, 'white', 5, amounts= 1))
                            i.kill[0] = True
                            self.Projectile.remove(i)
                            continue
            
            # HAND HANDLER
            self.hands[self.hand_idx].update(offset=render_scroll, player=self.Player)
            if click:
                self.hands[self.hand_idx].attack(self)

            # PARTICLES HANDLER BEHIND
            for Particle in sorted(self.Particles.copy(), key= lambda x: x.amounts):
                if Particle.type == 'blood':
                    kill = Particle.update()
                    Particle.render(display, offset=render_scroll)
                    if kill:
                        self.Particles.remove(Particle)

            #ENEMIES HANDLER
            for i in self.enemies.copy():
                i.update(self.tilemap, self.Player)
                i.render(display, offset=render_scroll)
                if self.Player.rect().colliderect(i.rect()):
                    if self.Player.is_dash:
                        i.DMG(100)
                        self.Particles.append(Shock_waves(i.rect().center, 30, 'white', 5, amounts= 1))
                        self.Particles.append(Blood_spill(self, i.rect().center, (-1 if self.Player.Vel.x < 0 else 1, 0), 6, 0.05, 3))
                if i.Dead:
                    self.enemies.remove(i)
                    self.Particles.append(Blood_explode(self, i.pos, 5, 0.05, 15))
                    # print("before",self.hands[self.hand_idx].ammo, self.hands[self.hand_idx].type)
                    DropHandler(self, i.pos)
            
            # BOSS HANDLER
            for boss in self.Boss.copy():
                boss.update()
                boss.render(display, offset= render_scroll)
                if boss.Dead:
                    self.Boss.remove(boss)

            # PLAYER AND HAND RENDER
            self.Player.render(display, offset=render_scroll)
            self.hands[self.hand_idx].render(display, player= self.Player, offset=render_scroll)

            # EXPLOSION HANDLER
            for i in self.explosion.copy():
                if i.owner == 'Player':
                    for ene in self.enemies.copy():
                        if ene.rect().colliderect(i.rect()):
                            ene.DMG(i.dame)
                            self.Particles.append(Blood_explode(self, ene.pos, 5, 0.05, 15))
                else:
                    if self.Player.rect().colliderect(i.rect()):
                        if not self.Player.is_dash:
                            self.Player.DMG(i.dame)
                            self.Particles.append(Blood_explode(self, self.Player.pos, 5, 0.05, 15))
                # i.render(display, render_scroll)
                self.Particles.append(Shock_waves(i.pos, 30, 'white', 5, amounts= 2))
                self.explosion.remove(i)
            
            # PARTICLES HANDLER FRONT
            for Particle in sorted(self.Particles.copy(), key= lambda x: x.amounts):
                if Particle.type != 'blood':
                    kill = Particle.update()
                    Particle.render(display, offset=render_scroll)
                    if kill:
                        self.Particles.remove(Particle)
            
            self.render_UI()
            self.cursor_render()

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
    
    def cursor_render(self):
        pygame.mouse.set_visible(False)
        mouse_pos = pygame.mouse.get_pos()
        img = self.assets['Cursor']
        img2 = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
        rect = img2.get_rect(center = mouse_pos)
        display.blit(img2, rect)
    
    def render_UI(self):
        inv = self.assets['UI/Inv'].copy()
        rect_inv = inv.get_rect(topleft = (5, 5))
        display.blit(inv, rect_inv)
        
        #WEAPONS
        wep_type = self.hands[self.hand_idx].type
        wep = self.assets['UI/' + wep_type].copy()
        wep2 = pygame.transform.rotate(wep, 45)
        rect_wep = wep2.get_rect(center = rect_inv.center)
        display.blit(wep2, rect_wep)

        #PLAYER HEALTH
        health_ration = self.Player.Health/self.Player.Max_Health
        healthbar_width = (health_ration * 360)
        if healthbar_width <= 0:
            healthbar_width = 0

        healthbar = pygame.Surface((360, 32), pygame.SRCALPHA)
        healthbar_rect = healthbar.get_rect(topleft = rect_inv.topright)
        pygame.draw.rect(healthbar, (0, 0, 0, 100), (0, 0, 360, 32), border_radius= 10)
        display.blit(healthbar, healthbar_rect)

        if health_ration*100 < 30:
             pygame.draw.rect(healthbar, 'red', (0, 0, healthbar_width, 32), border_radius= 10)
        elif health_ration*100 < 60:
             pygame.draw.rect(healthbar, 'yellow', (0, 0, healthbar_width, 32), border_radius= 10)
        else:
            pygame.draw.rect(healthbar, 'green', (0, 0, healthbar_width, 32), border_radius= 10)
        display.blit(healthbar, healthbar_rect)

        #AMMO
        ammo_surf = pygame.Surface((100, 32), pygame.SRCALPHA)
        pygame.draw.rect(ammo_surf, (0, 0, 0, 160), (0, 0, 100, 32), border_radius= 5)
        ammo_rect = ammo_surf.get_rect(topleft = healthbar_rect.bottomleft)
        ammo_count = self.hands[self.hand_idx].ammo
        ammo_str = BIG_FONT.render(str(ammo_count), True, 'white')
        ammo_str_rect = ammo_str.get_rect(center = (ammo_rect.centerx, ammo_rect.centery + 3))
        display.blit(ammo_surf, ammo_rect)
        display.blit(ammo_str, ammo_str_rect)

    def Boss_health_name(self, screen, boss):
        surf = BIG_FONT.render(boss.name, True, "white")
        screen.blit(surf, (280, 410))
        Health_bar = 600 * boss.health / boss.health_max
        Health_bar_rect = pygame.Rect(20, 440, Health_bar, 25)
        pygame.draw.rect(screen, 'aquamarine3', Health_bar_rect)


if __name__ == '__main__':
    pygame.init()
    BIG_FONT = pygame.font.Font("Data/Pixeltype.ttf", 40)
    SML_FONT = pygame.font.Font("Data/Pixeltype.ttf", 20)
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

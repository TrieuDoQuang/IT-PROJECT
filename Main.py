import pygame
import sys, os
import random
import math, json
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
        #BUTTONS
        self.Butt_Reset = Button((screen_w/2 - 100, 350), (200, 50), 'red', 'Reset', 'New Game', text_color='white', text_size=35)
        self.Butt_Play = Button((screen_w/2 - 100, 420), (200, 50), 'red', 'Play', 'Continue', text_color='white', text_size=35)
        self.Butt_Exit = Button((screen_w/2 - 100, 490), (200, 50), 'red', 'Quit', 'Quit', text_color='white', text_size=35)
        self.Butt_Main_Menu = Button((screen_w/2 - 100, 280), (200, 50), 'red', 'Menu', 'Main Menu', text_color='white', text_size=35)

        #ASSETS
        self.assets = Assets
        self.state = "Main_Menu"
        self.block_size = 32
        self.scroll = [0, 0]
        self.Clouds = Clouds(self.assets['Clouds'], count=20, size_mul=2)
        self.Particles = []
        self.hands = []
        self.Player = Player(self, 'Player', (250, 100), (25, 64), self.assets, size_mul=1, animoffset=(-32, 0))
        self.tilemap = Tilemap(self, tile_size=32)
        self.transition = -30
        self.temp = 1

        # Projectiles
        self.Projectile = []

        # Explosion
        self.explosion = []
        
        #DROPS
        self.Drops = []
        
        #WEAPONS
        self.hands.append(Pistol((15, 15), self.Player.pos, (10, 15), self.Projectile, scale= 1.2, offsetR=(30, 25), offsetL=(5, 30)))
        self.hands.append(Rifle((15, 15), self.Player.pos, (30, 15), self.Projectile, scale= 1.2, offsetR=(20, 25), offsetL=(2, 50)))
        self.hands.append(Launcher((15, 15), self.Player.pos, (58, 20), self.Projectile, scale= 0.2, offsetR=(10, 15), offsetL=(8, 35)))
        self.hand_idx = 0

        #LOAD SAVE
        try:
            self.Load_game('Data/Saves/save.json')
        except FileNotFoundError:
            if not os.path.exists('Data/Saves'):
                os.makedirs('Data/Saves')
            if not os.path.exists('Data/Saves/save.json'):
                f = open('Data/Saves/save.json', 'w')
                json.dump({'level': 0, 'pistol': 50, 'rifle': 100, 'launcher': 0, 'health': self.Player.Max_Health}, f)
                f.close()
            self.Load_game('Data/Saves/save.json')
        
        dest = 'Data/Maps/' + str(level) + '.json'
        try:
            self.tilemap.Load(dest)
        except FileNotFoundError:
            pass
        
        # Leaf Particles
        self.Leaf_spawner = []
        for tree in self.tilemap.extract([('large_decor', 2)], True):
            self.Leaf_spawner.append(pygame.Rect(tree['pos'][0] + 4, tree['pos'][1] + 4, 23, 13))
        
        self.Particles.append(Leafs(self, self.Leaf_spawner))

        #Extract Player pos
        for ply in self.tilemap.extract([('Spawner', 0)], keep=False):
            self.Player.pos[0] = ply['pos'][0]
            self.Player.pos[1] = ply['pos'][1]

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

        for boss in self.tilemap.extract([('Boss', 0)], keep= False):
            self.Boss.append(Evil_wizard(self, (boss['pos'][0], boss['pos'][1]), "Evil_wizard", (80, 150), anim_offset=(-190, -150)))
        
        for boss in self.tilemap.extract([('Boss', 1)], keep= False):
            self.Boss.append(Ghost(self, (boss['pos'][0], boss['pos'][1]), "Reaper", (90, 160), anim_offset=(-100, -60)))
        
        for boss in self.tilemap.extract([('Boss', 3)], keep= False):
            self.Boss.append(Groudon(self, (boss['pos'][0], boss['pos'][1]), "Machine dragon", (125, 190), anim_offset=(-100, -60), scale=2))
        
        for boss in self.tilemap.extract([('Boss', 2)], keep= False):
            self.Boss.append(Death(self, (boss['pos'][0], boss['pos'][1]), "Bringer of Death", (90, 155), anim_offsetL=(-165, -30), anim_offseR=(-30, -30), scale=2))
        if len(self.Boss):
            self.target = self.Boss[0]

        #LEVEL HANDLER
        self.End = False
        self.name_move_flag = False
        self.name_offset_move = 1
        self.Main_menu_BG = random.choice(['Paralax_1', 'Paralax_2', 'Paralax_3'])
        self.Main_menu = self.assets[self.Main_menu_BG].copy()

        #SFX
        pygame.mixer.init()
        self.expsfx = pygame.mixer.Sound('Data/sfx/explosion.mp3')
        self.expsfx.set_volume(0.1)

        self.ambiencesfx = pygame.mixer.Sound('Data/sfx/ambience.wav')
        self.ambiencesfx.set_volume(0.1)
        self.ambiencesfx.play(1)

    def run(self):
        if self.state == "Main_Menu":
            res = self.Butt_Play.update()
            if res:
                self.state = res

            res = self.Butt_Exit.update()
            if res:
                self.state = res
            
            res = self.Butt_Reset.update()
            if res:
                self.state = res

            self.Main_menu.update()
            display.blit(pygame.transform.scale(self.Main_menu.IMG(), (screen_w, screen_h)), (0, 0))

            name = self.assets['Name']
            name_rect = name.get_rect(center = (screen_w/2, 150 + self.name_offset_move))
            if not self.name_move_flag:
                if self.name_offset_move % 60 != 0:
                    self.name_offset_move += 0.5
                else:
                    self.name_offset_move -= 0.5
                    self.name_move_flag = True
            else:
                if self.name_offset_move % 60 != 0:
                    self.name_offset_move -= 0.5
                else:
                    self.name_offset_move += 0.5
                    self.name_move_flag = False

            display.blit(name, name_rect)

            self.Butt_Play.render(display)
            self.Butt_Exit.render(display)
            self.Butt_Reset.render(display)
        
        elif self.state == "Reset":
            os.remove('Data/Saves/save.json')
            self.End = True

        elif self.state == "Play":
            pygame.display.set_caption(str(pygame.time.Clock.get_fps(clock)))

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
                elif self.tilemap.physic_rects_around(i.pos, i.size):
                    if i.explosion:
                        if i.owner == 'player':
                            self.explosion.append(Explosion(i.pos, (200, 200), i.dame, 'Player'))
                        else:
                            self.explosion.append(Explosion(i.rect().center, (200, 200), i.dame, 'Ene'))
                        self.Particles.append(Smoke_explode(self, i.rect().center, 4, 0.5, 20))
                    else:
                        hit = pygame.mixer.Sound('Data/sfx/hit.wav')
                        hit.set_volume(0.5)
                        hit.play()
                    self.Particles.append(Dirt_Splater(self, 10, i.rect(), -1 if i.flip else 1, 10, 0.3, 8))
                    i.kill[0] = True
                    i.update()
                    self.Projectile.remove(i)
                    continue
                else:
                    if i.owner == 'player':
                        # print("before",self.hands[self.hand_idx].ammo, self.hands[self.hand_idx].type)
                        for ene in self.enemies.copy():
                            if ene.rect().colliderect(i.rect()):
                                hit = pygame.mixer.Sound('Data/sfx/hit.wav')
                                hit.set_volume(0.6)
                                hit.play()
                                ene.DMG(i.dame)
                                if i.explosion:
                                    self.explosion.append(Explosion(i.pos, (200, 200), i.dame, 'Player'))
                                    self.Particles.append(Smoke_explode(self, i.rect().center, 4, 0.5, 20))
                                self.Particles.append(Blood_spill(self, i.rect().center, i.dir, 10, 0.05, 3 ))
                                i.kill[0] = True
                                i.update()
                                self.Projectile.remove(i)
                                break
                        for boss in self.Boss.copy():
                            if boss.rect().colliderect(i.rect()):
                                self.target = boss
                                if not boss.Dead_2:
                                    if boss.Hurt_anim:
                                        boss.set_action('hit')
                                    boss.hurt_frame = pygame.time.get_ticks()
                                    boss.Recover_frame = pygame.time.get_ticks()
                                    boss.Hurt = True
                                    boss.flash_frame = pygame.time.get_ticks()
                                    hit = pygame.mixer.Sound('Data/sfx/hit.wav')
                                    hit.set_volume(0.6)
                                    hit.play()
                                    boss.DMG(i.dame)
                                    BossDropHandler(self, list(i.rect().center))
                                    self.Particles.append(Blood_spill(self, i.rect().center, i.dir, 6, 0.05, 3))
                                    i.kill[0] = True
                                    i.update()
                    else:
                        if self.Player.rect().colliderect(i.rect()):
                            if i.explosion:
                                self.explosion.append(Explosion(i.pos, (200, 200), i.dame, 'Ene'))
                                self.Particles.append(Smoke_explode(self, i.rect().center, 4, 0.5, 20))
                            if not self.Player.is_dash:
                                self.Player.DMG(i.dame)
                                self.Particles.append(Blood_explode(self, self.Player.rect().center, 6, 0.05, 20))
                            else:
                                self.Particles.append(Shock_waves(i.rect().center, 30, 'white', 5, amounts= 1))
                                self.Particles.append(Sparks(i.rect().center, 5, (255, 247, 180), 5, 60))
                            i.kill[0] = True
                            i.update()
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
                        i.DMG(20)
                        self.Particles.append(Shock_waves(i.rect().center, 30, 'white', 5, amounts= 1))
                        self.Particles.append(Blood_spill(self, i.rect().center, (-1 if self.Player.Vel.x < 0 else 1, 0), 6, 0.05, 3))
                        self.Particles.append(Sparks(i.rect().center, 5, (255, 247, 180), 5, 60))
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
                            self.Particles.append(Blood_explode(self, self.Player.rect().center, 5, 0.05, 15))
                # i.render(display, render_scroll)
                self.Particles.append(Shock_waves(i.rect().center, 30, 'white', 5, amounts= 2))
                self.explosion.remove(i)
                self.expsfx.play()
            
            # PARTICLES HANDLER FRONT
            for Particle in sorted(self.Particles.copy(), key= lambda x: x.amounts):
                if Particle.type != 'blood':
                    kill = Particle.update()
                    Particle.render(display, offset=render_scroll)
                    if kill:
                        self.Particles.remove(Particle)
            
            self.render_UI()
            if len(self.Boss):
                self.Boss_health_name(display, self.target)

            # TRANSITION
            if not self.temp:
                self.transition += 1
            if self.transition < 0:
                self.transition += 1

            if self.transition:
                trans_surf = pygame.Surface(display.get_size())
                pygame.draw.circle(trans_surf, "white", (display.get_width() / 2, display.get_height() / 2), (30 - abs(self.transition)) * 25)
                trans_surf.set_colorkey("white")
                display.blit(trans_surf, (0, 0))
            
            Pause_surf.blit(display, (0, 0))
            
            # WIN_CONDITION
            if len(self.enemies) == 0 and len(self.Boss) == 0:
                if not self.End:
                    global level
                    level = min(level + 1, max_level)
                    self.Save_game('Data/Saves/save.json', level)
                    self.End = True

            if self.Player.Dead:
                f = open('Data/Saves/save.json', 'r')
                map_data = json.load(f)
                f.close()

                f = open('Data/Saves/save.json', 'w')
                json.dump({'level': level, 'pistol': map_data['pistol'], 'rifle': map_data['rifle'], 'launcher': map_data['launcher'], 'health': self.Player.Max_Health}, f)
                f.close()
                self.End = True

        elif self.state == "Quit":
            pygame.quit()
            sys.exit()
    
    def Save_game(self, path, level):
        f = open(path, 'w')
        json.dump({'level': level, 'pistol': self.hands[0].ammo, 'rifle': self.hands[1].ammo, 'launcher': self.hands[2].ammo, 'health': self.Player.Health}, f)
        f.close()

    def Load_game(self, path):
        global level
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        self.hands[0].ammo = map_data['pistol']
        self.hands[1].ammo = map_data['rifle']
        self.hands[2].ammo = map_data['launcher']
        self.Player.Health = map_data['health']
        level = map_data['level']

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
            pygame.draw.rect(healthbar, 'chartreuse2', (0, 0, healthbar_width, 32), border_radius= 10)
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

        #DASHING_AVA
        Dash_surf = pygame.Surface((260, 32), pygame.SRCALPHA)
        pygame.draw.rect(Dash_surf, (0, 0, 0, 160), (0, 0, 260, 32), border_radius= 5)
        Dash_rect = Dash_surf.get_rect(topleft = ammo_rect.topright)
        Dash_status = self.Player.dash_ava
        if Dash_status:
            dash_text = BIG_FONT.render("Dash", True, "chartreuse2")
        else:
            dash_text = BIG_FONT.render("Dash", True, "grey")
        dash_text_rect = dash_text.get_rect(center = (Dash_rect.centerx, Dash_rect.centery + 3))
        display.blit(Dash_surf, Dash_rect)
        display.blit(dash_text, dash_text_rect)

    def Boss_health_name(self, screen, boss):
        Health_bar_width = 600 * boss.health / boss.health_max
        if Health_bar_width < 0:
            Health_bar_width = 0
        Health_bar_surf = pygame.Surface((Health_bar_width, 25))
        Health_bar_surf.fill('chartreuse2')
        Health_bar_rect = Health_bar_surf.get_rect(midbottom = (screen_w/2 , screen_h - 10))
        text = BIG_FONT.render(boss.name, True, "red")
        text_rect = text.get_rect(midbottom = Health_bar_rect.midtop)
        screen.blit(text, text_rect)
        screen.blit(Health_bar_surf, Health_bar_rect)


if __name__ == '__main__':
    pygame.init()
    MEGA_FONT = pygame.font.Font("Data/Pixeltype.ttf", 80)
    BIG_FONT = pygame.font.Font("Data/Pixeltype.ttf", 40)
    SML_FONT = pygame.font.Font("Data/Pixeltype.ttf", 20)
    screen = pygame.display.set_mode((screen_w, screen_h))
    display = pygame.surface.Surface((screen_w, screen_h))
    Pause_surf = pygame.surface.Surface((screen_w, screen_h))
    clock = pygame.time.Clock()
    max_level = len(os.listdir('Data/Maps')) - 1
    level = 0
    click = False
    Pause = False

    FPS = 60  # FRAMERATE LIMITER
    game = Game()

    while True:
        clock.tick(FPS)
        state = game.state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == 'Play':
                        Pause = not Pause
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

        if game.End:
            game = Game()
            game.state = 'Play'

        if state == 'Play':
            if not Pause:
                game.run()
                game.cursor_render()
            else:
                # PAUSE MENU
                resp = game.Butt_Main_Menu.update()
                if resp == 'Menu':
                    game = Game()
                    pygame.mouse.set_visible(True)
                    Pause = False
                else:
                    display.blit(Pause_surf, (0, 0))
                    black_overlay = pygame.Surface((screen_w, screen_h))
                    black_overlay.fill('black')
                    black_overlay.set_alpha(100)
                    display.blit(black_overlay, (0, 0))
                    game.Butt_Main_Menu.render(display)

                    display.blit(Assets['Help/Left_mouse'], (850, 400))
                    display.blit(Assets['Help/Scroll'], (850, 500))
                    display.blit(Assets['Help/Shift'], (850, 600))
                    display.blit(Assets['Help/Move'], (50, 540))

                    text = MEGA_FONT.render('PAUSE', True, 'white')
                    display.blit(text, (screen_w/2 - text.get_width()/2 + 5, screen_h/2 - 140))
                    game.cursor_render()

        else:
            game.run()

        screen.blit(pygame.transform.scale(
            display, (screen_w, screen_h)), (0, 0))
        pygame.display.flip()

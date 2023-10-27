import pygame
import time
import sys

from Scripts.Utils import Load_IMG
from Scripts.Utils import Load_IMGS
from Scripts.Tilemap import Tilemap

class Editor():
    def __init__(self):
        self.assets = {
            'decor' : [Load_IMGS('tiles/decor'), 2],
            'grass' : [Load_IMGS('tiles/grass'), 2],
            'stone' : [Load_IMGS('tiles/stone'), 2],
            'modular': [Load_IMGS('tiles/modular'), 2],
            'grass2': [Load_IMGS('tiles/grass2'), 2],
            'leaf': [Load_IMGS('tiles/leaf'), 1],
            'large_decor' : [Load_IMGS('tiles/large_decor'), 3],
            'dirt': [Load_IMGS('tiles/dirt'), 2],
            'Spawner' : [Load_IMGS('tiles/spawners'), 1],
            'Boss' : [Load_IMGS('tiles/booses'), 2]
        }

        self.Tilemap = Tilemap(self)
        self.scroll = [0, 0]

        self.Tile_list = list(self.assets)
        self.Tile_group = 0
        self.Tile_variant = 0

        try:
            self.Tilemap.Load('map.json')
        except FileNotFoundError:
            pass

    def Run(self):

        self.scroll[0] += (Movement[1] - Movement[0]) * 5
        self.scroll[1] += (Movement[3] - Movement[2]) * 5

        Display.fill('purple')
        current_tile_img = self.assets[self.Tile_list[self.Tile_group]][0][self.Tile_variant].copy()
        current_tile_img.set_alpha(150)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = [(mouse_pos[0]), mouse_pos[1]]
        loco = [int( (mouse_pos[0] + self.scroll[0] )// self.Tilemap.tile_size), int((mouse_pos[1] + self.scroll[1] )// self.Tilemap.tile_size)]
        loco_off = [round((mouse_pos[0] + self.scroll[0] )/ self.Tilemap.tile_size, 1), round((mouse_pos[1] + self.scroll[1] )/ self.Tilemap.tile_size, 1)]

        loco_str = str(loco[0]) + ';' + str(loco[1])
        loco_stroff = str(loco_off[0]) + ';' + str(loco_off[1])

        #Ghosting
        size_mul = self.assets[self.Tile_list[self.Tile_group]][1]
        img2 = current_tile_img.copy()
        img2 = pygame.transform.scale(img2, (img2.get_width() * size_mul, img2.get_height() * size_mul))
        if On_grid:
            Display.blit(img2, (loco[0] * self.Tilemap.tile_size - self.scroll[0], loco[1] * self.Tilemap.tile_size - self.scroll[1]))
        else:
            Display.blit(img2, (loco_off[0] * self.Tilemap.tile_size - self.scroll[0], loco_off[1] * self.Tilemap.tile_size - self.scroll[1]) )

        if clicking:
            if On_grid:
                self.Tilemap.tilemap[loco_str] = {'type': self.Tile_list[self.Tile_group], 'variant': self.Tile_variant, 'pos' : (loco[0], loco[1]), 'size' : self.Tile_list[self.Tile_group][1]}
            else:
                self.Tilemap.offgrid_map[loco_stroff] = {'type': self.Tile_list[self.Tile_group], 'variant': self.Tile_variant, 'pos' : (loco_off[0], loco_off[1]), 'size' : self.Tile_list[self.Tile_group][1]}

        if right_click:
            if loco_str in self.Tilemap.tilemap.copy():
                del self.Tilemap.tilemap[loco_str]

            if loco_stroff in self.Tilemap.offgrid_map.copy():
                del self.Tilemap.offgrid_map[loco_stroff]

        #BLOCK CHOICE:
        current_tile_img = pygame.transform.scale(current_tile_img, (self.Tilemap.tile_size,self.Tilemap.tile_size))
        Display.blit(current_tile_img, (0,0))

        render_scroll = (int(self.scroll[0]), int(self.scroll[1])) 
        self.Tilemap.render(Display, offset = render_scroll)


if __name__ == '__main__':
    pygame.init()
    screen_w = 1280
    screen_h = 736
    screen = pygame.display.set_mode((screen_w, screen_h))
    clock = pygame.time.Clock()

    #FPS
    FPS = 60  #FRAMERATE LIMITER
    FPS_Target = 60
    Prev_Time = time.time()
    Dt = 0

    editor = Editor()

    Movement = [False, False, False, False]

    clicking = False
    right_click = False
    shift = False

    On_grid = True

    while True:
        #CALCULATING DELTA TIME
        clock.tick(FPS)
        now = time.time()
        Dt = (now - Prev_Time) * FPS_Target
        Prev_Time = now
        pygame.display.set_caption( str( round(clock.get_fps(), 1 ) ) )

        Display = pygame.Surface((screen_w, screen_h))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicking = True
                if event.button == 3:
                    right_click = True
                if shift == False:
                    if event.button == 4:
                        editor.Tile_group = (editor.Tile_group - 1) % len(editor.Tile_list)
                        if editor.Tile_variant >=  len(editor.assets[editor.Tile_list[editor.Tile_group]][0]):
                            editor.Tile_variant = 0
                    if event.button == 5:
                        editor.Tile_group = (editor.Tile_group + 1) % len(editor.Tile_list)
                        if editor.Tile_variant >=  len(editor.assets[editor.Tile_list[editor.Tile_group]][0]):
                            editor.Tile_variant = 0
                else:
                    if event.button == 4:
                        editor.Tile_variant = (editor.Tile_variant - 1) % len(editor.assets[editor.Tile_list[editor.Tile_group]][0])
                    if event.button == 5:
                        editor.Tile_variant = (editor.Tile_variant + 1) % len(editor.assets[editor.Tile_list[editor.Tile_group]][0])
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    clicking = False
                if event.button == 3:
                    right_click = False
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    Movement[2] = True
                if event.key == pygame.K_s:
                    Movement[3] = True
                if event.key == pygame.K_a:
                    Movement[0] = True
                if event.key == pygame.K_d:
                    Movement[1] = True
                if event.key == pygame.K_LSHIFT:
                    shift = True
                if event.key == pygame.K_g:
                    On_grid = not On_grid
                if event.key == pygame.K_o:
                    editor.Tilemap.save('map.json')
                if event.key == pygame.K_t:
                    editor.Tilemap.AutoTile()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    Movement[2] = False
                if event.key == pygame.K_s:
                    Movement[3] = False
                if event.key == pygame.K_a:
                    Movement[0] = False
                if event.key == pygame.K_d:
                    Movement[1] = False
                if event.key == pygame.K_LSHIFT:
                    shift = False

        editor.Run()
        screen.blit(pygame.transform.scale(Display, (screen_w, screen_h)), (0, 0))
        pygame.display.flip()
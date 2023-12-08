import pygame
import json
from Scripts.Assets import *

AUTO_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(1, 0), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (-1, 1), (0, 0),
                   (0, -1), (0, 1), (1, 0), (1, -1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone', 'dirt', 'modular', 'leaf', 'grass2'}
AUTO_TILES = {'grass', 'stone', 'dirt', 'grass2'}


class Tilemap:
    def __init__(self, game, tile_size=32):
        self.game = game
        self.tile_size = tile_size
        self.song = ''
        self.tilemap = {}
        self.offgrid_map = {}

    def Tiles_around(self, pos, size):
        Tiles = []
        Tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        Tile_loc2 = (int((pos[0] + size[0] - self.tile_size) // self.tile_size), int((pos[1] + size[1] - self.tile_size) // self.tile_size))
        width = Tile_loc2[0] - Tile_loc[0]
        height = Tile_loc2[1] - Tile_loc[1]
        #Check X
        for i in range(-1, height):
            check_loc = str(Tile_loc[0]) + ';' + str(Tile_loc[1] + i + 1)
            if check_loc in self.tilemap:
                Tiles.append(self.tilemap[check_loc])

            check_loc2 = str(Tile_loc2[0] + 1) + ';' + str(Tile_loc[1] + i + 1)
            if check_loc2 in self.tilemap:
                Tiles.append(self.tilemap[check_loc2])

        #Check Y
        for i in range(-1, width):
            check_loc = str(Tile_loc[0] + i + 1) + ';' + str(Tile_loc[1])
            if check_loc in self.tilemap:
                Tiles.append(self.tilemap[check_loc])

            check_loc2 = str(Tile_loc[0] + i + 1) + ';' + str(Tile_loc2[1] + 1)
            if check_loc2 in self.tilemap:
                Tiles.append(self.tilemap[check_loc2])
        
        #Check Diag
        #(-1,-1)
        check_loc = str(Tile_loc[0]) + ';' + str(Tile_loc[1])
        if check_loc in self.tilemap:
            Tiles.append(self.tilemap[check_loc])
        #(1,-1)
        check_loc = str(Tile_loc2[0] + 1) + ';' + str(Tile_loc[1])
        if check_loc in self.tilemap:
            Tiles.append(self.tilemap[check_loc])
        #(1,1)
        check_loc = str(Tile_loc2[0] + 1) + ';' + str(Tile_loc2[1]  + 1)
        if check_loc in self.tilemap:
            Tiles.append(self.tilemap[check_loc])
        #(-1,1)
        check_loc = str(Tile_loc[0]) + ';' + str(Tile_loc2[1]  + 1)
        if check_loc in self.tilemap:
            Tiles.append(self.tilemap[check_loc])

        # for offset in NEIGHBOR_OFFSET:
        #     check_loc = str(Tile_loc[0] + offset[0]) + ';' + str(Tile_loc[1] + offset[1])
        #     if check_loc in self.tilemap:
        #         Tiles.append(self.tilemap[check_loc])
        return Tiles

    def physic_rects_around(self, pos, size):
        rects = []
        for tile in self.Tiles_around(pos, size):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(
                    tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def solid_check(self, pos, size, flip):
        block = None
        Tile_loc = (int(pos[0] // self.tile_size), int((pos[1] + size[1]) // self.tile_size))
        Tile_loc2 = (int((pos[0] + size[0]) // self.tile_size), int((pos[1] + size[1]) // self.tile_size))
        check_loc = str(Tile_loc[0] - 1) + ';' + str(Tile_loc[1])
        check_loc2 = str(Tile_loc2[0] + 1) + ';' + str(Tile_loc2[1])
        if flip == True:
            if check_loc in self.tilemap:
                if self.tilemap[check_loc]['type'] in PHYSICS_TILES:
                    block = self.tilemap[check_loc]
        else:
            if check_loc2 in self.tilemap:
                if self.tilemap[check_loc2]['type'] in PHYSICS_TILES:
                    block = self.tilemap[check_loc2]
        return block
    
    def AutoTile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            
            neighbors = tuple(sorted(neighbors))
            if tile['type'] in AUTO_TILES and neighbors in AUTO_MAP:
                tile['variant'] = AUTO_MAP[neighbors]

    def save(self, path):
        f = open(path, 'w')
        json.dump({'song': self.song, 'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_map}, f)
        f.close()

    def Load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        self.song = map_data['song']
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_map = map_data['offgrid']

    def extract(self, id_pair, keep=False):
        tiles = []
        for loc in self.tilemap.copy():
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pair:
                tiles.append(tile.copy())
                tiles[-1]['pos'] = tiles[-1]['pos'].copy()
                tiles[-1]['pos'][0] *= self.tile_size
                tiles[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        for loc in self.offgrid_map.copy():
            tile = self.offgrid_map[loc]
            if (tile['type'], tile['variant']) in id_pair:
                tiles.append(tile.copy())
                tiles[-1]['pos'] = tiles[-1]['pos'].copy()
                tiles[-1]['pos'][0] *= self.tile_size
                tiles[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.offgrid_map[loc]

        return tiles

    def render(self, surf, offset):
        maxlocx = (screen_w + offset[0]) // self.tile_size + 3
        minlocx = (offset[0]) // self.tile_size - 3

        maxlocy = (screen_h + offset[1]) // self.tile_size + 3
        minlocy = (offset[1]) // self.tile_size - 3
        
        for loc in self.offgrid_map:
            tile = self.offgrid_map[loc]
            if tile['pos'][0] > minlocx and tile['pos'][0] < maxlocx:
                if tile['pos'][1] > minlocy and tile['pos'][1] < maxlocy:
                    img = self.game.assets[tile['type']][0][tile['variant']]
                    size = self.game.assets[tile['type']][1]
                    image = pygame.transform.scale(img, (img.get_width() * size, img.get_height() * size))
                    surf.blit(image, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

        for x in range(offset[0] // self.tile_size - 1, (offset[0] + surf.get_width()) // self.tile_size + 3):
            for y in range(offset[1]//self.tile_size - 1, (offset[1] + surf.get_height()) // self.tile_size + 3):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    img = self.game.assets[tile['type']][0][tile['variant']]
                    size = self.game.assets[tile['type']][1]
                    image = pygame.transform.scale(img, (img.get_width() * size, img.get_height() * size))
                    surf.blit(image, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

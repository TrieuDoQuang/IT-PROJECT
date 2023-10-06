import pygame
import json

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

NEIGHBOR_OFFSET = [ (-1, 0), (-1,-1), (-1, 1), (0, 0), (0, -1), (0, 1), (1, 0), (1, -1), (1, 1) ]
PHYSICS_TILES = {'grass', 'stone', 'dirt'}
AUTO_TILES = {'grass', 'stone', 'dirt'}

class Tilemap:
    def __init__(self, game,tile_size = 32):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_map = []
        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant' : 1 ,'pos' :(3 + i, 10)}
            self.tilemap[str(3 + i) + ';9'] = {'type': 'dirt', 'variant' : 1 ,'pos' :(3 + i, 9)}
            self.tilemap['10;' + str(5 + i) ] = {'type': 'stone', 'variant' : 1 ,'pos' :(10, 5 + i)}
    
    def Tiles_around(self, pos):
        Tiles = []
        Tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSET:
            check_loc = str(Tile_loc[0] + offset[0]) + ';' + str(Tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                Tiles.append(self.tilemap[check_loc])
        return Tiles
    
    def physic_rects_around(self, pos):
        rects = []
        for tile in self.Tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def render(self, surf):
        for tile in self.offgrid_map:
            image = pygame.transform.scale(self.game.assets[tile['type']][tile['variant']], (64,64))
            surf.blit(image, (tile['pos'][0], tile['pos'][1]))
            
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            image = pygame.transform.scale(self.game.assets[tile['type']][tile['variant']], (32,32))
            surf.blit(image, (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))

        
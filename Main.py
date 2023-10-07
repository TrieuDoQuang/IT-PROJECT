import pygame, sys
from Scripts.Buttons import Button
from Scripts.Clouds import Clouds
from Scripts.Player import Player
from Scripts.Assets import *
from Scripts.Tilemap import Tilemap

class Game:
    def __init__(self):
        self.assets = Assets
        self.state = "Main_Menu"
        self.block_size = 32
        self.scroll = [0,0]
        self.Clouds = Clouds(self.assets['Clouds'], count=20, size_mul = 2)
        self.Player = Player('Player', (250, 100), (25, 64), self.assets, size_mul= 1, animoffset=(-32, 0))
        self.Butt_Play = Button((screen_w/2 - 100, 250), (200, 50), 'red', 'Play', 'Play', text_color='white' ,text_size= 35)
        self.Butt_Exit = Button((screen_w/2 - 100, 320), (200, 50), 'red', 'Quit', 'Quit', text_color='white' ,text_size= 35)
        self.tilemap = Tilemap(self, tile_size = 32)
        self.transition = -30
        dest = 'Data/Maps/' + str(level) + '.json'
        try:
            self.tilemap.Load(dest)
        except FileNotFoundError:
            pass
        self.temp = 1

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
            #WIN_CONDITION
            # if not len(self.enemies) and not len(self.Boss):
            #     global level
            #     global max_level
            #     level = min(level + 1, max_level)
            #     self.End = True

            #BACK_GROUND
            display.blit(pygame.transform.scale(self.assets['BG'], (screen_w, screen_h)), (0,0))

            ##RENDER SCROLL
            self.scroll[0] += (self.Player.rect().centerx - display.get_width()/2 - self.scroll[0]) / 30 # type: ignore
            self.scroll[1] += (self.Player.rect().centery - display.get_height()/2 - self.scroll[1]) / 20 # type: ignore
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            #RENDERS
            self.Clouds.render(display, offset = render_scroll)
            self.Clouds.update()
            self.tilemap.render(display, offset = render_scroll)
            self.Player.update(self.tilemap)
            self.Player.render(display, offset= render_scroll)

            #TRANSITION
            if not self.temp:
                self.transition += 1
            if self.transition < 0:
                self.transition += 1

            if self.transition:
                trans_surf = pygame.Surface(display.get_size())
                pygame.draw.circle(trans_surf, "white", (display.get_width() /2, display.get_height() /2), (30 - abs(self.transition)) * 25 )
                trans_surf.set_colorkey("white")
                display.blit(trans_surf, (0,0))

        elif self.state == "Quit":
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((screen_w, screen_h))
    display = pygame.surface.Surface((screen_w, screen_h))
    clock = pygame.time.Clock()
    level = 0

    FPS = 60  #FRAMERATE LIMITER
    game = Game()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        game.run()
        screen.blit(pygame.transform.scale(display, (screen_w, screen_h)), (0,0))
        pygame.display.flip()
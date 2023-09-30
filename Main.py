import pygame, sys
from Scripts.Buttons import Button

class Game:
    def __init__(self):
        self.state = "Main_Menu"
        self.Butt_Play = Button((screen_w/2 - 100, 250), (200, 50), 'red', 'Play', 'Play', text_color='white' ,text_size= 35)
        self.Butt_Exit = Button((screen_w/2 - 100, 320), (200, 50), 'red', 'Quit', 'Quit', text_color='white' ,text_size= 35)
    
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
            screen.fill('yellow')
        elif self.state == "Quit":
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    pygame.init()
    screen_w = 960
    screen_h = 540
    screen = pygame.display.set_mode((screen_w, screen_h))
    display = pygame.surface.Surface((screen_w, screen_h))
    clock = pygame.time.Clock()

    FPS = 60  #FRAMERATE LIMITER
    game = Game()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        game.run()
        screen.blit(display, (0,0))
        pygame.display.flip()
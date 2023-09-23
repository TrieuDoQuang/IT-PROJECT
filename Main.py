import pygame, sys

class Game:
    def __init__(self):
        pass
    
    def run(self):
        self.render()

    def render(self):
        pass

if __name__ == '__main__':
    pygame.init()
    screen_w = 960
    screen_h = 540
    screen = pygame.display.set_mode((screen_w, screen_h))
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
        pygame.display.flip()
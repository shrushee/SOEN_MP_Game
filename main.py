import pygame, sys
from settings import *
from level import Level
from debug import debug
from math_minigame import MathMinigame
from english_minigame import EnglishMinigame
from history_minigame import HistoryMinigame
from geo_minigame import GeographyMinigame
from science_minigame import ScienceMinigame

class Game:
    def __init__(self):

        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('QHHS')
        self.clock = pygame.time.Clock()

        self.state = "overworld"
        self.level = Level(self)
        self.minigame_cooldown = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.state == "overworld":
                self.run_overworld()
            
            elif self.state == "minigame1":
                MathMinigame(self).run()

            elif self.state == "minigame2":
                EnglishMinigame(self).run()

            elif self.state == "minigame3":
                HistoryMinigame(self).run()

            elif self.state == "minigame4":
                GeographyMinigame(self).run()
            
            elif self.state == "minigame5":
                ScienceMinigame(self).run()

            pygame.display.update()
            self.clock.tick(FPS)

    def run_overworld(self):
        self.screen.fill('black')
        self.level.run()
    
    def run_minigame1(self):
        self.screen.fill((30, 30, 30))
        font = pygame.font.Font(None, 50)
        text = font.render("MATHEMATICS", True, 'White')
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

if __name__ == '__main__':
    game = Game()
    game.run()
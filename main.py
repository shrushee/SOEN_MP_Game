import pygame, sys
import random
from settings import *
from level import Level
from debug import debug
from math_minigame import MathMinigame
from english_minigame import EnglishMinigame
from history_minigame import HistoryMinigame
from geo_minigame import GeographyMinigame
from science_minigame import ScienceMinigame
from art_minigame import ArtMinigame
from music_minigame import MusicMinigame

class Game:
    def __init__(self):

        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('QHHS')
        self.clock = pygame.time.Clock()

        self.state = "overworld"
        self.minigame_cooldown = False

        self.background = pygame.image.load("assets/chalkboard.jpg").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.font_big = pygame.font.Font("assets/fonts/Chalk Board.otf", 60)
        self.font_small = pygame.font.Font("assets/fonts/Chalk Board.otf", 40)

        self.minigame_state_map = {
            "minigame1": "minigame1",
            "minigame2": "minigame2",
            "minigame3": "minigame3",
            "minigame4": "minigame4",
            "minigame5": "minigame5",
            "minigame6": "minigame6",
            "minigame7": "minigame7"
        }
        self.minigames_to_play = random.sample(
            list(self.minigame_state_map.values()), 5
        )
        self.all_minigames = list(self.minigame_state_map.values())
        self.current_minigame_index = 0
        self.current_target_minigame = self.minigames_to_play[0]

        self.level = Level(self)
        self.total_score = 0


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
            
            elif self.state == "minigame6":
                ArtMinigame(self).run()

            elif self.state == "minigame7":
                MusicMinigame(self).run()
            
            elif self.state == "final_results":
                self.show_final_results()

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

    def show_final_results(self):
        running = True

        if self.total_score >= 40:
            rank = "S"
        elif self.total_score >= 30:
            rank = "A"
        elif self.total_score >= 20:
            rank = "B"
        elif self.total_score >= 10:
            rank = "C"
        else:
            rank = "D"

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.reset_game()
                        return

            self.screen.blit(self.background, (0,0))

            title = self.font_big.render("Day Complete! Thanks for playing!", True, (255,255,255))
            self.screen.blit(title, (WIDTH//2 - 300, 150))

            score_text = self.font_big.render(f"Total Score: {self.total_score}", True, (255, 255, 255))
            self.screen.blit(score_text, (WIDTH//2 - 250, 300))

            rank_text = self.font_big.render(f"Rank: {rank}", True, (255, 255, 255))
            self.screen.blit(rank_text, (WIDTH//2 - 150, 400))

            inst = self.font_small.render("Press SPACE to play again", True, (255, 255, 255))
            self.screen.blit(inst, (WIDTH//2 - 200, 550))

            pygame.display.update()
            self.clock.tick(FPS)
    
    def reset_game(self):
        self.total_score = 0
        self.current_minigame_index = 0
        self.minigames_to_play = random.sample(self.all_minigames, 5)
        self.current_target_minigame = self.minigames_to_play[0]
        self.state = "overworld"

if __name__ == '__main__':
    game = Game()
    game.run()
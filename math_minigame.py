import pygame
from settings import *
import random

class MathMinigame:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock

        self.font_big = pygame.font.SysFont(None, 70)
        self.font_small = pygame.font.SysFont(None, 40)

        self.score = 0
        self.current_question = None
        self.player_answer = ""
        self.generate_question()

    def generate_question(self):
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        op = random.choice(['+', '-', '*', '/'])

        if op == '+':
            self.current_question = f"{a} + {b}"
            self.correct_answer = a + b
        elif op == '-':
            self.current_question = f"{a} - {b}"
            self.correct_answer = a - b
        elif op == '*':
            self.current_question = f"{a} * {b}"
            self.correct_answer = a * b
        elif op == '/':
            # Ensure no division by zero and integer result
            while b == 0 or a % b != 0:
                a = random.randint(1, 50)
                b = random.randint(1, 50)
            self.current_question = f"{a} / {b}"
            self.correct_answer = a // b         

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.unicode.isdigit():
                        self.player_answer += event.unicode

                    if event.key == pygame.K_BACKSPACE:
                        self.player_answer = self.player_answer[:-1]

                    if event.key == pygame.K_RETURN:
                        if self.player_answer:
                            if int(self.player_answer) == self.correct_answer:
                                self.score += 1
                            else:
                                self.score -= 1
                            self.player_answer = ""
                            self.generate_question()
        
            #background
            self.screen.fill((30, 30, 30))

            #display question
            question_surf = self.font_big.render(self.current_question, True, (255, 255, 255))
            self.screen.blit(question_surf, (WIDTH//2 - 100, HEIGHT//2 - 100))

            #display player answer
            answer_surf = self.font_big.render(self.player_answer, True, (255, 255, 255))
            self.screen.blit(answer_surf, (WIDTH//2 - 100, HEIGHT//2))

            #display score
            score_surf = self.font_small.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_surf, (10, 10))

            #draw instructions
            inst_surf = self.font_small.render("Type your answer and press Enter. Press ESC to exit.", True, (255, 255, 255))
            self.screen.blit(inst_surf, (20, HEIGHT - 50))

            pygame.display.update()
            self.clock.tick(FPS)

        #return to overworld
        self.game.state = "overworld"

               
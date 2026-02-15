import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles):
        super().__init__(groups)
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.obstacles = obstacles
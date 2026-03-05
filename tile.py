import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('assets/grass.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.obstacle_sprites = obstacle_sprites
        self.obstacle_sprites.add(self)
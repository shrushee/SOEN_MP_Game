import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.Surface((64,64))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = pos)
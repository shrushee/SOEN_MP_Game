import pygame
from settings import *

class Level:
    def __init__(self):
        
        #Get display surface
        self.display_surface = pygame.display.get_surface()

        #Sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
    
        #Sprite setup
        self.create_map()

    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            print(row)
            print(row_index)


    def run(self):
        #update and draw game
        pass
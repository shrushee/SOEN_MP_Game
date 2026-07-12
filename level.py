import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *

class Level:
    def __init__(self, game):
        self.game = game
       
        #Get display surface
        self.display_surface = pygame.display.get_surface()

        #Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
    
        #Creating minigame zones
        self.minigame_zones = []
        self.create_minigame_zones()

        #Sprite setup
        self.create_map()

    def create_minigame_zones(self):
        minigame_zone1 = pygame.Rect(288, 2831, 20, 200)
        self.minigame_zones.append(('minigame1', minigame_zone1))

    def check_minigame_triggers(self):
        player_rect = self.player.rect
        for minigame_name, zone in self.minigame_zones:
            if player_rect.colliderect(zone):
                self.game.state = minigame_name

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('assets/tiles/qhhs map_boundary.csv'),
            'buildings': import_csv_layout('assets/tiles/qhhs map_buildings.csv'),
            'rail1': import_csv_layout('assets/tiles/qhhs map_railing layer.csv'),
            'rail2': import_csv_layout('assets/tiles/qhhs map_rail layer 2.csv'),
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != -1:
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites], self.obstacle_sprites, 'invisible')
                        if style == 'buildings':
                            Tile((x,y),[self.obstacle_sprites], self.obstacle_sprites, 'obstacle')
        self.player = Player((2471, 2841), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        #update and draw game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.check_minigame_triggers()
        debug(self.player.status)
        debug(f"X: {self.player.rect.x}, Y: {self.player.rect.y}", y=40)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('assets/qhhs map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))


    def custom_draw(self, player):

        #offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
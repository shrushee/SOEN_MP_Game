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
        self.active_minigame_zone = None  # Track the currently active minigame zone

        #Sprite setup
        self.create_map()

        self.font_prompt = pygame.font.Font("assets/fonts/Pixel Game.otf", 30)
        self.show_prompt = False

    def create_minigame_zones(self):
        #Maths
        minigame_zone1 = pygame.Rect(288, 2831, 10, 200)
        self.minigame_zones.append(('minigame1', minigame_zone1))

        #English
        minigame_zone2 = pygame.Rect(400, 2861, 700, 10)
        self.minigame_zones.append(("minigame2", minigame_zone2))

        #History
        minigame_zone3 = pygame.Rect(1640, 1683, 500, 10)
        self.minigame_zones.append(("minigame3", minigame_zone3))

        #Geography
        minigame_zone4 = pygame.Rect(288, 2195, 10, 300)
        self.minigame_zones.append(("minigame4", minigame_zone4))

        #Science
        minigame_zone5 = pygame.Rect(512, 1779, 700, 10)
        self.minigame_zones.append(("minigame5", minigame_zone5))

        #Art
        minigame_zone6 = pygame.Rect(1472, 627, 800, 10)
        self.minigame_zones.append(("minigame6", minigame_zone6))

        #Music
        minigame_zone7 = pygame.Rect(2304, 627, 10, 100)
        self.minigame_zones.append(("minigame7", minigame_zone7))

    def check_minigame_triggers(self):
        player_rect = self.player.rect
        keys = pygame.key.get_pressed()
        for minigame_name, zone in self.minigame_zones:
            if not self.game.minigame_cooldown:  # Check if the cooldown is not active
                if player_rect.colliderect(zone):
                    self.show_prompt = True
                    self.active_minigame_zone = minigame_name  # Set the active minigame zone

                    if keys[pygame.K_SPACE]:
                        self.game.state = minigame_name
                else:
                    self.show_prompt = False  # Hide the prompt if the player is not in any zone
                    self.active_minigame_zone = None  # Reset the active minigame zone
            else:
                self.show_prompt = False  # Hide the prompt if the cooldown is active

                in_any_zone = False
                for _, zone in self.minigame_zones:
                    if player_rect.colliderect(zone):
                        in_any_zone = True
                        break

                if not in_any_zone:
                    self.game.minigame_cooldown = False  # Reset the cooldown when the player leaves the zone

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('assets/tiles/tiles/qhhs map_boundary.csv'),
            'buildings': import_csv_layout('assets/tiles//tiles/qhhs map_buildings.csv'),
            'rail1': import_csv_layout('assets/tiles//tiles/qhhs map_railing layer.csv'),
            'rail2': import_csv_layout('assets/tiles/tiles/qhhs map_rail layer 2.csv'),
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

        if self.show_prompt and self.active_minigame_zone:
            if self.game.state == "minigame1":
                prompt_text = "Press SPACE to enter MATHEMATICS"
            elif self.game.state == "minigame2":
                prompt_text = "Press SPACE to enter ENGLISH"
            elif self.game.state == "minigame3":
                prompt_text = "Press SPACE to enter HISTORY"
            elif self.game.state == "minigame4":
                prompt_text = "Press SPACE to enter GEOGRAPHY"
            elif self.game.state == "minigame5":
                prompt_text = "Press SPACE to enter SCIENCE"
            elif self.game.state == "minigame6":
                prompt_text = "Press SPACE to enter ART"
            elif self.game.state == "minigame7":
                prompt_text = "Press SPACE to enter MUSIC"
            else:
                prompt_text = "Press SPACE to enter the minigame"

            prompt_surf = self.font_prompt.render(prompt_text, True, (255, 255, 255))
            prompt_bg = pygame.Surface((prompt_surf.get_width() + 20, prompt_surf.get_height() + 20))
            prompt_bg.fill((0, 0, 0))
            prompt_bg.set_alpha(200)  # Set transparency

            #position the prompt in the center of the screen
            x = WIDTH // 2 - prompt_bg.get_width() // 2
            y = HEIGHT - 100

            self.display_surface.blit(prompt_bg, (x, y))
            self.display_surface.blit(prompt_surf, (x + 10, y + 10))

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

        # map size
        self.map_width = self.floor_surf.get_width()
        self.map_height = self.floor_surf.get_height()


    def custom_draw(self, player):

        #offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # clamp X
        self.offset.x = max(0, min(self.offset.x, self.map_width - self.display_surface.get_width()))

        # clamp Y
        self.offset.y = max(0, min(self.offset.y, self.map_height - self.display_surface.get_height()))

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
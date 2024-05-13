from character import Character
from item import Item
import constants
import pygame
import math

class World():
  def __init__(self):
    self.map_tiles = []
    self.obstacle_tiles = []
    self.exit_tile = None
    self.player = None
    self.item_list = []
    self.enemy_list = []
    self.outerWalls = []


  def process_data(self, data, tile_list,item_images, mob_animations):
    self.level_length = len(data)
    # Iterate through every single value in level data file
    for y, row in enumerate(data):
      for x, tile in enumerate(row):
        image = tile_list[tile]
        image_rect = image.get_rect() 
        image_x = x * constants.TILE_SIZE*constants.GAME_SCALE
        image_y = y * constants.TILE_SIZE*constants.GAME_SCALE
        image_rect.center = (image_x, image_y)
        tile_data = [image, image_rect, image_x, image_y]

        # PLAYER-TILE
        if tile == 72:
          player = Character(image_x,image_y,100,mob_animations,0,constants.PLAYER_WIDTH,constants.PLAYER_HEIGHT)
          self.player = player
          tile_data[0] = tile_list[0]

       # OuterWall-TILE
        elif tile == 1:
          self.outerWalls.append(tile_data)

        # X-TILE
        elif tile == 56:
         tile_data[0] = tile_list[0]

        # Y-TILE
        elif tile == 57:
          tile_data[0] = tile_list[0]

        # SKINNY-ABERGA
        elif tile == 58:
          tile_data[0] = tile_list[0]

        # PIZZA-TILE
        elif tile == 59:
          tile_data[0] = tile_list[0]

        # EXIT-TILE
        elif tile == 60:
          self.exit_tile = tile_data

        # BRISN-TILE
        elif tile == 61:
          tile_data[0] = tile_list[0]

        # ABERGA-TILE
        elif tile == 62:
          aberga = Character(image_x, image_y, constants.ABERGA_HEALTH, mob_animations,1,constants.ABERGA_WIDTH,constants.ABERGA_HEIGHT)
          self.enemy_list.append(aberga)
          tile_data[0] = tile_list[0]
                

        # LORE-GETRÄNK
        elif tile == 63:
          potion = Item(image_x, image_y, 1, [potion])
          self.item_list.append(potion)
          tile_data[0] = tile_list[0]

        # COIN-TILE
        elif tile == 71:
          coin = Item(image_x,image_y,0,item_images[0])
          self.item_list.append(coin)
          tile_data[0] = tile_list[0]


              
        # Specify Obstacle-Tiles
        if tile != 0 and tile != 2 and tile != 3 and tile != 72 and tile != 62 and tile != 71 and tile != 63 and tile != 61 and tile != 59 and tile != 58 and tile != 60:
          self.obstacle_tiles.append(tile_data)

        # Add all tiles to main tiles list
        if tile >= 0:
          self.map_tiles.append(tile_data)
    
  def draw(self, surface):
    for tile in self.map_tiles:
      surface.blit(tile[0],tile[1])
      pygame.draw.rect(surface, constants.RED,tile[1],1)

  def update(self,screen_scroll):
    for tile in self.map_tiles:
      tile[2] += screen_scroll[0] # Update X-Kord
      tile[3] += screen_scroll[1] # Update Y-Kord
      tile[1].center = (tile[2],tile[3])



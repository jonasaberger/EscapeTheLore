from item import Item
import constants

class World():
   def __init__(self):
    self.map_tiles = []
    self.obstacle_tiles = []
    self.exit_tile = None
    self.item_list = []


   def process_data(self, data, tile_list,item_images):
    self.level_length = len(data)
    # Iterate through every single value in level data file
    for x, row in enumerate(data):
     for y, tile in enumerate(row):
      image = tile_list[tile]
      image_rect = image.get_rect() 
      image_x = x * constants.TILE_SIZE*constants.GAME_SCALE
      image_y = y * constants.TILE_SIZE*constants.GAME_SCALE
      image_rect.center = (image_x, image_y)
      tile_data = [image, image_rect, image_x, image_y]


      # Add Obstacle tiles
      # TODO: Add the rest of the obstacles
      if tile == 1:
        self.obstacle_tiles.append(tile_data)

      # TODO: Add the exit tile

      # TODO: Add the item tiles & add them to the item_list
      # if tile == 0:
        # coin = Item(image_x,image_y,0,item_images[0])
        # self.item_list.append(coin)
        # tile_data[0] = tile_list[0] -> Use the replacement image

      # TODO: Add the enemy tiles



      # Add all tiles to main tiles list
      if tile >= 0:
       self.map_tiles.append(tile_data)



   def draw(self, surface):
      for tile in self.map_tiles:
        surface.blit(tile[0],tile[1])

   def update(self,screen_scroll):
     for tile in self.map_tiles:
       tile[2] += screen_scroll[0] # Update X-Kord
       tile[3] += screen_scroll[1] # Update Y-Kord
       tile[1].center = (tile[2],tile[3])



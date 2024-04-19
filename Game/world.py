import constants

class World():
   def __init__(self):
    self.map_tiles = []

   def process_data(self, data, tile_list):
    self.level_length = len(data)
    #itereate through each value in level data file
    for x, row in enumerate(data):
     for y, tile in enumerate(row):
      image = tile_list[tile]
      image_rect = image.get_rect()
      image_x = x * constants.TILE_SIZE*constants.GAME_SCALE
      image_y = y * constants.TILE_SIZE*constants.GAME_SCALE
      image_rect.center = (image_x, image_y)
      tile_data = [image, image_rect, image_x, image_y]

      #add image data to main tiles list
      if tile >= 0:
       self.map_tiles.append(tile_data)

   def draw(self, surface):
      for tile in self.map_tiles:
        surface.blit(tile[0],tile[1])


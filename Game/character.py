import pygame;
import constants
import math

class Character():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = pygame.Rect(0,0,constants.TILE_SIZE, constants.TILE_SIZE)
        self.rect.center = (x,y)
        self.rect = pygame.Rect(0,0, constants.TILE_SIZE,40)


    # Player Movement Function
    def move(self, dx, dy):
        # Diagonal Speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        self.rect.x += dx 
        self.rect.y += dy

    # Draw the Player Character
    def draw(self, surface):
        surface.blit(self.image,self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect,1)
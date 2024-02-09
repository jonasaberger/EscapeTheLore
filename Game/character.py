import pygame;
import constants
import math

class Character():
    def __init__(self,x,y):
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x,y)


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
        pygame.draw.rect(surface, constants.RED, self.rect)
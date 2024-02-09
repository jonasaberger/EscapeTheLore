import pygame;
import constants

class Character():
    def __init__(self,x,y):
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x,y)

    # Draw the Player Character
    def draw(self, surface):
        pygame.draw.rect(surface, constants.RED, self.rect)
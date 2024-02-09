from logging import _Level
import pygame
import constants
import csv # import for csv-file
from character import Character # Import Character class

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Escape The Lore")

# define game variables
level = 1

# Create Player
player = Character(100,100)

# create empty tile list
world_data = []
r = [-1] * constants.COLS
print(r)



# Main-Game Loop
run = True 
while run:

    # Draw Player
    player.draw(screen)

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # Update Screen
    pygame.display.update()

pygame.quit()

from logging import _Level
import pygame
import constants
import csv # import for csv-file
from character import Character # Import Character class

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Escape The Lore")



# Creating Clock -> Frame Rate
clock = pygame.time.Clock()

# Define Player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# Delta X and Delta Y
dx = 0
dy = 0

# Create Player
player = Character(100,100)


# Main-Game Loop
run = True 
while run:
    # Limit Frame Rate
    clock.tick(constants.FRAMES_PER_SECOND)


    screen.fill(constants.BACKGROUND)

    # Calculate Player Movement
    # Reset movement momentum
    dx = 0
    dy = 0

    if moving_right == True:
        dx = constants.SPEED
    if moving_left == True:
        dx = -(constants.SPEED)
    
    if moving_up == True:
        dy = -(constants.SPEED)
    if moving_down == True:
        dy = constants.SPEED

    # Move Player
    player.move(dx,dy)

    print(str(dx) + "," + str(dy))
    

    # Draw Player
    player.draw(screen)

    # Event Handler
    for event in pygame.event.get():

        # Quit Game
        if event.type == pygame.QUIT:
            run = False
        

        # Take Keyboard Input
            
        # Key-Press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True

            if event.key == pygame.K_d:
                moving_right = True

            if event.key == pygame.K_w:
                moving_up = True

            if event.key == pygame.K_s:
                moving_down = True


        # Key-Release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False

            if event.key == pygame.K_d:
                moving_right = False

            if event.key == pygame.K_w:
                moving_up = False

            if event.key == pygame.K_s:
                moving_down = False


    # Update Screen
    pygame.display.update()

pygame.quit()

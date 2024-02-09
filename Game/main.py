import pygame
import constants
from character import Character # Import Character class
from button import Button

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Escape The Lore")

#helper function to scale image
def scale_img(image, scale):
  w = image.get_width()
  h = image.get_height()
  return pygame.transform.scale(image, (w * scale, h * scale))

#define game variables
start_game = False
pause_game = False

#load button images
start_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_start.png").convert_alpha(), constants.BUTTON_SCALE)
exit_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_exit.png").convert_alpha(), constants.BUTTON_SCALE)
restart_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_restart.png").convert_alpha(), constants.BUTTON_SCALE)
resume_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_resume.png").convert_alpha(), constants.BUTTON_SCALE)

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

#create button
start_button = Button(constants.SCREEN_WIDTH // 2 - 145, constants.SCREEN_HEIGHT // 2 - 150, start_img)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50, exit_img)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 50, restart_img)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, resume_img)


# Main-Game Loop
run = True 
while run:
    # Limit Frame Rate
    clock.tick(constants.FRAMES_PER_SECOND)

    if start_game == False:
        screen.fill(constants.MENU_BG)
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False
    else:
        if pause_game == True:
            screen.fill(constants.MENU_BG)
            if resume_button.draw(screen):
                pause_game = False
            if exit_button.draw(screen):
                run = False
        else:
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
            if event.key == pygame.K_ESCAPE:
                pause_game = True


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

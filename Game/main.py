from turtle import right
import pygame
import constants
from character import Character # Import Character class
from button import Button

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Escape The Lore")

# Helper function to scale image
def scale_img(image, scale):
  image_width = image.get_width()
  image_heigth = image.get_height()
  return pygame.transform.scale(image, (image_width * scale, image_heigth * scale)) 

# Define game variables
start_game = False
pause_game = False

# Load button images
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

# PLayer Animation
if moving_right == True:
    direction = "Right"
if moving_left == True:
    direction = "Left"
if moving_up == True:
    direction = "Up"
if moving_down == True:
    direction = "Down"

# Master Animation List -> contains all animations
animation_list = []

# Different Sub-Lists
idle_list = []
down_list = []
up_list = []
right_list = []
left_list = []

player_image = pygame.image.load(f"Game/assets/images/characters/Player/Idle/Default/0.png").convert_alpha()
player_image = scale_img(player_image, constants.GAME_SCALE)
idle_list.append(player_image)


for i in range(10):
    player_image = pygame.image.load(f"Game/assets/images/characters/Player/Run/Down/{i}.png").convert_alpha()
    player_image = scale_img(player_image, constants.GAME_SCALE)
    down_list.append(player_image)

for i in range(10):
    player_image = pygame.image.load(f"Game/assets/images/characters/Player/Run/Up/{i}.png").convert_alpha()
    player_image = scale_img(player_image, constants.GAME_SCALE)
    up_list.append(player_image)

for i in range(10):
    player_image = pygame.image.load(f"Game/assets/images/characters/Player/Run/Right/{i}.png").convert_alpha()
    player_image = scale_img(player_image, constants.GAME_SCALE)
    right_list.append(player_image)

for i in range(10):
    player_image = pygame.image.load(f"Game/assets/images/characters/Player/Run/Left/{i}.png").convert_alpha()
    player_image = scale_img(player_image, constants.GAME_SCALE)
    left_list.append(player_image)
    

animation_list.append(idle_list)
animation_list.append(down_list)
animation_list.append(up_list)
animation_list.append(right_list)
animation_list.append(left_list)

print(animation_list)



# Delta X and Delta Y
dx = 0
dy = 0

# Create Player
player = Character(100,100,animation_list)

# Create button
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
            updatedAction = 0

            if moving_right == True:
                dx = constants.SPEED
                updatedAction = 3
            if moving_left == True:
                dx = -(constants.SPEED)
                updatedAction = 4
            
            if moving_up == True:
                dy = -(constants.SPEED)
                updatedAction = 2
            if moving_down == True:
                dy = constants.SPEED
                updatedAction = 1

            # Move Player
            player.move(dx,dy)
            
            player.update(updatedAction)

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
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True

            if event.key == pygame.K_w or event.key == pygame.K_UP:
                moving_up = True

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                pause_game = True


        # Key-Release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False

            if event.key == pygame.K_w or event.key == pygame.K_UP:
                moving_up = False

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moving_down = False


    # Update Screen
    pygame.display.update()

pygame.quit()

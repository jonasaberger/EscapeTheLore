# from logging import _Level
from pickle import TRUE
import pygame
import constants
from character import Character # Import Character class
from screenfade import ScreenFade
from button import Button
from weapon import Weapon
from world import World
import csv

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Escape The Lore")

# Helper function to scale image
def scale_img(image, scale):
  image_width = image.get_width()
  image_heigth = image.get_height()
  return pygame.transform.scale(image, (image_width * scale, image_heigth * scale)) 

# Define game variables
level = 1

# Define game variables
start_game = False
pause_game = False
start_intro = False
 
# Load tilemap images
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"Game/assets/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

 # Create empty tile list
world_data = []
for row in range(constants.ROWS):
    row = [-1] * constants.COLS
    world_data.append(row)

# Load in level data and create world
with open("Game/levels/level1_Data.csv", newline="") as csvfile: 
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

#World Data
world = World()
world.process_data(world_data,tile_list)

# Load button images
start_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_start.png").convert_alpha(), constants.BUTTON_SCALE)
exit_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_exit.png").convert_alpha(), constants.BUTTON_SCALE)
restart_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_restart.png").convert_alpha(), constants.BUTTON_SCALE)
resume_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_resume.png").convert_alpha(), constants.BUTTON_SCALE)

# Load weapon images
ruler_image = scale_img(pygame.image.load("Game/assets/images/weapons/ruler.png").convert_alpha(), constants.WEAPON_SCALE)
pencil_image = scale_img(pygame.image.load("Game/assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)

# Load heart images
heart_empty = scale_img(pygame.image.load("Game/assets/images/GUI/heart_empty.png").convert_alpha(), constants.HEART_SCALE)
heart_half = scale_img(pygame.image.load("Game/assets/images/GUI/heart_half.png").convert_alpha(), constants.HEART_SCALE)
heart_full = scale_img(pygame.image.load("Game/assets/images/GUI/heart_full.png").convert_alpha(), constants.HEART_SCALE)

#classes down here:
#class for screen fade

# Creating Clock -> Frame Rate
clock = pygame.time.Clock()

# Define Player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

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

# Delta X and Delta Y
dx = 0
dy = 0

# Create Player
player = Character(100,100,animation_list)

# Create Player's weapon
ruler = Weapon(ruler_image, pencil_image)

#create Sprite Groups
pencil_group = pygame.sprite.Group()

# Create button
start_button = Button(constants.SCREEN_WIDTH // 2 - 145, constants.SCREEN_HEIGHT // 2 - 150, start_img)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50, exit_img)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 50, restart_img)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, resume_img)

#create screen fades
intro_fade = ScreenFade(1, constants.BLACK, 4, screen)
death_fade = ScreenFade(2, constants.PINK, 4, screen)

#Draw_grid
def draw_grid():
    for x in range(30):
        pygame.draw.line(screen,constants.WHITE, (x * constants.TILE_SIZE, 0), (x * constants.TILE_SIZE, constants.SCREEN_HEIGHT))
        pygame.draw.line(screen,constants.WHITE, (0, x * constants.TILE_SIZE), (constants.SCREEN_HEIGHT, x * constants.TILE_SIZE))

# Main-Game Loop
run = True 
while run:
    # Limit Frame Rate
    clock.tick(constants.FRAMES_PER_SECOND)

    draw_grid()

    if start_game == False:
        screen.fill(constants.MENU_BG)
        if start_button.draw(screen):
            start_game = True
            start_intro = True
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

            # Update Ruler
            pencil = ruler.update(player)
            if pencil:
                pencil_group.add(pencil)
            
            print(pencil_group)

            world.draw(screen)

            # Draw Player
            player.draw(screen)

            # Draw Ruler
            ruler.draw(screen)

    #show intro
    if start_intro == True:
        if intro_fade.fade():
          start_intro = False
          intro_fade.fade_counter = 0


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

from pickle import TRUE
import pygame
import pygame.font
import constants
from character import Character # Import Character class
from screenfade import ScreenFade
from damagetext import DamageText
from button import Button
from weapon import Weapon
from world import World
from item import Item
import csv
pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Escape The Lore")
# HELPER FUNCTIONS

# Function to scale images
def scale_img(image, scale):
    image_width = image.get_width()
    image_heigth = image.get_height()
    return pygame.transform.scale(image, (image_width * scale, image_heigth * scale)) 

# Define game variables
level = 1
constants.LEVEL_NAMES.append("HTL")
constants.LEVEL_NAMES.append("HAK")

# Define game variables
start_game = False
pause_game = False
start_intro = False
 
# Load tilemap images
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"Game/assets/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE*constants.GAME_SCALE, constants.TILE_SIZE*constants.GAME_SCALE))
    tile_list.append(tile_image)

 # Create empty tile list
world_data = []
for row in range(constants.ROWS):
    row = [-1] * constants.COLS
    world_data.append(row)

# Load in level data and create world
with open("Game/levels/Level1.csv", newline="") as csvfile: 
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)


# Load button images
start_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_start.png").convert_alpha(), constants.BUTTON_SCALE)
exit_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_exit.png").convert_alpha(), constants.BUTTON_SCALE)
restart_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_restart.png").convert_alpha(), constants.BUTTON_SCALE)
resume_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_resume.png").convert_alpha(), constants.BUTTON_SCALE)

# Load weapon images
ruler_image = scale_img(pygame.image.load("Game/assets/images/weapons/ruler.png").convert_alpha(), constants.WEAPON_SCALE)
pencil_image = scale_img(pygame.image.load("Game/assets/images/weapons/pencil.png").convert_alpha(), constants.WEAPON_SCALE)

# Load heart images
heart_empty = scale_img(pygame.image.load("Game/assets/images/GUI/heart_empty.png").convert_alpha(), constants.HEART_SCALE)
heart_half = scale_img(pygame.image.load("Game/assets/images/GUI/heart_half.png").convert_alpha(), constants.HEART_SCALE)
heart_full = scale_img(pygame.image.load("Game/assets/images/GUI/heart_full.png").convert_alpha(), constants.HEART_SCALE)

#load coin images
coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"Game/assets/images/GUI/coin_f{x}.png").convert_alpha(), constants.ITEM_SCALE)
    coin_images.append(img)

#load potion image
potion = scale_img(pygame.image.load("Game/assets/images/items/lore_potion.png").convert_alpha(), constants.POTION_SCALE)


# Add different Items to the general Item-List
item_images = []
item_images.append(coin_images)
item_images.append(potion)

#World Data
world = World()


#load bg image
titlescreen = pygame.image.load("Game/assets/images/GUI/menu_bg.png")


# Creating Clock -> Frame Rate
clock = pygame.time.Clock()

# Define Game variables
level = 1
screen_scroll = [0,0]

# Define Player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#define font
font = pygame.font.Font("Game/assets/fonts/MainFont.ttf", 30)

# Mob Types -> Different Types of Mobs and enemies
mob_animations = []
mob_types = ["Player", "Aberga"] #TODO:"Change PlayerPlaceholder to Aberga-Animation"
 

for mob in mob_types:
    # Master Animation List -> contains all animations
    animation_list = []

    # Different Sub-Lists
    idle_list = []
    down_list = []
    up_list = []
    right_list = []
    left_list = []

    player_image = pygame.image.load(f"Game/assets/images/characters/{mob}/Idle/Default/0.png").convert_alpha()
    player_image = scale_img(player_image, constants.GAME_SCALE)
    idle_list.append(player_image)

    for i in range(10):
        player_image = pygame.image.load(f"Game/assets/images/characters/{mob}/Run/Down/{i}.png").convert_alpha()
        player_image = scale_img(player_image, constants.GAME_SCALE)
        down_list.append(player_image)

    for i in range(10):
        player_image = pygame.image.load(f"Game/assets/images/characters/{mob}/Run/Up/{i}.png").convert_alpha()
        player_image = scale_img(player_image, constants.GAME_SCALE)
        up_list.append(player_image)

    for i in range(10):
        player_image = pygame.image.load(f"Game/assets/images/characters/{mob}/Run/Right/{i}.png").convert_alpha()
        player_image = scale_img(player_image, constants.GAME_SCALE)
        right_list.append(player_image)

    for i in range(10):
        player_image = pygame.image.load(f"Game/assets/images/characters/{mob}/Run/Left/{i}.png").convert_alpha()
        player_image = scale_img(player_image, constants.GAME_SCALE)
        left_list.append(player_image)
        
    animation_list.append(idle_list)
    animation_list.append(down_list)
    animation_list.append(up_list)
    animation_list.append(right_list)
    animation_list.append(left_list)
    mob_animations.append(animation_list)

world.process_data(world_data,tile_list,item_images, mob_animations)


# Delta X and Delta Y
dx = 0
dy = 0

#function for outputing text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for displaying Game Info
def draw_info():

    #Draw Panel
    pygame.draw.rect(screen, constants.PANEL, (0,0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0,50), (constants.SCREEN_WIDTH, 50))

    #Draw lives
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20): # type: ignore
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20 > 0) and half_heart_drawn == False: # type: ignore
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
           screen.blit(heart_empty, (10 + i * 50, 0))

    # Display level
    draw_text(f"LEVEL: {constants.LEVEL_NAMES[level-1]}", constants.MAIN_FONT,constants.WHITE,constants.SCREEN_WIDTH/2,15)
    
    # Display score
    draw_text(f"CoinScore: {player.score}", font, constants.WHITE,constants.SCREEN_WIDTH - 150, 20) # type: ignore
    
# Create Player
player = world.player


# Create Player's weapon
ruler = Weapon(ruler_image, pencil_image, world.outerWalls)



# Create Sprite Groups
damage_text_group = pygame.sprite.Group()
pencil_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH-160, 26.5, 0, coin_images, True)
item_group.add(score_coin)

potion = Item(200, 200, 1, [potion])
item_group.add(potion)
coin = Item(400, 400, 0, coin_images)
item_group.add(coin)

# Add the Items from the level data
for item in world.item_list:
    item_group.add(item)

# Create button
start_button = Button(630, 530, start_img) #constants.SCREEN_WIDTH // 2 - 145, constants.SCREEN_HEIGHT // 2 - 150
exit_button = Button(665,630, exit_img) #constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50
exit_pause_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50, exit_img)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 50, restart_img)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, resume_img)

#create screen fades
intro_fade = ScreenFade(1, constants.BLACK, 4, screen)
death_fade = ScreenFade(2, constants.PINK, 4, screen)

#Draw_grid


# Main-Game Loop
run = True 
while run:
    # Limit Frame Rate
    clock.tick(constants.FRAMES_PER_SECOND)

    if start_game == False:
        screen.blit(titlescreen, (0, 0))
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        if pause_game == True:
            if resume_button.draw(screen):
                pause_game = False
            if exit_pause_button.draw(screen):
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
            screen_scroll = player.move(dx,dy,world.obstacle_tiles) #type:ignore
            print(screen_scroll)
            

            # UPDATES

            # Update the world
            world.update(screen_scroll)


            # Update all enemies in enemy_list
            for enemy in world.enemy_list:
                enemy.ai(screen_scroll)
                enemy.update(0)

            # Update the player
            player.update(updatedAction) # type: ignore

            # Update Ruler
            pencil = ruler.update(player)

            if pencil:
                pencil_group.add(pencil)
            for pencil in pencil_group:
                damage, damage_pos = pencil.update(screen_scroll, world.enemy_list)
                if damage != 0:
                    if damage == 14:
                        damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.YELLOW)
                    else:
                     damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
                    damage_text_group.add(damage_text)
            damage_text_group.update(screen_scroll)
            item_group.update(screen_scroll,player)
            

            world.draw(screen)
            item_group.draw(screen)
            draw_info()
            score_coin.draw(screen)

            # Player Update & Draw
            player.draw(screen) #type: ignore


            # Draw all enemies in enemy_list
            for enemy in world.enemy_list:
             enemy.draw(screen)


            # Draw Ruler & pencil
            ruler.draw(screen)
            for pencil in pencil_group:
                pencil.draw(screen)

            damage_text_group.draw(screen)
            

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
            # Movement
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True

            if event.key == pygame.K_w or event.key == pygame.K_UP:
                moving_up = True

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moving_down = True

            # Menu
            if event.key == pygame.K_ESCAPE and pause_game == False:
                pause_game = True
            elif event.key == pygame.K_ESCAPE and pause_game == True:
                pause_game = False


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

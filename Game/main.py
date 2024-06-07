from pickle import TRUE
import subprocess
from tkinter.tix import INTEGER
import pygame
# from pygame import mixer
import pygame.font
import pygame.image
from music import Music
import constants
from character import Character # Import Character class
from screenfade import ScreenFade
from damagetext import DamageText
from button import Button
from weapon import Weapon
from world import World
from item import Item
import csv
import os

# mixer.init()
pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Escape The Lore")

# Creating Clock -> Frame Rate
clock = pygame.time.Clock()

# Define game variables
level = 11
screen_scroll = [0,0]
start_game = False
pause_game = False
start_intro = False
game_over = False
restart_available = False

# Define Player movement variables
dx = 0
dy = 0
moving_left = False
moving_right = False
moving_up = False
moving_down = False

temp_hp = 0
temp_score = 0
brisn_boost = 0

temp_potion_price = constants.SHOP_POTION_BASE
temp_brisn_price = constants.SHOP_BRISN_BASE
temp_rockerflasche_price = constants.SHOP_ROCKERFLASCHE_BASE
temp_rocker = False

# Helper Function to scale images
def scale_img(image, scale):
    image_width = image.get_width()
    image_heigth = image.get_height()
    return pygame.transform.scale(image, (image_width * scale, image_heigth * scale))

#Function for loading music and soundfx

# Music
musicPlayer = Music("Game/assets/audio/background_music.wav",0.5)
musicPlayer.toggleMusic()

# SoundFX
shot_fx = pygame.mixer.Sound("Game/assets/audio/arrow_shot.mp3")
shot_fx.set_volume(0.6)
hit_fx = pygame.mixer.Sound("Game/assets/audio/arrow_hit.wav")
hit_fx.set_volume(0.6)
coin_fx = pygame.mixer.Sound("Game/assets/audio/coin.wav")
coin_fx.set_volume(0.6)
heal_fx = pygame.mixer.Sound("Game/assets/audio/heal.wav")
heal_fx.set_volume(0.6)
pizza_fx = pygame.mixer.Sound("Game/assets/audio/pizza_consume.mp3")
pizza_fx.set_volume(0.6)
brisn_fx = pygame.mixer.Sound("Game/assets/audio/brisn_consume.mp3")
brisn_fx.set_volume(0.6)

# Function for loading all the sprite images -> Function for better readability
def getImages():
    # Load the different collectables Images
    def getItemImages():
        coin_images = []
        for x in range(4):
            img = scale_img(pygame.image.load(f"Game/assets/images/GUI/coin_images/coin_f{x}.png").convert_alpha(), constants.COIN_SCALE)
            coin_images.append(img)
        potion_image = scale_img(pygame.image.load("Game/assets/images/items/lore_potion.png").convert_alpha(), constants.POTION_SCALE)
        pizza_image = scale_img(pygame.image.load("Game/assets/images/items/pizza.png").convert_alpha(),constants.PIZZA_SCALE)
        brisn_image = scale_img(pygame.image.load("Game/assets/images/items/brisn.png").convert_alpha(),constants.BRISN_SCALE)
        rockflasche_image = scale_img(pygame.image.load("Game/assets/images/items/rockflasche.png").convert_alpha(),1)
        return coin_images, potion_image, pizza_image,brisn_image,rockflasche_image
    def getHeartImages():
        heart_empty = scale_img(pygame.image.load("Game/assets/images/GUI/heart_images/heart_empty.png").convert_alpha(), constants.HEART_SCALE)
        heart_half = scale_img(pygame.image.load("Game/assets/images/GUI/heart_images/heart_half.png").convert_alpha(), constants.HEART_SCALE)
        heart_full = scale_img(pygame.image.load("Game/assets/images/GUI/heart_images/heart_full.png").convert_alpha(), constants.HEART_SCALE)
        return heart_empty, heart_half, heart_full
    def getWeaponImages():
        ruler_image = scale_img(pygame.image.load("Game/assets/images/weapons/ruler.png").convert_alpha(), constants.WEAPON_SCALE)
        pencil_image = scale_img(pygame.image.load("Game/assets/images/weapons/pencil.png").convert_alpha(), constants.WEAPON_SCALE)
        return ruler_image,pencil_image
    def getButtonImages():
        start_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_start.png").convert_alpha(), constants.BUTTON_SCALE)
        exit_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_exit.png").convert_alpha(), constants.BUTTON_SCALE)
        restart_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_restart.png").convert_alpha(), constants.BUTTON_SCALE)
        resume_img = scale_img(pygame.image.load("Game/assets/images/buttons/button_resume.png").convert_alpha(), constants.BUTTON_SCALE)
        return start_img, exit_img, restart_img, resume_img
    def getTileImages():
        tile_images = []
        for x in range(constants.TILE_TYPES):
            tile_image = pygame.image.load(f"Game/assets/tiles/{x}.png").convert_alpha()
            tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE*constants.GAME_SCALE, constants.TILE_SIZE*constants.GAME_SCALE))
            tile_images.append(tile_image)
        return tile_images
    def getSchanzenShopImages():
        tile_texture = scale_img(pygame.image.load("Game/assets/images/schanzenshop/tile-texture.png").convert_alpha(),constants.SHOP_TILE_SCALE)
        schnazenshop_main = pygame.image.load("Game/assets/images/schanzenshop/schanzenshop_main.png").convert_alpha()
        return tile_texture, schnazenshop_main
    def getExitImages():
        exitOff_image = scale_img(pygame.image.load("Game/assets/images/GUI/exit/exit_off.png").convert_alpha(),constants.EXIT_SCALE)
        exitOn_image = scale_img(pygame.image.load("Game/assets/images/GUI/exit/exit_on.png").convert_alpha(),constants.EXIT_SCALE)
        return exitOff_image, exitOn_image

    item_images = getItemImages()
    heart_images = getHeartImages()
    weapon_images = getWeaponImages()
    button_images = getButtonImages()
    titlescreen_image = pygame.image.load("Game/assets/images/GUI/menu_bg.png")
    tile_images = getTileImages()
    schanzenshop_images = getSchanzenShopImages()
    exit_images = getExitImages()

    return item_images, heart_images, weapon_images, button_images, titlescreen_image, tile_images, schanzenshop_images, exit_images
item_images,heart_images,weapon_images,button_images,titlescreen_image,tile_images,schanzenshop_images,exit_images = getImages()

# Function for outputing text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for displaying Game Info
def draw_info():
    #Draw Panel
    pygame.draw.rect(screen, constants.PANEL, (0,0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0,50), (constants.SCREEN_WIDTH, 50))

    #Draw lives
    try:
        half_heart_drawn = False
        for i in range(5):
            if player.health >= ((i + 1) * 20): #type:ignore -> Exception
                screen.blit(heart_images[2], (10 + i * 50, 0)) 
            elif (player.health % 20 > 0) and half_heart_drawn == False: #type:ignore -> Exception
                screen.blit(heart_images[1], (10 + i * 50, 0))
                half_heart_drawn = True
            else:
                screen.blit(heart_images[0], (10 + i * 50, 0))
    
        
        # Display level
        draw_text(f"LEVEL: {constants.LEVEL_NAMES[level-1]}", constants.MAIN_FONT,constants.WHITE,constants.SCREEN_WIDTH/2,15)
        
        # Display score
        draw_text(f"CoinScore: {player.score}", constants.MAIN_FONT, constants.WHITE,constants.SCREEN_WIDTH - 150, 20) #type:ignore -> Exception
    except:
        print("Player is None!")
# Reset the entire tilemap
def reset_level():
  damage_text_group.empty()
  pencil_group.empty()
  item_group.empty()

  #create empty tile list
  data = []
  for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    data.append(r)

  return data

# Mob Types -> Different Types of Mobs and enemies -> Function for better readability
def getMobAnimations():
    mob_animations = []
    rock_animations = []
    for mob in constants.MOB_TYPES:
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
        
        if mob != "Player":
            death_animation_list = []
            if mob != "Igol":
                for i in range(8):
                    player_image = pygame.image.load(f"Game/assets/images/characters/{mob}/Death/{i}.png").convert_alpha()
                    player_image = scale_img(player_image, constants.GAME_SCALE)
                    death_animation_list.append(player_image)
            else:
                for i in range(22):
                    player_image = pygame.image.load(f"Game/assets/images/characters/{mob}/Death/{i}.png").convert_alpha()
                    player_image = scale_img(player_image, constants.GAME_SCALE)
                    death_animation_list.append(player_image)

            animation_list.append(death_animation_list)
        mob_animations.append(animation_list)

    # Add the Rocker skin for when buying the rockerflasche
    rocker_animations = []
    rocker_idle_list = []
    rocker_down_list = []
    rocker_up_list = []
    rocker_left_list = []
    rocker_right_list = []

    player_image = pygame.image.load(f"Game/assets/images/characters/RockerPlayer/Idle/Default/0.png").convert_alpha()
    player_image = scale_img(player_image, constants.GAME_SCALE)
    rocker_idle_list.append(player_image)
    for i in range(10):
        player_image = pygame.image.load(f"Game/assets/images/characters/RockerPlayer/Run/Down/{i}.png").convert_alpha()
        player_image = scale_img(player_image, constants.GAME_SCALE)
        rocker_down_list.append(player_image)

    for i in range(10):
        player_image = pygame.image.load(f"Game/assets/images/characters/RockerPlayer/Run/Up/{i}.png").convert_alpha()
        player_image = scale_img(player_image, constants.GAME_SCALE)
        rocker_up_list.append(player_image)

    for i in range(10):
        player_image = pygame.image.load(f"Game/assets/images/characters/RockerPlayer/Run/Right/{i}.png").convert_alpha()
        player_image = scale_img(player_image, constants.GAME_SCALE)
        rocker_right_list.append(player_image)

    for i in range(10):
        player_image = pygame.image.load(f"Game/assets/images/characters/RockerPlayer/Run/Left/{i}.png").convert_alpha()
        player_image = scale_img(player_image, constants.GAME_SCALE)
        rocker_left_list.append(player_image)
    
    rocker_animations.append(rocker_idle_list)
    rocker_animations.append(rocker_down_list)
    rocker_animations.append(rocker_up_list)
    rocker_animations.append(rocker_right_list)
    rocker_animations.append(rocker_left_list)

    return mob_animations, rocker_animations
mob_animations,rocker_animations = getMobAnimations()

# Load in level data and create world
world_data = []
for row in range(constants.ROWS):
    row = [-1] * constants.COLS
    world_data.append(row)
with open(f"Game/levels/{level}.csv", newline="") as csvfile: 
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data,tile_images,item_images, mob_animations, schanzenshop_images,exit_images)

# Create Player + Weapon
player = world.player
ruler = Weapon(weapon_images[0], weapon_images[1], world.outerWalls)

# Get the enemy list 
enemy_list = world.enemy_list

# Create the sprite groups
damage_text_group = pygame.sprite.Group()
pencil_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
puck_group = pygame.sprite.Group()

# Score/Display coin
score_coin = Item(constants.SCREEN_WIDTH-160, 26.5, 0, item_images[0], True)

# Add the Items from the level data
for item in world.item_list: 
    item_group.add(item)

# Create button
start_button = Button(630, 530, button_images[0]) #constants.SCREEN_WIDTH // 2 - 145, constants.SCREEN_HEIGHT // 2 - 150
exit_button = Button(665,630, button_images[1]) #constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50
exit_pause_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50, button_images[1])
restart_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, button_images[2])
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, button_images[3])

# Create screen fades
intro_fade = ScreenFade(1, constants.BLACK, 4, screen)
death_fade = ScreenFade(2, constants.PINK, 14, screen)
shopActive = False
touchShop = False
shopMusic = False
mainMusic = True

# Main-Game Loop
run = True

while run:
    # Limit Frame Rate
    clock.tick(constants.FRAMES_PER_SECOND)
    if start_game == False:
        screen.blit(titlescreen_image, (0, 0))
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        if pause_game == True:
            if restart_available == True:
                if restart_button.draw(screen):
                   restart_available = False
                   subprocess.Popen(['python','Game/main.py'])
                   run = False
                              
            else:
                if resume_button.draw(screen):
                    pause_game = False
            if exit_pause_button.draw(screen):
                run = False   
        else:
            if shopActive == True:
                if not shopMusic:
                    shopMusic = True
                    mainMusic = False
                    musicPlayer.toggleMusic()
                    musicPlayer.loadMusic("Game/assets/audio/schanzenshop_theme.wav")
                    musicPlayer.toggleMusic()

                world.schanzenshop.drawInterface(screen,score_coin,schanzenshop_images,item_images,screen_scroll,player,coin_fx,heal_fx,pizza_fx,brisn_fx,draw_text,scale_img) #type:ignore -> Exception 
            else:
                shopMusic = False
                if not mainMusic and player.isRocker == False: #type:ignore -> Exception
                    mainMusic = True
                    musicPlayer.toggleMusic()
                    musicPlayer.loadMusic("Game/assets/audio/background_music.wav")
                    musicPlayer.toggleMusic()
                elif not mainMusic and player.isRocker == True: #type:ignore -> Exception
                    mainMusic = True
                    musicPlayer.toggleMusic()
                    musicPlayer.loadMusic("Game/assets/audio/rocker_theme.mp3")
                    musicPlayer.toggleMusic()
                screen.fill(constants.BACKGROUND)
            # Calculate Player Movement
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

            try:
                # Check if player was actually not defines
                if player == None:
                    raise Exception('Player is None!')

                # Move Player Method
                screen_scroll, level_complete = player.move(dx,dy,world.obstacle_tiles,world.exit_tile)
                # Update the Player
                player.update(updatedAction)
                
                # Update all enemies in enemy_list
                if shopActive == False:
                    for enemy in enemy_list:
                        puck = enemy.ai(screen, player, world.obstacle_tiles, screen_scroll)
                        if puck:
                            puck_group.add(puck)
                    #score_coin.update(screen_scroll,player)
                    world.update(screen_scroll)

                    # Update Ruler / Weapon
                    pencil = ruler.update(player)
                    if pencil:
                        pencil_group.add(pencil)
                        shot_fx.play()
                    for pencil in pencil_group:
                        damage, damage_pos = pencil.update(screen_scroll, world.enemy_list,player.damage_boost)
                        if damage != 0:
                            if damage == 14:
                                damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.YELLOW)
                            else:
                                damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
                                damage_text_group.add(damage_text)
                                hit_fx.play()
                    damage_text_group.update(screen_scroll)
                    puck_group.update(screen_scroll,player)
                    item_group.update(screen_scroll,player, coin_fx, heal_fx, pizza_fx,brisn_fx)
                if world.schanzenshop != None:
                    world.schanzenshop.update(screen_scroll)
                # Game over
                if game_over == True:
                    restart_available = True

                # DRAW-METHODS
                if shopActive == False:
                    world.draw(screen)
                    for enemy in enemy_list:
                        enemy.draw(screen)
                    # Player Draw + Weapon / Projectiles
                    player.draw(screen)
                    ruler.draw(screen)
                    for pencil in pencil_group:
                        pencil.draw(screen)
                    for puck in puck_group:
                        puck.draw(screen)
                    damage_text_group.draw(screen)
                    item_group.draw(screen)
                    if world.schanzenshop != None:
                        world.schanzenshop.draw(screen)
                        if player.rect.colliderect(world.schanzenshop.hitbox):
                            touchShop = True
                        else:
                            touchShop = False
                draw_info()
                score_coin.draw(screen)
                score_coin.update(screen_scroll,player,coin_fx,heal_fx,pizza_fx,brisn_fx)
                  
                # Check if game over
                if player.health == 0:
                    game_over = True

                # Change player skin to rocker
                if player.isRocker:
                    player.changeSkin(rocker_animations)

                # Change the exit tile when all pizzas are collected
                if player.pizzaCount == world.totalPizzas:
                    world.activateExit()

                if level_complete == True and player.pizzaCount == world.totalPizzas:
                    # Save the hp and score
                    temp_hp = player.health
                    temp_score = player.score
                    brisn_boost = player.damage_boost
                    temp_rocker = player.isRocker

                    if world.schanzenshop != None:
                        temp_potion_price = world.schanzenshop.schanzenshop_potion_price
                        temp_brisn_price = world.schanzenshop.schanzenshop_brisn_price
                        temp_rockerflasche_price = world.schanzenshop.schanzenshop_rockerflasche_price

                    level += 1
                    world_data = reset_level()
                    #load in level data and create world
                    with open(f"Game/levels/{level}.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter = ",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    world.process_data(world_data, tile_images, item_images, mob_animations,schanzenshop_images,exit_images)
                    player = world.player
                    if player == None:
                        raise Exception('Player is None!')
                    player.health = temp_hp
                    player.score = temp_score
                    player.damage_boost = brisn_boost
                    enemy_list = world.enemy_list
                    score_coin = Item(constants.SCREEN_WIDTH - 160, 26.5, 0, item_images[0], True)
                    player.isRocker = temp_rocker
                    for item in world.item_list:
                        item_group.add(item)

                    if world.schanzenshop != None:
                        world.schanzenshop.updatePrices(temp_potion_price,temp_brisn_price,temp_rockerflasche_price)

                # TODO: Maybe play error sound when cant access exit yet
                elif level_complete == True and player.pizzaCount < world.totalPizzas:
                    print(" ")
            except Exception as error:
                print(error)
                run = False
    # Show intro
    if start_intro == True:
        if intro_fade.fade():
          start_intro = False
          intro_fade.fade_counter = 0

    # show deathfade
    if game_over == True:
        if death_fade.fade():
          pause_game = True
          game_over = False
          death_fade.fade_counter = 0

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
                if shopActive == True:
                    shopActive = False
                else:
                    pause_game = True
            elif event.key == pygame.K_ESCAPE and pause_game == True:
                pause_game = False

        # Schanzenshop
            shopActive = False
            if event.key == pygame.K_e and touchShop == True:
                shopActive = True
            else:
                shopActive = False
        
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

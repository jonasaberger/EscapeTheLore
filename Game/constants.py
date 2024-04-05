import pygame;
import pygame.font;

pygame.init()

# This File defines all the constants used for Colours, Sizes,...

# Sizes

# Game
FPS = 60
FRAMES_PER_SECOND = 60
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
GAME_SCALE = 2
CHARACTER_HEIGHT = 32
CHARACTER_WIDTH = 32
TILE_SIZE = 16 * GAME_SCALE
TILE_TYPES = 2

# Menu
BUTTON_SCALE = 1

# Player
SPEED = 5
OFFSET = 12

# Weapon
WEAPON_SCALE = 1.5
PENCIL_SPEED = 10
DAMAGE_FONT = pygame.font.Font("Game/assets/fonts/MainFont.ttf",35)
DAMAGE_BASE = 10
DAMAGE_EXTRA = 5

#GUI
HEART_SCALE = 3


# Backend
ROWS = 150
COLS = 150

# Colours
WHITE = (255, 255, 255)
RED = (255,0,0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
BACKGROUND = (40,25,25)
MENU_BG = (0,0,0)
WHITE = (255, 255, 255)
PANEL = (50,50,50)
YELLOW = (255,215,0)
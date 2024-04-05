import pygame;
import constants
import math

class Character():

    def __init__(self,x,y,health,animation_list, mob_type):
        self.mob_type = mob_type
        self.running = False
        self.health = health
        self.alive = True
        self.animation_list = animation_list[mob_type]
        self.frame_index = 0
        self.action = 0 # 0 = Idle | 1 = Down | 2 = Up | 3 = Right | 4 = Left
        self.updated_time = pygame.time.get_ticks()

        self.image = animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0,0,constants.TILE_SIZE*constants.GAME_SCALE, constants.TILE_SIZE*constants.GAME_SCALE)
        self.rect.center = (x/2,y/2)
    
    # Player Movement Function
    def move(self, dx, dy):
        # Diagonal Speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        self.rect.x += dx 
        self.rect.y += dy


    def update(self, action):
        # Check if Character is even alive
        if self.health <= 0:
            self.health = 0
            self.alive = False


        #Check which action player is performing
        self.update_action(action)

        animation_cooldown = 70
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.updated_time > animation_cooldown:
            self.frame_index += 1
            self.updated_time = pygame.time.get_ticks()
        
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            self.updated_time = pygame.time.get_ticks()


    

    def update_action(self,new_action):
        # Check if new Action is different
        if new_action != self.action:
            self.action = new_action
            # Update Animation Settings -> Sudden Changes update Index!
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        

    # Draw the Player Character
    def draw(self, surface):
        surface.blit(self.image,self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect,1)



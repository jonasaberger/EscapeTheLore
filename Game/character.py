import pygame;
import constants
import math

class Character():

    def __init__(self,x,y,health,animation_list, mob_type):
        self.score = 0
        self.mob_type = mob_type
        self.running = False
        self.health = health
        self.alive = True
        self.animation_list = animation_list[mob_type]
        self.frame_index = 0
        self.action = 0 # 0 = Idle | 1 = Down | 2 = Up | 3 = Right | 4 = Left
        self.updated_time = pygame.time.get_ticks()

        self.image = animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0,0,(constants.CHARACTER_WIDTH*constants.GAME_SCALE)/2, constants.CHARACTER_HEIGHT*constants.GAME_SCALE)
        self.rect.center = (x,y)
    
    # Player Movement Function
    def move(self, dx, dy):
        screen_scroll = [0,0]

        # Diagonal Speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        self.rect.x += dx 
        self.rect.y += dy

        # Only scroll screen if it's the player
        if self.mob_type == 0:
            # Update Scroll -> Move camera

            # Left & Right
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRES):
                screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRES) - self.rect.right
                self.rect.right = (constants.SCREEN_WIDTH - constants.SCROLL_THRES)

            if self.rect.left < constants.SCROLL_THRES:
                screen_scroll[0] = constants.SCROLL_THRES - self.rect.left
                self.rect.left = constants.SCROLL_THRES

            # Up & Down
            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRES):
                screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRES) - self.rect.bottom
                self.rect.bottom = (constants.SCREEN_HEIGHT - constants.SCROLL_THRES)

            if self.rect.top < constants.SCROLL_THRES:
                screen_scroll[1] = constants.SCROLL_THRES - self.rect.top
                self.rect.top = constants.SCROLL_THRES

            
        print(screen_scroll)
        return screen_scroll



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


    def ai(self, screen_scroll):
        # Reposition enemies based on screen_scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
    

    def update_action(self,new_action):
        # Check if new Action is different
        if new_action != self.action:
            self.action = new_action
            # Update Animation Settings -> Sudden Changes update Index!
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        

    # Draw the Player Character
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect.move(15,0), 1)




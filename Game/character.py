import pygame;
import constants
import math

class Character():

    def __init__(self,x,y,health,animation_list, mob_type,width,height):
        self.score = 0
        self.mob_type = mob_type
        self.running = False
        self.health = health
        self.alive = True
        self.animation_list = animation_list[mob_type]
        self.frame_index = 0
        self.action = 0 # 0 = Idle | 1 = Down | 2 = Up | 3 = Right | 4 = Left
        self.updated_time = pygame.time.get_ticks()

        self.hit = False
        self.last_hit = pygame.time.get_ticks() # Timer for when player received last hit
        self.stunned = False

        self.image = animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0,0,width, height)
        self.rect.center = (x,y)
    
    # Player Movement Function
    def move(self, dx, dy, obstacle_tiles):
        screen_scroll = [0,0]

        # Diagonal Speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        # Check for collission x
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                # Check which side it collides with
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                     self.rect.left = obstacle[1].right


        # Check for collission y
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                # Check which side it collides with
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

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

        return screen_scroll



    def update(self, action):
        # Check if Character is even alive
        if self.health <= 0:
            self.health = 0
            self.alive = False

        # Timer to reset player getting hit
        if self.mob_type == 0:
            if self.hit == True and (pygame.time.get_ticks() - self.last_hit) > constants.P_HIT_COOLDOWN:
                self.hit = False
            


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


    def ai(self, screen, player, obstacle_tiles, screen_scroll):
        
        # Movement Variables
        ai_dx = 2
        ai_dy = 0
        enemy_speed = 0
        enemy_range = 0
        enemy_damage = 0
        enemy_stun_cooldown = 0

        clipped_line = ()
        
        # Get the correct STATS for the specific mob-type
        if self.mob_type == 1:
            enemy_speed = constants.ABERGA_SPEED
            enemy_range = constants.ABERGA_RANGE
            enemy_damage = constants.ABERGA_DAMAGE
            enemy_stun_cooldown = constants.ABERGA_STUN_COOLDOWN


        # Reposition enemies based on screen_scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # Creating line of sight
        line_of_sight = ((self.rect.centerx,self.rect.centery),(player.rect.centerx,player.rect.centery))
         # Use this to demonstrate the line of sight -> comment out world.draw
         # pygame.draw.line(screen,constants.RED,line_of_sight[0],line_of_sight[1])

        # Check if the line_of_sight collides with a obstacle_tile
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)


        # Check distance to player -> Pythagoras
        distanceToPlayer = math.sqrt(((self.rect.centerx - player.rect.centerx)**2)+((self.rect.centery - player.rect.centery)**2))

        # Enemy has simple line of sight and moves to player
        if not clipped_line and distanceToPlayer > constants.RANGE:
            if self.rect.centerx > player.rect.centerx:
                ai_dx = -enemy_speed
            if self.rect.centerx < player.rect.centerx:
                ai_dx = enemy_speed

            if self.rect.centery > player.rect.centery:
                ai_dy = -enemy_speed
            if self.rect.centery < player.rect.centery:
                ai_dy = enemy_speed

        # Check if the enemy is even alive!
        if self.alive:

            if not self.stunned:
                # Move towards the Player
                self.move(ai_dx, ai_dy, obstacle_tiles)

                # Attack the Player
                if distanceToPlayer < enemy_range and player.hit == False:
                    player.health -= enemy_damage
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()


            # Check if hit
            if self.hit == True:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunned = True
                self.update_action(0)

            # Reset the stun timeout
            if (pygame.time.get_ticks() - self.last_hit > enemy_stun_cooldown):
                self.stunned = False


    

    def update_action(self,new_action):
        # Check if new Action is different
        if new_action != self.action:
            self.action = new_action
            # Update Animation Settings -> Sudden Changes update Index!
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        

    # Draw the Player Character
    def draw(self, surface):
        x_offset = (self.rect.width - self.image.get_width()) / 2
        y_offset = (self.rect.height - self.image.get_height()) / 2


        surface.blit(self.image, (self.rect.x + x_offset, self.rect.y + y_offset))
        pygame.draw.rect(surface, constants.RED, self.rect.move(0, 0), 1)




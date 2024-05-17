from asyncio import constants
from turtle import pen
import pygame
import math
import random
import constants

class Weapon():
    def __init__(self, image, pencil_image, outerWalls):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.pencil_image = pencil_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
        self.outerWalls = outerWalls
    
    def update(self, player):
        shot_cooldown = 300
        pencil = None

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)  # negative, because pygame y coords increase down the screen 
        self.angle = math.degrees(math.atan2(y_dist, x_dist)) 

        #get mouseclick
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
            pencil = Pencil(self.pencil_image, self.rect.centerx, self.rect.centery, self.angle, self.outerWalls)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        #reset mouse click
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False
        
        
        return pencil
    
    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))


class Pencil(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle, outerWalls): 
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center =  (x,y)
        self.outerWalls = outerWalls
        #calculate horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * constants.PENCIL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.PENCIL_SPEED) # -ve because pygame y coordinats increases down the screen 

    
    def update(self, screen_scroll, enemy_list):

        # Reset variables
        damage = 0
        damage_pos = 0
 
        #reposition based on speed
        self.rect.x = screen_scroll[0] + int(round(self.rect.x + self.dx))
        self.rect.y = screen_scroll[1] + int(round(self.rect.y + self.dy))

        #check if arrow has gone off screen 
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
           self.kill() 

        # Check for enemy-collision
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                # Calculate the damage delt
                damage = constants.P_DAMAGE_BASE + random.randint(0,constants.P_DAMAGE_EXTRA)
                damage_pos = enemy.rect
                enemy.health -= damage
                enemy.hit = True

                self.kill()
                break # Exit the for-loop


            for wall in self.outerWalls:
                if wall[1].colliderect(self.rect):
                    self.kill()

        return damage, damage_pos
    

        
        


    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))

class Fireball(pygame.sprite.Sprite):
  def __init__(self, image, x, y, target_x, target_y):
    pygame.sprite.Sprite.__init__(self)
    self.original_image = image
    x_dist = target_x - x
    y_dist = -(target_y - y)
    self.angle = math.degrees(math.atan2(y_dist, x_dist))
    self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    #calculate the horizontal and vertical speeds based on the angle
    self.dx = math.cos(math.radians(self.angle)) * constants.FIREBALL_SPEED
    self.dy = -(math.sin(math.radians(self.angle)) * constants.FIREBALL_SPEED)#-ve because pygame y coordiate increases down the screen


  def update(self, screen_scroll, player):
    #reposition based on speed
    self.rect.x += screen_scroll[0] + self.dx
    self.rect.y += screen_scroll[1] + self.dy

    #check if fireball has gone off screen
    if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
      self.kill()

    #check collision between self and player
    if player.rect.colliderect(self.rect) and player.hit == False:
      player.hit = True
      player.last_hit = pygame.time.get_ticks()
      player.health -= 10
      self.kill()


  def draw(self, surface):
    surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))

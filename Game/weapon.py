from asyncio import constants
from turtle import pen
import pygame
import math
import random
import constants

class Weapon():
    def __init__(self, image, pencil_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.pencil_image = pencil_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
    
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
            pencil = Pencil(self.pencil_image, self.rect.centerx, self.rect.centery, self.angle)
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
    def __init__(self, image, x, y, angle): 
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center =  (x,y)
        #calculate horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * constants.PENCIL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.PENCIL_SPEED) # -ve because pygame y coordinats increases down the screen 

    
    def update(self, enemy_list):

        # Reset variables
        damage = 0
        damage_pos = 0

        #reposition based on speed
        self.rect.x = int(round(self.rect.x + self.dx))
        self.rect.y = int(round(self.rect.y + self.dy))

        #check if arrow has gone off screen 
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
           self.kill() 

        # Check for enemy-collision
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                # Calculate the damage delt
                damage = 10 + random.randint(-5,5)
                damage_pos = enemy.rect
                enemy.health -= damage
                self.kill()
                break # Exit the for-loop

        return damage, damage_pos
        


    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))



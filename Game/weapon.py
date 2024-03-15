from turtle import pen
import pygame
import math

class Weapon():
    def __init__(self, image, pencil_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.pencil_image = pencil_image
        self.rect = self.image.get_rect()
    
    def update(self, player):
        pencil = None

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)  # negative, because pygame y coords increase down the screen 
        self.angle = math.degrees(math.atan2(y_dist, x_dist)) 

        #get mouseclick
        if pygame.mouse.get_pressed()[0]:
            pencil = Pencil(self.pencil_image, self.rect.centerx, self.rect.centery, self.angle)
        
        return pencil
    
    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))

class Pencil(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center =  (x,y)

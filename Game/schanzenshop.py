import pygame
import constants

class Schanzenshop(pygame.sprite.Sprite):
    def __init__(self,x,y,tile_texture):
        pygame.sprite.Sprite.__init__(self)
        self.tile_texture = tile_texture
        self.rect = pygame.rect.Rect(0,0,constants.SHOP_WIDTH,constants.SHOP_HEIGHT)
        self.rect.center = (x,y)
        self.hitbox = pygame.rect.Rect(0,0,self.rect.width+constants.SHOP_RANGE,self.rect.height+constants.SHOP_RANGE)
        self.hitbox.center = (x,y)
        self.music = 

    def update(self,screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        self.hitbox.x += screen_scroll[0]
        self.hitbox.y += screen_scroll[1]

    def draw(self,surface):
        pygame.draw.rect(surface,constants.WHITE,self.rect,1)
        pygame.draw.rect(surface,constants.RED,self.hitbox,1)
        surface.blit(self.tile_texture,self.rect)
        






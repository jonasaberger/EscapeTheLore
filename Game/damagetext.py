import pygame
import constants

class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = constants.DAMAGE_FONT.render(damage,True,color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    def update(self):
        # Move the Damage-Text upwards
        self.rect.y -= 1

        # Delete the counter after a small time period
        self.counter += 1
        if self.counter > 30:
            self.kill()
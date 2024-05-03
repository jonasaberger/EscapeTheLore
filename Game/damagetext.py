import pygame
import constants

class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = constants.MAIN_FONT.render(damage,True,color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    def update(self, screen_scroll):
        # Reposition based on screen_scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # Move the Damage-Text upwards
        self.rect.y -= 1

        # Delete the counter after a small time period
        self.counter += 1
        if self.counter > 30:
            self.kill()
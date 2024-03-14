import pygame;
import constants

class ScreenFade():
  def __init__(self, direction, colour, speed, screen):
    self.direction = direction
    self.colour = colour
    self.speed = speed
    self.fade_counter = 0
    self.screen = screen

  def fade(self):
    fade_complete = False
    self.fade_counter += self.speed
    if self.direction == 1: #whole screen fade
      pygame.draw.rect(self.screen, self.colour, (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
      pygame.draw.rect(self.screen, self.colour, (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
      pygame.draw.rect(self.screen, self.colour, (0, 0 - self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
      pygame.draw.rect(self.screen, self.colour, (0, constants.SCREEN_HEIGHT // 2 + self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    elif self.direction == 2: #vertical screen fade down
      pygame.draw.rect(self.screen, self.colour, (0, 0, constants.SCREEN_WIDTH, 0 + self.fade_counter))

    if self.fade_counter >= constants.SCREEN_WIDTH:
      fade_complete = True

    return fade_complete

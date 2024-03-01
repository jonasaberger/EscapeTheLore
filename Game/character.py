import pygame;
import constants
import math

class Character():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x,y)

    

        


    # Player Movement Function
    def move(self, dx, dy):

        def scale_player(playerImage):
            image_width = playerImage.get_width()
            image_height = playerImage.get_height()
            return pygame.transform.scale(playerImage, (image_width * constants.GAME_SCALE, image_height * constants.GAME_SCALE)) 


        if dx < 0:
            self.image = scale_player((pygame.image.load("Game/assets/images/characters/Player/Idle/Left/0.png").convert_alpha()))
        if dx > 0:
            self.image = scale_player((pygame.image.load("Game/assets/images/characters/Player/Idle/Right/0.png").convert_alpha()))

        if dy < 0:
            self.image = scale_player((pygame.image.load("Game/assets/images/characters/Player/Idle/Up/0.png").convert_alpha()))
        if dy > 0:
            self.image = scale_player((pygame.image.load("Game/assets/images/characters/Player/Idle/Down/0.png").convert_alpha()))


        # Diagonal Speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        self.rect.x += dx 
        self.rect.y += dy

        

    # Draw the Player Character
    def draw(self, surface):
        surface.blit(self.image,self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect,1)



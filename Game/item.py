import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list, dummy_coin = False):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type      #0: Coin, 1: Potion
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.dummy_coin = dummy_coin

    def update(self,screen_scroll, player, coin_fx, heal_fx): 
        # Not apply scroll to the "Score-Coin"
        if not self.dummy_coin: 
            # Reposition with the screen_scroll
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]


        #check to see if item has been collected by the player
        if self.rect.colliderect(player.rect):
            #coin collected
            if self.item_type == 0:
                player.score += 1
                coin_fx.play()
            elif self.item_type == 1:
                player.health += 10
                heal_fx.play()
                if player.health > 100:
                    player.health = 100
            self.kill()

        #handle animation
        animation_cooldown = 150
        #update image
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed since last update

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if the animation has finished
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0


    def draw(self, surface):
        surface.blit(self.image, self.rect)      
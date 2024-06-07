import pygame
import constants
from button import Button

class Schanzenshop(pygame.sprite.Sprite):
    def __init__(self,x,y,tile_texture):
        pygame.sprite.Sprite.__init__(self)
        self.tile_texture = tile_texture
        self.rect = pygame.rect.Rect(0,0,constants.SHOP_WIDTH,constants.SHOP_HEIGHT)
        self.rect.center = (x,y)
        self.hitbox = pygame.rect.Rect(0,0,self.rect.width+constants.SHOP_RANGE,self.rect.height+constants.SHOP_RANGE)
        self.hitbox.center = (x,y)

        self.buttonClicked = False
        self.schanzenshop_potion_price = constants.SHOP_POTION_BASE
        self.schanzenshop_brisn_price = constants.SHOP_BRISN_BASE
        self.schanzenshop_rockerflasche_price = constants.SHOP_ROCKERFLASCHE_BASE

    def update(self,screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        self.hitbox.x += screen_scroll[0]
        self.hitbox.y += screen_scroll[1]

    def draw(self,surface):
        # pygame.draw.rect(surface,constants.WHITE,self.rect,1)
        # pygame.draw.rect(surface,constants.RED,self.hitbox,1)
        surface.blit(self.tile_texture,self.rect)

    def drawInterface(self,screen,score_coin,schanzenshop_images,item_images,screen_scroll,player,coin_fx,heal_fx,pizza_fx,brisn_fx,draw_text,scale_img):
        screen.blit(schanzenshop_images[1], (0,50))
        score_coin.draw(screen)
        score_coin.update(screen_scroll,player,coin_fx,heal_fx,pizza_fx,brisn_fx)
        
        # Drachenshop buttons
        schanzenshop_potion = Button(210,585,scale_img(item_images[1],3))
        schanzenshop_potion_price = constants.SHOP_POTION_BASE

        schanzenshop_brisn = Button(538,585,scale_img(item_images[3],1.5))
        schanzenshop_brisn_price = constants.SHOP_BRISN_BASE

        schanzenshop_rockerflasche = Button(812,546,scale_img(item_images[4],5))
        schanzenshop_rockerflasche_price = constants.SHOP_ROCKERFLASCHE_BASE

        # Draw the prices
        draw_text(f"{self.schanzenshop_potion_price}",constants.MAIN_FONT,constants.WHITE,252,550)
        draw_text(f"{self.schanzenshop_brisn_price}",constants.MAIN_FONT,constants.WHITE,580, 550)
        draw_text(f"{self.schanzenshop_rockerflasche_price}",constants.MAIN_FONT,constants.WHITE,887, 550)

            # Lore-Getränk Logik
        if schanzenshop_potion.draw(screen) and self.buttonClicked != True:
            self.buttonClicked = True
            print("First Item Clicked")
            if player.score >= schanzenshop_potion_price: #type:ignore -> Exception
                player.score -= schanzenshop_potion_price #type:ignore -> Exception
                self.schanzenshop_potion_price += constants.SHOP_POTION_INCR
                player.health += constants.POTION_HEAL #type:ignore -> Exception
                heal_fx.play()

        if pygame.mouse.get_pressed()[0] == False:
            self.buttonClicked = False

        # Brisn Logik
        if schanzenshop_brisn.draw(screen) and self.buttonClicked != True:
            self.buttonClicked = True
            print("Second Item Bought")
            if player.score >= schanzenshop_brisn_price: #type:ignore -> Exception
                player.score -= schanzenshop_brisn_price #type:ignore -> Exception
                self.schanzenshop_brisn_price += constants.SHOP_BRISN_INCR
                brisn_fx.play()

                # Add the Brisn-Effect
                player.damage_boost += constants.BRISN_ATTACK_BOOST #type:ignore -> Exception
                player.health -= constants.BRISN_DAMAGE #type:ignore -> Exception

        if pygame.mouse.get_pressed()[0] == False:
            self.buttonClicked = False

        # Rocker-Flasche Logik
        if schanzenshop_rockerflasche.draw(screen) and self.buttonClicked != True:
            self.buttonClicked = True
            print("Third Item Bought")
            if player.score >= schanzenshop_rockerflasche_price: #type:ignore -> Exception
                player.score -= schanzenshop_rockerflasche_price #type:ignore -> Exception
                self.schanzenshop_rockerflasche_price = constants.SHOP_ROCKERFLASCHE_INCR

                # TODO Add the Rockerflasche-Effect
                player.isRocker = True

        if pygame.mouse.get_pressed()[0] == False:
            self.buttonClicked = False
        






# Class Entity
#       - Correspond à une entité de jeu


# Import des modules
import pygame
from game_config import *

class Entity(pygame.sprite.Sprite) :

    def __init__(self, x, y, height, width):
        pygame.sprite.Sprite.__init__(self)

        # Rect
        self.rect = pygame.Rect(x,
                    y,
                    width,
                    height)

        # Origin rect
        self.origin_rect = pygame.Rect(x,
                    y,
                    width,
                    height)

        # Vitesse de l'entité
        self.vx = 0
        self.vy = 0

    def advanced_state(self):
        # Gravity
        if self.rect.bottom > GameConfig.WINDOW_GAME_H:
            self.vy = 0
        else :
            self.vy = self.vy+GameConfig.GRAVITY*GameConfig.DT

        # Position
        x = self.origin_rect.left
        vx_min = -x/GameConfig.DT
        vx_max = (GameConfig.WINDOW_W-self.origin_rect.width-x)/GameConfig.DT
        self.vx = min(self.vx,vx_max)
        self.vx = max(self.vx,vx_min)
        self.origin_rect = self.origin_rect.move(self.vx*GameConfig.DT,self.vy*GameConfig.DT)

        self.rect.x = self.origin_rect.x
        self.rect.y = self.origin_rect.y


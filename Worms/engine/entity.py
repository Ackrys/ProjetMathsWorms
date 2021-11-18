# Class Entity
#       - Correspond à une entité de jeu


# Import des modules
import pygame
from game_config import *

class Entity(pygame.sprite.Sprite) :

    def __init__(self, x, y, height, width, mass):
        pygame.sprite.Sprite.__init__(self)

        # Rect
        self.rect = pygame.Rect(x,
                    y,
                    width,
                    height)

        # Display rect
        self.rect_display = pygame.Rect(x,
                    y,
                    width,
                    height)

        # Vitesse de l'entité
        self.vx = 0
        self.vy = 0

        # Offset
        self.x_offset = 0
        self.y_offset = 0

        # Mass
        self.mass = mass

    def advance_state(self):
        # Gravity
        if self.rect.bottom > GameConfig.WINDOW_H:
            self.vy = 0
        else :
            self.vy = self.vy+GameConfig.GRAVITY*GameConfig.DT*self.mass

        # Position
        x = self.rect.left
        vx_min = -x/GameConfig.DT
        vx_max = (GameConfig.WINDOW_W-self.rect.width-x)/GameConfig.DT
        self.vx = max(min(self.vx,vx_max), vx_min)
        self.rect = self.rect.move(self.vx*GameConfig.DT,self.vy*GameConfig.DT)

        self.rect_display.x = self.rect.x
        self.rect_display.y = self.rect.y

    def applyZoom(self, zoom):
        # Resize
        self.rect_display.height = self.rect.height * zoom
        self.rect_display.width = self.rect.width * zoom
        self.image_display = pygame.transform.scale(self.image, (
            self.image.get_rect().size[0] * zoom,
            self.image.get_rect().size[1] * zoom,
        )
        )

        # Move
        self.rect_display.x = self.rect.x * zoom
        self.rect_display.y = self.rect.y * zoom

    def applyOffset(self, x, y):
        self.x_offset = x
        self.y_offset = y


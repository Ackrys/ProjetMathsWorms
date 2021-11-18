# Class Worm
#       - Correspond à un ver


# Import des modules
import pygame
from game_config import *
from engine.entity import Entity


class Worm(Entity) :

    def __init__(self, x, y, height, width, mass):
        super().__init__(x, y, height, width, mass)

        self.image = GameConfig.WORM_IMG
        self.image_display = self.image

    def advance_state(self): 
        super().advance_state()

    def draw(self, screen):
        screen.blit(self.image_display, (self.rect_display.x + self.x_offset, self.rect_display.y + self.y_offset))

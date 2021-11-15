# Class Worm
#       - Correspond à un ver


# Import des modules
import pygame
from game_config import *
from engine.entity import Entity


class Worm(Entity) :

    def __init__(self, x, y, height, width):
        super().__init__(x, y, height, width)

        self.image = GameConfig.WORM_IMG
        self.origin_image = self.image

    def advanced_state(self): 
        super().advanced_state()

    def draw(self, window):
        window.blit(self.image, self.rect)


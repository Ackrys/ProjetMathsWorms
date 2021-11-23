# Class PMap
#           - Implémente la map

import pygame
import math
import random
from engine.map_image import MapImage

from game_config import *

class Map(pygame.sprite.Sprite) :


    # Initialisation

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Data
        self.image = MapImage(6)

        self.rect = self.image.rect
        self.mask = self.image.get_mask()


    # Advance State

    def advance_state(self):
        pass
        # self.image.advance_state()

    def isTouchingMap(self, object):
        return pygame.sprite.collide_mask(self, object)


    # Display methods
    def applyZoom(self, zoom):
        self.image.applyZoom(zoom)

    def applyOffset(self, x, y):
        self.image.applyOffset(x, y)

    def draw(self, screen):
        self.image.draw(screen)


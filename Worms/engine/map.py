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

    def is_touching_map(self, object):
        return pygame.sprite.collide_mask(self, object)

    def collision_point_with(self, object):
        collision_pixels = []
        map_image = self.image.get_noise_image()
        for w in range(object.rect.width):
            for h in range(object.rect.height):
                pos_x = object.rect.x + w
                pos_y = object.rect.y - self.rect.y + h
                if pos_x > 0 and pos_y > 0 and pos_x < map_image.get_width() and pos_y < map_image.get_height():
                    if map_image.get_at((pos_x, pos_y))[0] < 120:
                        collision_pixels.append((pos_x, pos_y))
        return collision_pixels


    # Display methods
    def applyZoom(self, zoom):
        self.image.applyZoom(zoom)

    def applyOffset(self, x, y):
        self.image.applyOffset(x, y)

    def draw(self, screen):
        self.image.draw(screen)


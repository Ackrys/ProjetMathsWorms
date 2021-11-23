# Class Worm
#       - Correspond à un ver

# Import des modules
import pygame
from game_config import *
from engine.animation import Animation
from engine.entity import Entity
import math


class Projectile(Entity):

    def __init__(self, x, y, height, width, mass):
        super().__init__(x, y, height, width, mass, "projectile_1.png")

    def draw(self, screen):
        screen.blit(
            self.image_display,
            (
                self.rect_display.x + self.x_offset,
                self.rect_display.y + self.y_offset
            )
        )

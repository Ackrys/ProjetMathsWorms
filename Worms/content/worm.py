# Class Worm
#       - Correspond à un ver

# Import des modules
import pygame
from game_config import *
from engine.animation import Animation
from engine.entity import Entity
import math
import time


class Worm(Entity) :

    def __init__(self, x, y, height, width, mass):
        super().__init__(x, y, height, width, mass, "standing.png")

        self.define_animation("idle", Animation(["standing.png"]))
        self.define_animation("walk_right", Animation(["R1.png", "R2.png", "R3.png", "R4.png", "R5.png", "R6.png", "R7.png", "R8.png", "R9.png"]))
        self.define_animation("walk_left", Animation(["L1.png", "L2.png", "L3.png", "L4.png", "L5.png", "L6.png", "L7.png", "L8.png", "L9.png"]))

    def advance_state(self):
        super().advance_state()

        # Gravity
        if self.rect.bottom >= GameConfig.WINDOW_H:
            self.vy = 0
        else:
            self.vy = self.vy+GameConfig.GRAVITY*GameConfig.DT*self.mass
    
    def has_touched_map(self, point, point_image, map_image):
        # self.rect.x et self.rect.y -> position du ver
        # self.rect.width et self.rect.height -> dimensions du ver
        # point[0] et point[1] -> position du point de collision (le plus en haut à gauche)
        # point_image[0] et point_image[1] -> position du point de collision dans l'image

        # map_image -> Image de la map
        # map_image.get_at(point) -> Couleur du pixel point
        #       point -> (x, y)
        # map_image.get_height() -> Hauteur de l'image de la map
        # map_image.get_width() -> Largeur de l'image de la map
        pass

    def draw(self, screen):
        super().draw(screen)

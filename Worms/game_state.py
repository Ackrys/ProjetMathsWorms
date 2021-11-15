# Class Game State
#       - Correspond à l'état de jeu


# Import des modules
import pygame
from game_config import GameConfig
from content.worm import *
from engine.camera import *

class GameState :
    def __init__(self):
        self.camera = Camera()

        self.worm = Worm(300, 150, 64, 64)

    def advance_state(self):
        self.move = None
        self.worm.advanced_state()

    def draw(self, window):
        pygame.draw.rect(window,(0, 0, 255),
            (200,150,100,50)
        )

        GameConfig.WINDOW_GAME_H = GameConfig.WINDOW_H * self.camera.zoom
        GameConfig.WINDOW_GAME_W = GameConfig.WINDOW_W * self.camera.zoom

        if self.camera.zoom != 1: # Zoom camera
            # Resize
            self.worm.rect.height = self.worm.origin_rect.height * self.camera.zoom
            self.worm.rect.width = self.worm.origin_rect.width * self.camera.zoom
            self.worm.image = pygame.transform.scale(self.worm.image, (
                self.worm.origin_image.get_rect().size[0] * self.camera.zoom,
                self.worm.origin_image.get_rect().size[1] * self.camera.zoom,
            )
            )

            # Move
            if self.camera.zoom > 1 :
                self.worm.rect.x = self.worm.origin_rect.x - self.worm.rect.width + self.worm.origin_rect.width
                self.worm.rect.y = self.worm.origin_rect.y - self.worm.rect.height + self.worm.origin_rect.height
            else :
                self.worm.rect.x = self.worm.origin_rect.x + self.worm.rect.width - self.worm.origin_rect.width
                self.worm.rect.y = self.worm.origin_rect.y + self.worm.rect.height - self.worm.origin_rect.height

        if (self.camera.zoom < 1.1) :
            self.camera.zoom_by(0.05)


        self.worm.draw(window)
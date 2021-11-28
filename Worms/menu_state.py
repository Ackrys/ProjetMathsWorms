# Class Game State
#       - Correspond à l'état de jeu

# Pygame
import pygame

# Game Config
from game_config import GameConfig

# Engine
from engine.camera import *
from engine.animation import *
from engine.scene import *
from engine.map_image import *
from engine.map import *
from engine.ui import *

from content.worm import *

class MenuState :

    # Initialisation

    def __init__(self):
        # Camera
        self.camera = Camera()

        # Scene
        self.scene = Scene()

        # Play Button
        button_height = 40
        button_width = 40

        self.play_button = UI(GameConfig.WINDOW_W // 2 - button_width // 2, GameConfig.WINDOW_H // 2 - button_height // 2, button_height, button_width, "standing.png")

        self.scene.add_ui(self.play_button)

        self.loading_screen = UI(0, 0, GameConfig.WINDOW_W, GameConfig.WINDOW_H, "standing.png")

    # Advance state
    def advance_state(self, click, pos_click):
        if click and self.play_button.is_clicked_on(pos_click):
            return False
        self.scene.advance_state()
        return True

    # Display
    def draw(self, screen):
        # self.scene.draw(screen, self.camera)
        self.scene.draw_ui(screen, self.camera)

    def draw_loading(self, screen):
        self.loading_screen.draw(screen)
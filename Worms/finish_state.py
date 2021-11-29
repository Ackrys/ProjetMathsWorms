# Class Finish State
#       - Correspond à l'état de jeu terminé

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

class FinishState:

    # Initialisation

    def __init__(self, winner):
        # Camera
        self.camera = Camera()

        # Scene
        self.scene = Scene()

        # Play Button
        button_height = 40
        button_width = 40

        self.replay_button = UI(GameConfig.WINDOW_W // 2 - button_width // 2, GameConfig.WINDOW_H // 2 - button_height // 2, button_height, button_width, "play_button.png")
        self.quit_button = UI(GameConfig.WINDOW_W // 2 - button_width // 2, GameConfig.WINDOW_H // 2 - button_height // 2 + 100, button_height, button_width, "quit_button.png")

        self.scene.add_ui(self.replay_button)
        self.scene.add_ui(self.quit_button)

        self.title = GameConfig.FONT_TITLE.render("Worms", True, GameConfig.COLOR_BLACK)

        self.loading_screen = GameConfig.FONT_MAIN.render("Equipe " + str(winner) + " a gagne", True, GameConfig.COLOR_BLACK)

    # Advance state
    def advance_state(self, click, pos_click):
        if click and self.replay_button.is_clicked_on(pos_click):
            return False
        elif click and self.quit_button.is_clicked_on(pos_click):
            pygame.quit()
            quit()
        self.scene.advance_state()
        return True

    # Display
    def draw(self, screen):
        # self.scene.draw(screen, self.camera)
        self.scene.draw_ui(screen, self.camera)
        screen.blit(
            self.title,
            (GameConfig.WINDOW_W // 2 - self.title.get_width() // 2, 20)
        )
        screen.blit(
            self.loading_screen,
            (GameConfig.WINDOW_W // 2 - self.title.get_width() // 2, GameConfig.WINDOW_H // 2 - self.title.get_height() // 2)
        )
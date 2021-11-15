# Class Game State
#       - Correspond à l'état de jeu


# Import des modules
import pygame

class GameState :
    def __init__(self):
        self.player = None

    def advance_state(self):
        self.move = None

    def draw(self, window):
        pygame.draw.rect(window,(0, 0, 255),
            (200,150,100,50)
        )

# Class Game State
#       - Correspond à l'état de jeu


# Import des modules
from player import *


class GameState :
    def __init__(self):
        self.player = Player(20)

    def advance_state(self,next_move):
        self.player.advance_state(next_move)

    def draw(self, window):
        window.blit(GameConfig.BACKGROUND_IMG,(0,0))
        self.player.draw(window)



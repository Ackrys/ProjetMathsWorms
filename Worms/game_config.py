# Class Game Config
#       - Contient les constantes de jeu


# Import des modules
import pygame
import os


class GameConfig :
    ASSET_FOLDER = os.path.join('Worms', 'assets')

    # Dimensions fenêtre
    WINDOW_H = 640
    WINDOW_W = 960

    # Gravité
    GRAVITY = 9.81

    def init():
        GameConfig.img = None


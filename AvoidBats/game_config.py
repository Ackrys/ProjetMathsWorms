# Class Game Config
#       - Contiens les constantes de jeu


# Import des modules
import pygame
import os


class GameConfig :
    ASSET_FOLDER = 'AvoidBats/assets'

    WINDOW_H = 640
    WINDOW_W = 960

    Y_PLATEFORM = 516

    # Init
    def init() :
        GameConfig.BACKGROUND_IMG = GameConfig.loadImage('background.png')

    # Fonction chargeant une image avec un chemin démarrant au dossier 'assets'
    def loadImage(image_path) :
        return pygame.image.load(os.path.join(GameConfig.ASSET_FOLDER, image_path))


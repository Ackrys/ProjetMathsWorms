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

    # Constante
    DT = 0.3

    # Gravité
    GRAVITY = 9.81

    def init():
        GameConfig.WORM_IMG = GameConfig.loadImage("standing.png")

    # Fonction chargeant une image avec un chemin démarrant au dossier 'assets'
    def loadImage(image_path) :
        return pygame.image.load(os.path.join(GameConfig.ASSET_FOLDER, image_path))

    # Fonction chargeant une image transparante
    def loadImageAlpha(image_path) :
        return GameConfig.loadImage(image_path).convert_alpha()

    # Fonction chargeant une font avec un chemin démarrant au dossier 'assets'
    def loadFont(font, size) :
        return pygame.font.Font(os.path.join(GameConfig.ASSET_FOLDER, font), size)

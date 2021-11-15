# Class Game Config
#       - Contiens les constantes de jeu


# Import des modules
import pygame
import os


class GameConfig :
    ASSET_FOLDER = 'AvoidBats/assets'

    # Dimensions fenêtre
    WINDOW_H = 640
    WINDOW_W = 960

    # Plateforme Y
    Y_PLATEFORM = 516

    # Dimensions joueur
    PLAYER_W = 64
    PLAYER_H = 64

    # Mouvements
    DT = 0.5
    FORCE_LEFT = -20
    FORCE_RIGHT = -FORCE_LEFT

    # Gravité
    GRAVITY = 9.81
    FORCE_JUMP = -100

    # Init
    def init() :
        GameConfig.BACKGROUND_IMG = GameConfig.loadImage('background.png')
        GameConfig.STANDING_IMG = GameConfig.loadImage('standing.png')

    # Fonction chargeant une image avec un chemin démarrant au dossier 'assets'
    def loadImage(image_path) :
        return pygame.image.load(os.path.join(GameConfig.ASSET_FOLDER, image_path))


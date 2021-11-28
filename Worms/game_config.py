# Class Game Config
#       - Contient les constantes de jeu


# Import des modules
import pygame
import os


class GameConfig :
    ASSET_FOLDER = os.path.join('Worms', 'assets')

    PI = 3.14

    # Dimensions fenêtre
    WINDOW_H = 640
    WINDOW_W = 960

    # Dimensions fenêtre de jeu
    WINDOW_GAME_H = WINDOW_H
    WINDOW_GAME_W = WINDOW_W

    # Caméra
    CAMERA_ZOOM_SPEED = 0.01
    CAMERA_MOVE_SPEED = 4

    # Constante DeltaTime
    DT = 0.3

    # Gravité
    GRAVITY = 9.81



    # Worm
    WORM_SPEED = 10
    WORM_JUMP_FORCE = 30

    WORM_HEIGHT = 64
    WORM_WIDTH = 64

    WORM_HP = 100

    # Projectile
    MASS_PROJ = 5
    GRAVITY = 9.81


    # Color
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_GROUND = (126, 70, 60)
    COLOR_SKY = (100, 220, 250)

    def init():
        pass

    # Fonction chargeant une image avec un chemin démarrant au dossier 'assets'
    def loadImage(image_path) :
        return pygame.image.load(os.path.join(GameConfig.ASSET_FOLDER, image_path))

    # Fonction chargeant une image transparante
    def loadImageAlpha(image_path) :
        return GameConfig.loadImage(image_path).convert_alpha()

    # Fonction chargeant une font avec un chemin démarrant au dossier 'assets'
    def loadFont(font, size) :
        return pygame.font.Font(os.path.join(GameConfig.ASSET_FOLDER, font), size)

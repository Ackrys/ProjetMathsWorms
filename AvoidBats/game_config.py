# Class Game Config
#       - Contiens les constantes de jeu


# Import des modules
import pygame
import os


class GameConfig :
    ASSET_FOLDER = os.path.join('AvoidBats', 'assets')

    # Dimensions fenêtre
    WINDOW_H = 640
    WINDOW_W = 960

    # Plateforme Y
    Y_PLATEFORM = 516

    # Couleur
    GREY = (51,51,0)

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


    # Bats
    BAT_W = 32
    BAT_H = 32
    TICKS_BETWEEN_BATS = 100
    BAT_MIN_SPEED = 15
    BAT_MAX_SPEED = 30

    # Animation
    NB_FRAMES_PER_SPRITE_PLAYER = 2
    NB_FRAMES_PER_SPRITE_BAT = 3

    # Init
    def init() :
        # Décor
        GameConfig.BACKGROUND_IMG = GameConfig.loadImage('background.png')

        # Joueur
        GameConfig.WALK_RIGHT_IMG = [
            GameConfig.loadImageAlpha('R'+str(i)+'.png') for i in range(1, 10)
        ]
        GameConfig.WALK_LEFT_IMG = [
            GameConfig.loadImageAlpha('L'+str(i)+'.png') for i in range(1, 10)
        ]
        GameConfig.STANDING_IMG = [
            GameConfig.loadImageAlpha('standing.png')
        ]


        GameConfig.WALK_RIGHT_MASKS = [
            pygame.mask.from_surface(im) for im in GameConfig.WALK_RIGHT_IMG
        ]
        GameConfig.WALK_LEFT_MASKS = [
            pygame.mask.from_surface(im) for im in GameConfig.WALK_LEFT_IMG
        ]
        GameConfig.STANDING_MASK = [
            pygame.mask.from_surface(GameConfig.STANDING_IMG[0])
        ]

        # Chauve-souris
        GameConfig.FLYING_FROM_RIGHT =[
            GameConfig.loadImageAlpha('bat'+str(i)+'.png') for i in range(1,6)
         ]
        GameConfig.FLYING_FROM_LEFT =[
            pygame.transform.flip(im,True,False)
            for im in GameConfig.FLYING_FROM_RIGHT
        ]
        GameConfig.FLYING_FROM_RIGHT_MASKS = [
            pygame.mask.from_surface(im)
            for im in GameConfig.FLYING_FROM_RIGHT
        ]
        GameConfig.FLYING_FROM_LEFT_MASKS = [
            pygame.mask.from_surface(im)
            for im in GameConfig.FLYING_FROM_LEFT
        ]


        # Police
        GameConfig.FONT150 = GameConfig.loadFont('BradBunR.ttf',150)
        GameConfig.FONT20 = GameConfig.loadFont('BradBunR.ttf', 20)

    # Fonction chargeant une image avec un chemin démarrant au dossier 'assets'
    def loadImage(image_path) :
        return pygame.image.load(os.path.join(GameConfig.ASSET_FOLDER, image_path))

    # Fonction chargeant une image transparante
    def loadImageAlpha(image_path) :
        return GameConfig.loadImage(image_path).convert_alpha()

    # Fonction chargeant une font avec un chemin démarrant au dossier 'assets'
    def loadFont(font, size) :
        return pygame.font.Font(os.path.join(GameConfig.ASSET_FOLDER, font), size)

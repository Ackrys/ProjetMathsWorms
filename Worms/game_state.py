# Class Game State
#       - Correspond à l'état de jeu


# Import des modules
import pygame
from game_config import GameConfig
from content.worm import *

# Engine
from engine.decor import *
from engine.camera import *

class GameState :
    def __init__(self):
        self.camera = Camera()

        self.worm = Worm(300, 150, 64, 64)
        self.background = Decor(0, 0, GameConfig.WINDOW_W, GameConfig.WINDOW_H, "background.png")

        self.objects = []
        self.objects.append(self.worm)
        self.objects.append(self.background)

        self.count = 0

    def advance_state(self, inputs):
        # Window Resize
        GameConfig.WINDOW_GAME_H = GameConfig.WINDOW_H * self.camera.zoom
        GameConfig.WINDOW_GAME_W = GameConfig.WINDOW_W * self.camera.zoom

        # Camera zoom
        if inputs.zoom_in:
            self.camera.zoom_by(-0.01)
        if inputs.zoom_out:
            self.camera.zoom_by(0.01)

        # Camera movement
        camera_moved = False
        if inputs.up :
            self.camera.move_by(0, 2)
            camera_moved = True
        if inputs.down :
            self.camera.move_by(0, -2)
            camera_moved = True
        if inputs.left :
            self.camera.move_by(2, 0)
            camera_moved = True
        if inputs.right :
            self.camera.move_by(-2, 0)
            camera_moved = True

        if camera_moved:
            for i in range(len(self.objects)):
                currentObject = self.objects[i]
                currentObject.applyOffset(self.camera.x, self.camera.y)

        # Advance state
        self.worm.advance_state()
        # self.background.advance_state()

    def draw(self, window):

        for i in range(len(self.objects)):
            currentObject = self.objects[i]
            if self.camera.zoom != 1:
                currentObject.applyZoom(self.camera.zoom)


        self.background.draw(window)
        self.worm.draw(window)
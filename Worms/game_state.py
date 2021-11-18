# Class Game State
#       - Correspond à l'état de jeu


# Import des modules
import pygame
from engine.animation import Animation
from game_config import GameConfig
from content.worm import *

# Engine
from engine.decor import *
from engine.camera import *

class GameState :
    def __init__(self):
        # Array of all objects in scene
        self.objects = []

        # Camera
        self.camera = Camera()

        # Objects
        self.worm = Worm(300, 150, 64, 64, 1)

        self.background = Decor(0, 0, GameConfig.WINDOW_W, GameConfig.WINDOW_H, "background.png")
        
        self.worm_2 = Decor(400, 200, 64, 64, "standing.png")
        self.worm_2.define_animation("right", Animation(["R1.png", "R2.png", "R3.png", "R4.png", "R5.png", "R6.png", "R7.png", "R8.png", "R9.png"]))
        self.worm_2.set_animation("right")

        self.objects.append(self.background)
        self.objects.append(self.worm)
        self.objects.append(self.worm_2)

    def advance_state(self, inputs):
        # Window Resize
        GameConfig.WINDOW_GAME_H = GameConfig.WINDOW_H * self.camera.zoom
        GameConfig.WINDOW_GAME_W = GameConfig.WINDOW_W * self.camera.zoom

        # Camera zoom
        if inputs.camera_zoom_in:
            self.camera.zoom_by(-GameConfig.CAMERA_ZOOM_SPEED)
        if inputs.camera_zoom_out:
            self.camera.zoom_by(GameConfig.CAMERA_ZOOM_SPEED)

        # Camera movement
        camera_moved = False
        if inputs.camera_up:
            self.camera.move_by(0, GameConfig.CAMERA_MOVE_SPEED)
            camera_moved = True
        if inputs.camera_down:
            self.camera.move_by(0, -GameConfig.CAMERA_MOVE_SPEED)
            camera_moved = True
        if inputs.camera_left:
            self.camera.move_by(GameConfig.CAMERA_MOVE_SPEED, 0)
            camera_moved = True
        if inputs.camera_right:
            self.camera.move_by(-GameConfig.CAMERA_MOVE_SPEED, 0)
            camera_moved = True

        if inputs.player_move_left:
            self.worm.vx = -GameConfig.WORM_SPEED
            self.worm.set_animation("walk_left")
        if inputs.player_move_right:
            self.worm.vx = GameConfig.WORM_SPEED
            self.worm.set_animation("walk_right")
        if not inputs.player_move_left and not inputs.player_move_right:
            self.worm.vx = 0
            self.worm.set_animation("idle")

        if camera_moved:
            for i in range(len(self.objects)):
                currentObject = self.objects[i]
                currentObject.applyOffset(self.camera.x, self.camera.y)

        # Advance state
        for i in range(len(self.objects)):
            currentObject = self.objects[i]
            currentObject.advance_state()

    def draw(self, window):
        for i in range(len(self.objects)):
            currentObject = self.objects[i]
            if self.camera.zoom != 1:
                currentObject.applyZoom(self.camera.zoom)
            currentObject.draw(window)

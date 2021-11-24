# Class Game State
#       - Correspond à l'état de jeu


# Pygame
import pygame
from content.projectile import Projectile
from engine.map import Map

# Game Config
from game_config import GameConfig

# Engine
from engine.decor import *
from engine.camera import *
from engine.animation import *
from engine.scene import *
from engine.map_image import *

from content.worm import *

class GameState :
    def __init__(self):
        # Scene
        self.scene = Scene()
        self.collision_worm = False
        self.collision_point = (0, 0)

        # Map
        self.map = Map()
        self.scene.load_map(self.map)

        # Camera
        self.camera = Camera()

        # Objects
        self.worm = Worm(300, 150, 64, 64, 1)

        #self.background = Decor(0, 0, GameConfig.WINDOW_W, GameConfig.WINDOW_H, "background.png")

        #self.worm_2 = Decor(450, 600, 64, 64, "standing.png")
        #self.worm_2.define_animation("right", Animation(["R1.png", "R2.png", "R3.png", "R4.png", "R5.png", "R6.png", "R7.png", "R8.png", "R9.png"]))
        #self.worm_2.set_animation("right")

        self.scene.add_object(self.worm)
        #self.scene.add_object(self.worm_2)

        # Projectile
        self.projectile = None

    def advance_state(self, inputs):
        # Window Resize
        GameConfig.WINDOW_GAME_H = GameConfig.WINDOW_H * self.camera.zoom
        GameConfig.WINDOW_GAME_W = GameConfig.WINDOW_W * self.camera.zoom

        # Camera movement
        if inputs.camera_up:
            self.camera.move_by(0, GameConfig.CAMERA_MOVE_SPEED)
        if inputs.camera_down:
            self.camera.move_by(0, -GameConfig.CAMERA_MOVE_SPEED)
        if inputs.camera_left:
            self.camera.move_by(GameConfig.CAMERA_MOVE_SPEED, 0)
        if inputs.camera_right:
            self.camera.move_by(-GameConfig.CAMERA_MOVE_SPEED, 0)

        # Player movement
        if inputs.player_move_left:
            self.worm.vx = -GameConfig.WORM_SPEED
            self.worm.set_animation("walk_left")
        if inputs.player_move_right:
            self.worm.vx = GameConfig.WORM_SPEED
            self.worm.set_animation("walk_right")
        if inputs.player_move_up and self.worm.touch_down == True:
            print(self.worm.touch_down)
            self.worm.vy = -GameConfig.JUMP_FORCE
            self.worm.set_animation("walk_left")
        if not inputs.player_move_left and not inputs.player_move_right:
            self.worm.vx = 0
            self.worm.set_animation("idle")

        # Player action
        if inputs.player_shoot and self.projectile==None:
            self.projectile = Projectile(self.worm, 20, 20, 5)
            self.scene.add_object(self.projectile)

        #projectile_colision
        if self.projectile!=None and (self.map.is_touching_map(self.projectile) or self.projectile.out_window()==True):
            self.scene.remove_object(self.projectile)
            self.projectile=None

        # Collisions
        collision_points = self.map.collision_point_with(self.worm)
        if len(collision_points) > 0:
            self.collision_worm = True
            self.collision_point = collision_points
            # print(collision_point_temp)
            if len(collision_points) > 0 :
                self.worm.has_touched_map(collision_points)
        else:
            self.worm.points = []
            self.collision_worm = False
            self.collision_point = (0, 0)

        # Camera zoom
        if inputs.camera_zoom_in:
            self.camera.zoom_by(-GameConfig.CAMERA_ZOOM_SPEED)
        if inputs.camera_zoom_out:
            self.camera.zoom_by(GameConfig.CAMERA_ZOOM_SPEED)

        # Camera follow
        self.scene.applyOffset(self.camera.x, self.camera.y)

        # Advance state
        self.scene.advance_state()

    def draw(self, screen):
        self.scene.draw(screen, self.camera)
        if self.collision_worm :
            for pixel in self.collision_point:
                x = pixel[0] + self.camera.x
                y = pixel[1] + self.camera.y + self.map.image.rect.y
                pygame.draw.rect(screen, (255, 0, 0), (x * self.camera.zoom, y * self.camera.zoom, 1, 1))

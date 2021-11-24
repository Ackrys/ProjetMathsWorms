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

        # Camera follow
        if camera_moved:
            self.scene.applyOffset(self.camera.x, self.camera.y)

        # Player movement
        if inputs.player_move_left:
            self.worm.vx = -GameConfig.WORM_SPEED
            self.worm.set_animation("walk_left")
        if inputs.player_move_right:
            self.worm.vx = GameConfig.WORM_SPEED
            self.worm.set_animation("walk_right")
        if not inputs.player_move_left and not inputs.player_move_right:
            self.worm.vx = 0
            self.worm.set_animation("idle")

        # Player action
        if inputs.player_shoot:
            self.projectile = Projectile(self.worm.rect.x, self.worm.rect.y, 20, 20, 5)
            self.scene.add_object(self.projectile)

        # Collisions
        if self.map.is_touching_map(self.worm):
            self.collision_worm = True
            collision_point_temp, collision_point_on_image = self.map.collision_point_with(self.worm)
            # print(collision_point_temp)
            if collision_point_temp != None:
                self.collision_point = (collision_point_temp[0] * self.camera.zoom, collision_point_temp[1] * self.camera.zoom)
                self.worm.has_touched_map(collision_point_temp, collision_point_on_image, self.map.image.get_noise_image())
        else:
            self.collision_worm = False
            self.collision_point = (0, 0)

        # Advance state
        self.scene.advance_state()

    def draw(self, screen):
        self.scene.draw(screen, self.camera)
        if self.collision_worm:
            pygame.draw.rect(screen, (255, 0, 0), (self.collision_point[0] + self.camera.x, self.collision_point[1] + self.camera.y, 4, 4))


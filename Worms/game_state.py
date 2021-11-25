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


    # Initialisation

    def __init__(self):
        # Camera
        self.camera = Camera()

        # Scene
        self.scene = Scene()
        self.collision_worm = False
        self.collision_point = (0, 0)

        # Map
        self.map = Map()
        self.scene.load_map(self.map)

        # Worms
        self.team_blue = []
        self.team_red = []

        self.team_blue.append(Worm(100, 100, GameConfig.WORM_WIDTH, GameConfig.WORM_WIDTH, 1, self.map))
        # self.team_blue.append(Worm(200, 100, GameConfig.WORM_WIDTH, GameConfig.WORM_WIDTH, 1, self.map))
        # self.team_blue.append(Worm(300, 100, GameConfig.WORM_WIDTH, GameConfig.WORM_WIDTH, 1, self.map))

        self.team_red.append(Worm(400, 100, GameConfig.WORM_WIDTH, GameConfig.WORM_WIDTH, 1, self.map))
        # self.team_red.append(Worm(500, 100, GameConfig.WORM_WIDTH, GameConfig.WORM_WIDTH, 1, self.map))
        # self.team_red.append(Worm(600, 100, GameConfig.WORM_WIDTH, GameConfig.WORM_WIDTH, 1, self.map))

        self.actual_team = "BLUE"
        self.actual_worm = self.team_blue[0]

        for worm in self.team_blue:
            self.scene.add_object(worm)

        for worm in self.team_red:
            self.scene.add_object(worm)

        # Projectile
        self.projectile = None

        # Game State Management
        self.state_is_firing = False


    # Advance state
    def advance_state(self, inputs):
        self.handle_inputs(inputs)

        # Projectile Collision
        if self.projectile != None and (self.map.is_touching_map(self.projectile) or self.projectile.out_window()==True):
            self.scene.remove_object(self.projectile)
            self.projectile=None
            self.next_worm()

        # Worm Collisions
        if self.state_is_firing:
            self.handle_worm_collision(self.actual_worm)
        else:
            for worm in self.team_blue:
                self.handle_worm_collision(worm)

            for worm in self.team_red:
                self.handle_worm_collision(worm)

        # Camera follow
        self.scene.applyOffset(self.camera.x, self.camera.y)

        # Advance state
        self.scene.advance_state()

    def handle_inputs(self, inputs):
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

        # Camera zoom
        if inputs.camera_zoom_in:
            self.camera.zoom_by(-GameConfig.CAMERA_ZOOM_SPEED)
        if inputs.camera_zoom_out:
            self.camera.zoom_by(GameConfig.CAMERA_ZOOM_SPEED)

        # Player movement
        if inputs.player_move_left:
            self.actual_worm.vx = -GameConfig.WORM_SPEED
            self.actual_worm.set_animation("walk_left")
        if inputs.player_move_right:
            self.actual_worm.vx = GameConfig.WORM_SPEED
            self.actual_worm.set_animation("walk_right")
        if inputs.player_move_up and self.actual_worm.touch_down == True:
            if not self.actual_worm.is_jumping:
                self.actual_worm.vy = -GameConfig.WORM_JUMP_FORCE
                self.actual_worm.is_jumping = True
        if not inputs.player_move_left and not inputs.player_move_right:
            self.actual_worm.vx = 0
            self.actual_worm.set_animation("idle")

        # Player action
        if inputs.player_shoot and self.projectile == None:
            self.projectile = Projectile(self.actual_worm, 20, 20, GameConfig.MASS_PROJ, -1, -1, self.camera)
            self.scene.add_object(self.projectile)

    # Worm management
    def handle_worm_collision(self, worm):
        collision_points = self.map.collision_point_with(worm)
        if len(collision_points) > 0:
            self.collision_worm = True
            self.collision_point = collision_points
            worm.has_touched_map(collision_points)
            worm.is_jumping = False
        else:
            worm.points = []
            self.collision_worm = False
            self.collision_point = (0, 0)
    
    def next_worm(self):
        self.actual_worm.vx = 0
        self.actual_worm.set_animation("idle")
        if self.actual_worm == self.team_blue[0]:
            self.actual_worm = self.team_red[0]
            self.actual_team = "RED"
            print("Tour Red")
        elif self.actual_worm == self.team_red[0]:
            self.actual_worm = self.team_blue[0]
            self.actual_team = "BLUE"
            print("Tour Blue")
        # elif self.actual_worm == self.team_blue[1]:
        #     self.actual_worm = self.team_red[1]
        #     self.actual_team = "RED"
        # elif self.actual_worm == self.team_red[1]:
        #     self.actual_worm = self.team_blue[2]
        #     self.actual_team = "BLUE"
        # elif self.actual_worm == self.team_blue[2]:
        #     self.actual_worm = self.team_red[2]
        #     self.actual_team = "RED"
        # elif self.actual_worm == self.team_red[2]:
        #     self.actual_worm = self.team_blue[0]
        #     self.actual_team = "BLUE"
        # Le worm qui joue est ennemi
        # if self.actual_team == "RED":
        self.actual_worm.worm_brain(self.team_blue[0], self.camera, self.scene)
        

    # Display
    def draw(self, screen):
        self.scene.draw(screen, self.camera)
        #if self.collision_worm :
        #    for pixel in self.collision_point:
        #        x = pixel[0] + self.camera.x
        #        y = pixel[1] + self.camera.y + self.map.image.rect.y
        #        pygame.draw.rect(screen, (255, 0, 0), (x * self.camera.zoom, y * self.camera.zoom, 1, 1))

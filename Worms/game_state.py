# Class Game State
#       - Correspond à l'état de jeu

# Pygame
import pygame
from content.projectile import Projectile
from content.fake_projectile import FakeProjectile
from content.worm import Worm

# Game Config
from game_config import GameConfig

# Engine
from engine.camera import *
from engine.animation import *
from engine.scene import *
from engine.map_image import *
from engine.map import *
from engine.ui import *

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
        self.fake_projectile = None

        # Game State Management
        self.state_is_firing = False

    # Advance state
    def advance_state(self, inputs):
        self.handle_inputs(inputs)

        # Projectile Collision
        if self.projectile != None and (self.map.is_touching_map(self.projectile) or self.projectile.out_window() or self.projectile_collision_with_worm()):
            self.handle_damages()
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
            self.actual_enemy = self.team_blue[0]
            # IA
            new_projectile = self.actual_worm.worm_brain(self.actual_enemy, self.camera)
            self.projectile = new_projectile
            self.scene.add_object(new_projectile)
            self.actual_team = "RED"
            print("Tour Red")
        elif self.actual_worm == self.team_red[0]:
            self.actual_worm = self.team_blue[0]
            self.actual_enemy = self.team_red[0]
            self.actual_team = "BLUE"
            print("Tour Blue")

        # if self.actual_worm == None:
            # self.next_worm()
        
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
        
    def handle_damages(self):
        for worm in self.team_blue:
            distance = self.scene.distance_between_objects(self.projectile, worm)
            if distance < 120:
                damages = self.projectile.damage / (distance / 50)
                if distance < 50:
                    damages = self.projectile.damage

                if worm.take_damages(damages):
                    self.scene.remove_object(worm)
                    self.team_blue[self.team_blue.index(worm)] = None
                    break
        for worm in self.team_red:
            distance = self.scene.distance_between_objects(self.projectile, worm)
            if distance < 120:
                damages = self.projectile.damage / (distance / 50)
                if distance < 50:
                    damages = self.projectile.damage

                if worm.take_damages(damages):
                    self.scene.remove_object(worm)
                    self.team_red[self.team_red.index(worm)] = None
                    break

    def projectile_collision_with_worm(self):
        for worm in self.team_blue:
            if self.scene.areColliding(self.projectile, worm) and worm != self.actual_worm:
                return True
        for worm in self.team_red:
            if self.scene.areColliding(self.projectile, worm) and worm != self.actual_worm:
                return True

    # Display
    def draw(self, screen):
        self.scene.draw(screen, self.camera)
        if self.actual_team == "BLUE":
            self.draw_projectile_projection(screen)
        self.scene.draw_ui(screen, self.camera)

    def draw_projectile_projection(self, screen):
        self.fake_projectile = FakeProjectile(self.actual_worm, 20, 20, GameConfig.MASS_PROJ, self.camera)
        for i in range(0, 200):
            x_projection, y_projection = self.fake_projectile.pull(i)
            x_projection_2, y_projection_2 = self.fake_projectile.pull(i + 1)
            x_projection *= self.camera.zoom
            y_projection *= self.camera.zoom
            x_projection_2 *= self.camera.zoom
            y_projection_2 *= self.camera.zoom
            pygame.draw.line(screen, (255, 0, 0), (x_projection + self.camera.x, y_projection + self.camera.y), (x_projection_2 + self.camera.x, y_projection_2 + self.camera.y), 1)

 
# Class Worm
#       - Correspond à un ver

# Import des modules
import pygame
from game_config import *
from engine.animation import Animation
from engine.entity import Entity
import math
import time


class Worm(Entity) :

    def __init__(self, x, y, height, width, mass):
        super().__init__(x, y, height, width, mass, "standing.png")

        self.define_animation("idle", Animation(["standing.png"]))
        self.define_animation("walk_right", Animation(["R1.png", "R2.png", "R3.png", "R4.png", "R5.png", "R6.png", "R7.png", "R8.png", "R9.png"]))
        self.define_animation("walk_left", Animation(["L1.png", "L2.png", "L3.png", "L4.png", "L5.png", "L6.png", "L7.png", "L8.png", "L9.png"]))

        self.points = []

        self.touch_down = False
        self.touch_left = False
        self.touch_right = False

    def advance_state(self):
        super().advance_state()

        # Gravity
        if self.rect.bottom >= GameConfig.WINDOW_H:
            self.vy = 0
        else:
            if len(self.points) < 1:
                self.vy = self.vy+GameConfig.GRAVITY*GameConfig.DT*self.mass
            else :
                print("------------------------------------")
                print(self.rect.y)
                print(self.rect.x)
                self.touch_right = False
                self.touch_down = False
                self.touch_left = False
                for i in range(len(self.points)):
                    if self.rect.y >= self.points[i][1]:
                        self.vy = 0
                        self.touch_down = True
                    if self.rect.x >= self.points[i][0] :
                        self.touch_left = True
                if self.touch_left == True :
                    self.vx = 0
                print(self.rect.y)
                print(self.rect.x)
                print("down")
                print(self.touch_down)
                print("left")
                print(self.touch_left)
                print("right")
                print(self.touch_right)


    def has_touched_map(self, points):
        self.points = points

    def draw(self, screen):
        super().draw(screen)

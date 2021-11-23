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

    def advance_state(self):
        super().advance_state()

    def draw(self, screen):
        super().draw(screen)

    def trajectoire(self, a, t, mass):
        gravity = 9.7639
        speed = mass * gravity
        x = math.cos(a)*speed*t
        y = -0.5*gravity*t**2+math.sin(a)*speed*t+self.height

        return x,y

    def pull(self, projectile):
        cur_x, cur_y = pygame.mouse.get_pos()
        hypotenuse = math.sqrt((self.x - cur_x)**2 + (self.y - cur_y)**2)
        oppo = cur_y - 0
        angle = math.sin(oppo / hypotenuse)
        v0 = round(time.time() * 1000)
        proj_x, proj_y = self.x + self.width, self.y - (self.height/2)

        while (proj_y > 0):
            proj_x, proj_y = self.trajectoire(angle, round(time.time() * 1000) - v0, projectile.mass)
            projectile.x = proj_x
            projectile.y = proj_y
            projectile.draw(self.screen)
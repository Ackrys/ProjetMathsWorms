# Class Worm
#       - Correspond à un ver

# Import des modules
import pygame
from game_config import *
from engine.animation import Animation
from engine.entity import Entity
import math
import time


class Projectile(Entity):

    def __init__(self, x, y, height, width, mass):
        super().__init__(x, y, height, width, mass, "projectile_1.jpg")

    def draw(self, screen):
        super().draw(screen)

    def advance_state(self):
        self.pull()
        super().advance_state()

    def trajectoire(self, a, t, mass):
        gravity = 9.7639
        speed = mass * gravity
        x = math.cos(a)*speed*t
        y = -0.5*gravity*t**2+math.sin(a)*speed*t+self.rect.height

        return x,y

    def pull(self):
        cur_x, cur_y = pygame.mouse.get_pos()
        hypotenuse = math.sqrt((self.rect.x - cur_x)**2 + (self.rect.y - cur_y)**2)
        oppo = cur_y - 0
        angle = math.sin(oppo / hypotenuse)
        v0 = round(time.time() * 1000)
        proj_x, proj_y = self.rect.x + self.rect.width, self.rect.y - (self.rect.height/2)

        while (proj_y > 0):
            proj_x, proj_y = self.trajectoire(angle, round(time.time() * 1000) - v0, self.mass)
            self.rect.x = proj_x
            self.rect.y = proj_y

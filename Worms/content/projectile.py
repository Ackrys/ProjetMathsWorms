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

    v0 = 0
    g = 9.7639
    pi = 3.141592654
    x0 = 0
    y0 = 0


    def __init__(self, worm, height, width, mass):
        self.cursor_x, self.cursor_y = pygame.mouse.get_pos()
        self.pos_x = worm.rect.x + worm.rect.width/2 - width/2
        self.pos_y = worm.rect.y + worm.rect.height/2 - height/2
        super().__init__(self.pos_x, self.pos_y, height, width, mass, "missile.png")
        self.x0 = worm.rect_display.x + worm.rect_display.width/2 - self.rect_display.width/2
        self.y0 = worm.rect_display.y + worm.rect_display.height/2 - self.rect_display.height/2
        self.r = abs(math.sqrt((self.rect.x - self.cursor_x)** 2 + (self.rect.y - self.cursor_y)**2))
        print("r : ", self.r)
        self.v0 = round(time.time() * 1000)

    def draw(self, screen):
        super().draw(screen)

    def advance_state(self):
        self.pull()
        super().advance_state()

    def trajectoire(self, t, mass):
        speed = mass * self.g
        x = (self.cursor_x-self.x0) / self.r * speed * t
        y = -0.5 * self.pi * t**2 - (self.cursor_y-self.y0) / self.r * speed * t + self.rect.height
        
        print("x : ", x)
        print("y : ", y)

        self.rect.x = x + self.pos_x
        self.rect.y = -(y) + self.pos_y


    def pull(self):        
        self.trajectoire((round(time.time() * 1000) - self.v0) / 100, self.mass)

    def out_window(self):
        if self.rect.x > GameConfig.WINDOW_W or self.rect.y > GameConfig.WINDOW_H:
            return True

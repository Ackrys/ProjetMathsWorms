# Class Worm
#       - Correspond à un ver

# Import des modules
import pygame
from game_config import *
from engine.animation import Animation
from engine.entity import Entity
import math
import time


class FakeProjectile(Entity):

    v0 = 0
    g = 9.7639
    x0 = 0
    y0 = 0
    damage = 70

    def __init__(self, worm, height, width, mass, camera):
        self.cursor_x, self.cursor_y = pygame.mouse.get_pos()
        self.pos_x = worm.rect.x + worm.rect.width/2 - width/2
        self.pos_y = worm.rect.y + worm.rect.height/2 - height/2
        super().__init__(self.pos_x, self.pos_y, height, width, mass, "missile.png")
        self.x0 = worm.rect_display.x + worm.rect_display.width/2 - self.rect_display.width/2
        self.y0 = worm.rect_display.y + worm.rect_display.height/2 - self.rect_display.height/2
        self.x0 += camera.x
        self.y0 += camera.y
        self.r = abs(math.sqrt((self.rect.x - self.cursor_x)** 2 + (self.rect.y - self.cursor_y)**2))
        self.v0 = round(time.time() * 1000)

    def draw(self, screen):
        pass

    def advance_state(self):
        pass

    def trajectoire(self, t, mass):
        speed_temp = mass * self.g
        x_temp = (self.cursor_x-self.x0)/self.r*speed_temp*t
        y_temp = -0.5*GameConfig.PI*t**2-(self.cursor_y-self.y0)/self.r*speed_temp*t+self.rect.height
        
        return x_temp + self.pos_x, -(y_temp) + self.pos_y


    def pull(self, i):
        x_return, y_return = self.trajectoire((round(time.time() * 1000) - self.v0 + i * 10) / 100, self.mass)
        print(x_return, y_return)
        return x_return, y_return

    def out_window(self):
        if self.rect.x > GameConfig.WINDOW_W or self.rect.y > GameConfig.WINDOW_H:
            return True

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

    v0 = round(time.time() * 1000)
    g = 9.7639
    pi = 3.141592654
    x0 = 0
    y0 = 0


    def __init__(self, x, y, height, width, mass):
        super().__init__(x, y, height, width, mass, "missile.png")
        self.x0 = x
        self.y0 = y
        self.cur_x, self.cur_y = pygame.mouse.get_pos()

    def draw(self, screen):
        super().draw(screen)

    def advance_state(self):
        self.pull()

        super().advance_state()

    def trajectoire(self, t, mass):
        a = (45 - 44 * self.pi / 180)
        speed = mass * self.g
        x = math.cos(a)*speed*t
        y = -0.5*self.pi*t**2+math.sin(a)*speed*t+self.rect.height
        
        divide = 1
        self.rect.x = x + self.x0 / divide
        self.rect.y = -(y) + self.y0 / divide

        print("===========")
        print(self.rect.x - self.x0)
        print(self.rect.y - self.y0)
        print(speed)
 

    def pull(self):
        hypotenuse = math.sqrt((self.rect.x - self.cur_x)**2 + (self.rect.y - self.cur_y)**2)
        oppo = self.cur_y - 600
        angle = math.sin(oppo / hypotenuse)
        
        # while (self.rect.x < GameConfig.WINDOW_GAME_W and self.rect.y < GameConfig.WINDOW_GAME_H):
        self.trajectoire((round(time.time() * 1000) - self.v0) / 1000, self.mass)

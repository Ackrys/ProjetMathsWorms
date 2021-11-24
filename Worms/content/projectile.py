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


    def __init__(self, x, y, height, width, mass):
        self.cursor_x, self.cursor_y = pygame.mouse.get_pos()
        super().__init__(x, y, height, width, mass, "missile.png")
        self.x0 = x + 20
        self.y0 = y + 40
        self.hypotenuse = abs(math.sqrt((self.rect.x - self.cursor_x)** 2 + (self.rect.y - self.cursor_y)**2))
        self.oppo = abs(self.cursor_y - 600)
        self.angle = math.asin(self.oppo / self.hypotenuse)
        self.v0 = round(time.time() * 1000)
        if (x >= self.cursor_x):
            self.angle = - (self.angle + 3)
        print(self.angle)

    def draw(self, screen):
        super().draw(screen)

    def advance_state(self):
        self.pull()
        super().advance_state()

    def trajectoire(self, t, mass):
        speed = mass * self.g
        x = math.cos(self.angle)*speed*t
        y = -0.5*self.pi*t**2+math.sin(self.angle)*speed*t+self.rect.height
        
        self.rect.x = x + self.x0
        self.rect.y = -(y) + self.y0

    

    
 

    def pull(self):        
        self.trajectoire((round(time.time() * 1000) - self.v0) / 100, self.mass)

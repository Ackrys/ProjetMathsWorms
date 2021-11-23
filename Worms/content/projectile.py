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

    g = 9.7639

    def __init__(self, x, y, height, width, mass):
        super().__init__(x, y, height, width, mass, "missile.png")
        self.cur_x, self.cur_y = pygame.mouse.get_pos()

    def draw(self, screen):
        super().draw(screen)

    def advance_state(self):
        self.pull()
        super().advance_state()

    def trajectoire(self, t, mass):
        # gravity = 9.7639
        # speed = mass * gravity
        # x = math.cos(a)*speed*t
        # y = -0.5*gravity*t**2+math.sin(a)*speed*t+self.rect.height 
 
        # return x,y
        pi = 3.141592654
 
        if self.rect.x == 0:
            a = 90*pi/180
 
        else:
            a = 45*pi/180
 
        y = self.rect.y/mass
        x = self.rect.x/mass
        v0 = math.sqrt(pow(x,2) + pow(y,2))
        vy = self.g * t + v0* math.sin (a)
        y = +1*(vy- 0.5*self.g*pow(t,2))
        x = v0*math.cos(a) * t
 
        self.rect.x = x + 100
        self.rect.y = y

        print(self.rect.x , " || " , x)
        print(self.rect.y, " || ", y)


    def pull(self):
        hypotenuse = math.sqrt((self.rect.x - self.cur_x)**2 + (self.rect.y - self.cur_y)**2)
        oppo = self.cur_y - GameConfig.WINDOW_H
        angle = math.sin(oppo / hypotenuse)
        v0 = round(time.time() * 1000)
        proj_x, proj_y = self.rect.x, self.rect.y

        while (self.rect.x < GameConfig.WINDOW_W and self.rect.y < GameConfig.WINDOW_H):
            self.trajectoire(round(time.time() * 1000) - v0, self.mass)
        #     self.rect.x = proj_x
        #     self.rect.y = proj_y

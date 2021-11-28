# Class Projectile
#       - Correspond à un projectile

# Import des modules
import pygame
from game_config import *
from engine.animation import Animation
from engine.entity import Entity
import math
import time


class Projectile(Entity):

    t0 = 0
    g = 9.7639
    x0 = 0
    y0 = 0
    damage = 70

    def __init__(self, worm, height, width, mass, alpha, camera):
    # def __init__(self, worm, height, width, mass, pre_def_cursor_x, pre_def_cursor_y, camera,team):
        # if pre_def_cursor_x != -1:
        #     self.cursor_x, self.cursor_y = pre_def_cursor_x, pre_def_cursor_y
        # else:
        self.alpha = alpha
        self.cursor_x, self.cursor_y = pygame.mouse.get_pos()
        self.pos_x = worm.rect.x + worm.rect.width/2 - width/2
        self.pos_y = worm.rect.y + worm.rect.height/2 - height/2
        super().__init__(self.pos_x, self.pos_y, height, width, mass, "missile.png")
        self.x0 = worm.rect_display.x + worm.rect_display.width/2 - self.rect_display.width/2
        self.y0 = worm.rect_display.y + worm.rect_display.height/2 - self.rect_display.height/2
        self.x0 += camera.x
        self.y0 += camera.y
        self.r = abs(math.sqrt((self.rect.x - self.cursor_x)** 2 + (self.rect.y - self.cursor_y)**2))
        self.t0 = round(time.time() * 1000)
        

    def draw(self, screen):
        super().draw(screen)

    def advance_state(self):
        self.pull()
        super().advance_state()

    def trajectoire(self, t, mass):
        speed = mass * GameConfig.GRAVITY
        x = (self.cursor_x-self.x0)/self.r*speed*t
        y = -0.5*GameConfig.GRAVITY*t**2-(self.cursor_y-self.y0)/self.r*speed*t+self.rect.height
        
        self.rect.x = x + self.pos_x
        self.rect.y = -(y) + self.pos_y

    def trajectoire_IA(self,t,mass,a):
        speed = mass * GameConfig.GRAVITY
        x = math.sin(a)*speed*t
        y = -0.5*GameConfig.GRAVITY*t**2-math.cos(a)*speed*t+self.rect.height


    def pull(self):
        if self.alpha == -1:
            self.trajectoire((round(time.time() * 1000) - self.t0) / 100, self.mass)
        else:
            self.trajectoire_IA((round(time.time() * 1000) - self.t0) / 100, self.mass, self.alpha)

        

    def out_window(self):
        if self.rect.x > GameConfig.WINDOW_W or self.rect.y > GameConfig.WINDOW_H:
            return True

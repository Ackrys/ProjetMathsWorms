# Class Camera
#       - Correspond à la caméra du jeu


# Import des modules
import pygame
from game_config import *

class Camera :
    def __init__(self):
        self.zoom = 0.8

        self.x = 0
        self.y = 0

    def zoom_by(self, value):
        self.zoom += value

    def move_by(self, x, y):
        self.x += x
        self.y += y

    def move_to(self, x, y):
        self.x = x
        self.y = y
    
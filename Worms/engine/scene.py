# Class Scene
#       - Correspond à une scène de jeu


# Import des modules
import pygame
from game_config import *

class Scene :
    
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)
    
    def advance_state(self):
        for obj in self.objects:
            obj.advance_state()
    
    def draw(self, screen, camera):
        for obj in self.objects:
            obj.applyZoom(camera.zoom)
            obj.draw(screen)

    def applyOffset(self, x, y):
        for obj in self.objects:
            obj.applyOffset(x, y)

    def areColliding(self, obj1, obj2):
        return pygame.sprite.collide_mask(obj1, obj2)
    
# Class Scene
#       - Correspond à une scène de jeu


# Import des modules
import pygame
from game_config import *

class Scene :
    

    # Initialisation

    def __init__(self):
        self.objects = []


    # Objects management

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)
    
    def advance_state(self):
        # self.map.advance_state()
        for obj in self.objects:
            obj.advance_state()
    

    # Map management

    def load_map(self, map):
        self.map = map

    def get_map(self):
        return self.map

    def remove_map(self):
        self.map = None


    # Display methods

    def draw(self, screen, camera):
        # Draw map
        self.map.applyZoom(camera.zoom)
        self.map.draw(screen)
        
        # Draw objects
        for obj in self.objects:
            obj.applyZoom(camera.zoom)
            obj.draw(screen)

    def applyOffset(self, x, y):
        self.map.applyOffset(x, y)
        for obj in self.objects:
            obj.applyOffset(x, y)


    # Collision management

    def areColliding(self, obj1, obj2):
        return pygame.sprite.collide_mask(obj1, obj2)
    
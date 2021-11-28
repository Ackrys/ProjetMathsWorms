# Class Scene
#       - Correspond à une scène de jeu


# Import des modules
import pygame
import math
from game_config import *

class Scene :
    

    # Initialisation

    def __init__(self):
        self.objects = []
        self.ui = []
        self.map = None


    # Objects management

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)
    
    def advance_state(self):
        # self.map.advance_state()
        for obj in self.objects:
            obj.advance_state()

    # UI management

    def add_ui(self, ui):
        self.ui.append(ui)
    
    def remove_ui(self, ui):
        self.ui.remove(ui)
    

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
        if self.map != None:
            self.map.applyZoom(camera.zoom)
            self.map.draw(screen)
        
        # Draw objects
        for obj in self.objects:
            obj.applyZoom(camera.zoom)
            obj.draw(screen)

    def applyOffset(self, x, y):
        if self.map != None:
            self.map.applyOffset(x, y)
        for obj in self.objects:
            obj.applyOffset(x, y)
        for ui in self.ui:
            ui.applyOffset(x, y)


    # UI

    def draw_ui(self, screen, camera):
        for ui in self.ui:
            ui.draw(screen)



    # Collision management

    def areColliding(self, obj1, obj2):
        return pygame.sprite.collide_mask(obj1, obj2)
    
    def distance_between_objects(self, obj1, obj2):
        x1, y1 = obj1.rect.center
        x2, y2 = obj2.rect.center
        return math.sqrt((x1-x2)**2+(y1-y2)**2)
# Class Animation
#       - Correspond à une animation d'une entité


# Import des modules
import pygame
from game_config import *

class Animation() :

    def __init__(self, images):
        self.images = []

        for i in range(len(images)) :
            self.images.append(GameConfig.loadImageAlpha(images[i]))

        self.current_image = self.images[0]
        self.nb_tick = 0
    
    def get_current_image(self):
        return self.current_image

    def get_current_mask(self):
        return pygame.mask.from_surface(self.current_image)

    def advance_state(self):
        if self.nb_tick == 2 : # 2 ticks = 1 frame
            if self.current_image == self.images[-1]: # Si on est à la dernière image
                self.current_image = self.images[0]
            else : # Sinon on passe à l'image suivante
                self.current_image = self.images[self.images.index(self.current_image) + 1]
            self.nb_tick = 0

        # On incrémente le nombre de ticks
        self.nb_tick += 1 

    def reset_state(self):
        self.current_image = self.images[0]
        self.nb_tick = 0


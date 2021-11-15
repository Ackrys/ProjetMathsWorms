# Class Bat
#       - Correspond aux chauve-souris


# Import des modules
import pygame
from game_config import *


class Bat(pygame.sprite.Sprite) :

    LEFT = 0
    RIGHT = 1

    def __init__(self, x, y, vx):
        pygame.sprite.Sprite.__init__(self)

        # Position du chauve-souris
        self.rect = pygame.Rect(x,
                y,
                GameConfig.BAT_W,
                GameConfig.BAT_H)

        # Vitesse de la chauve-souris
        self.vx = vx

        # Animation
        self.sprite_count=0
        if self.vx < 0 :
            self.direction = Bat.RIGHT
        else :
            self.direction = Bat.LEFT

        self.image = Bat.IMAGES[self.direction][
            self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER
        ]
        self.mask = Bat.MASKS[self.direction][
            self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER
        ]

    def init_sprites() :
        Bat.IMAGES = {
            Bat.LEFT : GameConfig.FLYING_FROM_LEFT,
            Bat.RIGHT : GameConfig.FLYING_FROM_RIGHT
        }
        Bat.MASKS = {
            Bat.LEFT : GameConfig.FLYING_FROM_LEFT_MASKS,
            Bat.RIGHT : GameConfig.FLYING_FROM_RIGHT_MASKS
        }

    def advance_state(self):
        self.rect.x += self.vx*GameConfig.DT

        # Animation
        self.sprite_count+=1
        if self.sprite_count >= GameConfig.NB_FRAMES_PER_SPRITE_BAT*len(Bat.IMAGES[self.direction]) :
            self.sprite_count=0
        self.image = Bat.IMAGES[self.direction][
            self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_BAT
        ]
        self.mask = Bat.MASKS[self.direction][
            self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_BAT
        ]

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

    def is_dead(self):
        if self.vx < 0 :
            return self.rect.right < 0
        else :
            return self.rect.left > GameConfig.WINDOW_W

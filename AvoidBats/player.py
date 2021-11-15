# Class Player
#       - Correspond au joueur


# Import des modules
import pygame
from game_config import *


class Player(pygame.sprite.Sprite) :

    LEFT = -1
    RIGHT = 1
    NONE = 0

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)

        # Position du joueur
        self.rect = pygame.Rect(x,
                  GameConfig.Y_PLATEFORM-GameConfig.PLAYER_H,
                  GameConfig.PLAYER_W,
                  GameConfig.PLAYER_H)

        # Vitesse du joueur
        self.vx = 0
        self.vy = 0

        # Animation
        self.sprite_count=0
        self.direction = Player.NONE

        # Image
        self.image =Player.IMAGES[self.direction][
            self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER
        ]

        # Mask
        self.mask =Player.MASKS[self.direction][
            self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER
        ]

    def init_sprites() :
        Player.IMAGES = {
          Player.LEFT : GameConfig.WALK_LEFT_IMG,
          Player.RIGHT : GameConfig.WALK_RIGHT_IMG,
          Player.NONE : GameConfig.STANDING_IMG
        }
        Player.MASKS = {
          Player.LEFT : GameConfig.WALK_LEFT_MASKS,
          Player.RIGHT : GameConfig.WALK_RIGHT_MASKS,
          Player.NONE : GameConfig.STANDING_MASK
        }

    def on_ground(self) : # Contact avec le sol
        return self.rect.bottom > GameConfig.Y_PLATEFORM

    def is_touching(self, bat) :
        return pygame.sprite.collide_mask(self, bat)

    def advance_state(self,next_move) : # Acceleration
        fx = 0
        fy = 0

        if next_move.left :
            fx = GameConfig.FORCE_LEFT
        elif next_move.right :
            fx = GameConfig.FORCE_RIGHT # Vitesse

        if next_move.jump:
            fy = GameConfig.FORCE_JUMP

        # Acceleration X
        self.vx = fx*GameConfig.DT

        # Acceleration Y
        if self.on_ground() :
            self.vy = fy*GameConfig.DT
        else :
            self.vy = self.vy+GameConfig.GRAVITY*GameConfig.DT

        # Position
        x = self.rect.left
        vx_min = -x/GameConfig.DT
        vx_max = (GameConfig.WINDOW_W-GameConfig.PLAYER_W-x)/GameConfig.DT
        self.vx = min(self.vx,vx_max)
        self.vx = max(self.vx,vx_min)
        self.rect = self.rect.move(self.vx*GameConfig.DT,self.vy*GameConfig.DT)

        # Rectification de la vitesse
        y = self.rect.top
        vy_max = (GameConfig.Y_PLATEFORM-GameConfig.PLAYER_H-y)/GameConfig.DT
        self.vy = min(self.vy,vy_max)

        # Direction - Animation
        if next_move.left :
            self.direction = Player.LEFT
        elif next_move.right :
            self.direction = Player.RIGHT
        else :
            self.direction = Player.NONE

        # Animation
        self.sprite_count+=1
        if self.sprite_count >= GameConfig.NB_FRAMES_PER_SPRITE_PLAYER*len(Player.IMAGES[self.direction]) :
            self.sprite_count=0
        self.image = Player.IMAGES[self.direction][
            self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER
        ]
        self.mask = Player.MASKS[self.direction][
            self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER
        ]


    def draw(self, window):
        window.blit(self.image,self.rect.topleft)

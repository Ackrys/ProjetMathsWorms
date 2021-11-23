# Class Entity
#       - Correspond à une entité de jeu


# Import des modules
import pygame
from game_config import *
from engine.animation import Animation

class Entity(pygame.sprite.Sprite) :


    # Init
    def __init__(self, x, y, height, width, mass, image):
        pygame.sprite.Sprite.__init__(self)

        # Rect
        self.rect = pygame.Rect(x,
                    y,
                    width,
                    height)

        # Display rect
        self.rect_display = pygame.Rect(x,
                    y,
                    width,
                    height)

        # Vitesse de l'entité
        self.vx = 0
        self.vy = 0

        # Offset
        self.x_offset = 0
        self.y_offset = 0

        # Mass
        self.mass = mass

        # Animation
        self.animations = {
            "idle": Animation([image])
        }

        self.image_display = self.animations["idle"].get_current_image()
        self.mask = self.animations["idle"].get_current_mask()

        self.current_animation = "idle"

        # Collidors
        self.collidors = []


    # Advance method
    def advance_state(self):
        # Gravity
        if self.rect.bottom >= GameConfig.WINDOW_H :
            self.vy = 0
        else :
            self.vy = self.vy+GameConfig.GRAVITY*GameConfig.DT*self.mass

        # Position
        self.rect = self.rect.move(self.vx*GameConfig.DT,self.vy*GameConfig.DT)

        self.rect_display.x = self.rect.x
        self.rect_display.y = self.rect.y

        # Animation
        self.animations[self.current_animation].advance_state()


    # Display methods
    def applyZoom(self, zoom):
        # Resize
        self.rect_display.height = self.rect.height * zoom
        self.rect_display.width = self.rect.width * zoom
        self.image_display = pygame.transform.scale(self.animations[self.current_animation].get_current_image(), (
            self.animations[self.current_animation].get_current_image().get_rect().size[0] * zoom,
            self.animations[self.current_animation].get_current_image().get_rect().size[1] * zoom,
        )
        )

        # Move
        self.rect_display.x = self.rect.x * zoom
        self.rect_display.y = self.rect.y * zoom

    def applyOffset(self, x, y):
        self.x_offset = x
        self.y_offset = y

    def draw(self, screen):
        super().draw(screen)


    # Animation methods
    def define_animation(self, animation_name, animation):
        self.animations[animation_name] = animation
    
    def remove_animation(self, animation_name):
        self.animations.pop(animation_name)

    def set_animation(self, animation_name):
        if (animation_name != self.current_animation):
            for animation in self.animations.values():
                animation.reset_state()

            self.current_animation = animation_name


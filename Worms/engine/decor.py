# Class Entity
#       - Correspond à une entité de jeu


# Import des modules
import pygame
from game_config import *
from engine.animation import Animation

class Decor(pygame.sprite.Sprite) :


    # Init
    def __init__(self, x, y, height, width, image):
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

        # Offset
        self.x_offset = 0
        self.y_offset = 0

        # Animation
        self.animations = {
            "idle": Animation([image])
        }

        self.image_display = self.animations["idle"].get_current_image()

        self.current_animation = "idle"


    # Advance methods
    def advance_state(self):
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
        screen.blit(
            self.image_display,
            (
                self.rect_display.x + self.x_offset, 
                self.rect_display.y + self.y_offset
            )
        )


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


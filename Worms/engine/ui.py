# Class UI
#       - Correspond à un élément de l'interface utilisateur


# Import des modules
import pygame
from game_config import *
from engine.animation import Animation

class UI(pygame.sprite.Sprite) :


    # Init
    def __init__(self, x, y, height, width, image):
        pygame.sprite.Sprite.__init__(self)

        # Rect
        self.rect = pygame.Rect(x,
                    y,
                    width,
                    height)

        # Animation
        self.animations = {
            "idle": Animation([image])
        }

        self.image_display = self.animations["idle"].get_current_image()
        self.mask = self.animations["idle"].get_current_mask()

        self.current_animation = "idle"


    # Advance methods
    def advance_state(self):
        # Animation
        self.animations[self.current_animation].advance_state()
        self.image_display = self.animations[self.current_animation].get_current_image()

    def is_clicked_on(self, pos):
        return self.rect.collidepoint(pos[0], pos[1])

    # Display methods
    def draw(self, screen):
        screen.blit(
            self.image_display,
            (
                self.rect.x, 
                self.rect.y
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


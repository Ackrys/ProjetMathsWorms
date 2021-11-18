# Class Entity
#       - Correspond à une entité de jeu


# Import des modules
import pygame
from game_config import *

class Decor(pygame.sprite.Sprite) :

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

        # Image
        self.image = GameConfig.loadImage(image)
        self.image_display = self.image

        # Offset
        self.x_offset = 0
        self.y_offset = 0

    def advance_state(self):
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y

    def applyZoom(self, zoom):
        # Resize
        self.rect_display.height = self.rect.height * zoom
        self.rect_display.width = self.rect.width * zoom
        self.image_display = pygame.transform.scale(self.image, (
            self.image.get_rect().size[0] * zoom,
            self.image.get_rect().size[1] * zoom,
        )
        )

        # Move
        if zoom > 1 :
            self.rect_display.x = self.rect.x + self.rect.x * zoom
            self.rect_display.y = self.rect.y + self.rect.y * zoom
        else :
            self.rect_display.x = self.rect.x - self.rect.x * zoom
            self.rect_display.y = self.rect.y - self.rect.y * zoom

    def applyOffset(self, x, y):
        self.x_offset = x
        self.y_offset = y

    def draw(self, screen):
        screen.blit(self.image_display, (self.rect_display.x + self.x_offset, self.rect_display.y + self.y_offset))


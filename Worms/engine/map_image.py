# Class Map Image
#           - Implémente la génération d'image de la map via du perlin noise
#           - Source : https://gist.github.com/veb/7b9f5393d0c25977e4cb

import pygame
import math
import random
import numpy as np

from game_config import *

class MapImage :

    # Initialisation

    def __init__(self, complexity):
        # Data
        self.width = GameConfig.WINDOW_W
        self.height = GameConfig.WINDOW_H

        self.noise_image = pygame.Surface( (self.width // complexity, self.height // complexity - 400 // complexity) )
        self.complexity = complexity

        self.x_offset = 0
        self.y_offset = 0

        self.rect = pygame.Rect(0, GameConfig.WINDOW_H - self.noise_image.get_height(), self.noise_image.get_width(), self.noise_image.get_height())
        self.rect_display = self.rect.copy()
        
        # Generation
        # self.noise_image.fill((120,40,120))

        self.row_state_max = 8
        self.row_state = []

        self.color_white = (255, 255, 255)
        self.color_black = (0, 0, 0)
        self.color_transparent = (255, 255, 255)
        
        self.generate_map()
        self.noise_image_display = self.noise_image.copy()

    # Methods

    def get_noise_image(self):
        return self.noise_image

    def get_mask(self):
        return pygame.mask.from_surface(self.noise_image)

    # Display methods
    def applyZoom(self, zoom):
        # Resize
        self.rect_display.height = self.rect.height * zoom
        self.rect_display.width = self.rect.width * zoom
        self.noise_image_display = pygame.transform.scale(self.noise_image, (
            self.noise_image.get_width() * zoom,
            self.noise_image.get_height() * zoom,
        )
        )

        # Move
        self.rect_display.x = self.rect.x * zoom
        self.rect_display.y = self.rect.y * zoom

    def applyOffset(self, x, y):
        self.x_offset = x
        self.y_offset = y
    
    def advance_state(self):
        pass

    def draw(self, screen):
        screen.blit(
            self.noise_image_display,
            (
                self.rect_display.x + self.x_offset, 
                self.rect_display.y + self.y_offset
            )
        )


    # Map Generation
    def generate_map(self, thickness=3, density=2, randomness=2):
        # Density > 0 / Integer
        # Thickness > 0 / Integer

        self.noise_image_gen = pygame.Surface( (self.noise_image.get_width() * randomness, self.noise_image.get_height() * randomness) )

        # Generate noise
        scale1 = 2.0
        scale2 = 4.0
        scale3 = 8.0
        for w in range(0, self.noise_image_gen.get_width()):
            for h in range(0, self.noise_image_gen.get_height()):
                i = int((self.noise(w/scale1,h/scale1)+1.0) * 42)
                i += int((self.noise(w/scale2,h/scale2)+1.0) * 42)
                i += int((self.noise(w/scale3,h/scale3)+1.0) * 42)
                # Flat the color
                if(i>255):
                    i=255
                if(i<0):
                    i=0
                self.noise_image_gen.set_at((w,h),(i,i,i))

        # Get random part of the noise
        noise_x_start = random.randint(0, self.noise_image_gen.get_width() - self.noise_image.get_width())
        noise_y_start = random.randint(0, self.noise_image_gen.get_height() - self.noise_image.get_height())
        for w in range(noise_x_start, noise_x_start + self.noise_image.get_width()):
            for h in range(noise_y_start, noise_y_start + self.noise_image.get_height()):
                self.noise_image.set_at((w - noise_x_start, h - noise_y_start), self.noise_image_gen.get_at((w,h)))
        
        # Round color to neareast black/white
        self.round_to_nearest_black_and_white()

        # Apply delation to image
        for i in range(0, density):
            self.delation(thickness)

        # Round color to neareast black/white
        self.round_to_nearest_black_and_white()

        # Get white islands
        white_islands = self.get_white_islands()

        # Color islands in red
        # for island in white_islands:
            # if island[0][1] > self.noise_image.get_height() - 150:
                # for pixel in island:
                    # self.noise_image.set_at(pixel, (255,0,0))
        
        # Link each islands
        last_island = None
        for i in range(0, len(white_islands) - 1):
            # Calculate distance between islands
            if white_islands[i][0][1] > self.noise_image.get_height() - self.noise_image.get_height() * 0.60: # Island y > half of the map
                if last_island :
                    actual_island = white_islands[i]
                    points_to_draw = self.pixels_between_points(last_island[0], actual_island[0])
                    for pixel in points_to_draw:
                        self.noise_image.set_at(pixel, (255,0,0))
                    last_island = actual_island
                else:
                    last_island = white_islands[i]
            else: # Erase island
                for pixels in white_islands[i]:
                    self.noise_image.set_at(pixels, self.color_black)


        # Resize image to fit the screen
        self.noise_image = pygame.transform.smoothscale(self.noise_image, (self.noise_image.get_width() * self.complexity, self.noise_image.get_height() * self.complexity))
        self.rect = pygame.Rect(0, GameConfig.WINDOW_H - self.noise_image.get_height(), self.noise_image.get_width(), self.noise_image.get_height())
        self.rect_display = self.rect.copy()

        # Round color to neareast black/white
        self.round_to_nearest_black_and_white()

        # Apply delation to image
        for i in range(0, density):
            self.delation(thickness)

        # Round color to neareast black/white
        self.round_to_nearest_black_and_white(10)

        # Fill the map
        self.fill_map()

        # Add black columns to the sides
        self.add_columns()

        # Invert colors
        self.invert_colors()

        # Add height to the map
        self.add_height()

        # Transparent the map
        self.transparent_map()


    # - Image manipulation
    def delation(self, thickness):
        # Apply delation to image
        self.noise_image = pygame.transform.smoothscale(self.noise_image, (self.noise_image.get_width() / thickness, self.noise_image.get_height() / thickness))

        # Resize the image to original size
        self.noise_image = pygame.transform.smoothscale(self.noise_image, (self.noise_image.get_width() * thickness, self.noise_image.get_height() * thickness))

    def round_to_nearest_black_and_white(self, color_value=140):       
        for w in range(0, self.noise_image.get_width()):
            for h in range(0, self.noise_image.get_height()):
                if self.noise_image.get_at((w,h))[0] > color_value:
                    self.noise_image.set_at((w,h), self.color_white)
                else:
                    self.noise_image.set_at((w,h), self.color_black)

    # - Get white islands
    def get_white_islands(self):
        # Get white islands
        white_islands = []
        white_pixels = []

        # Test only first islands
        # end = 5
        for w in range(0, self.noise_image.get_width()):
            for h in range(0, self.noise_image.get_height()):
                if (w, h) not in white_pixels and self.noise_image.get_at((w,h))[0] > 120 :
                    island = self.get_island(w, h)
                    white_islands.append(island)
                    for pixel in island:
                        white_pixels.append(pixel)
                    # Test only first islands
                    # end -= 1
                    # if end == 0:
                    #     return white_islands
        return white_islands

        pass

    def get_island(self, x, y):
        white_pixels = []
        white_pixels_done = []

        # First pixel
        actual_pixel = (x,y)
        white_pixels.append(actual_pixel)
        neighbours = self.get_neighbours(actual_pixel)
        for neighbour in neighbours:
            white_pixels.append(neighbour)
        white_pixels_done.append(actual_pixel)

        # Call for every pixel
        while len(white_pixels_done) < len(white_pixels):
            actual_pixel = white_pixels[len(white_pixels_done)]
            neighbours = self.get_neighbours(actual_pixel)
            for neighbour in neighbours:
                if neighbour not in white_pixels:
                    white_pixels.append(neighbour)
            actual_pixel = neighbours[0]
            white_pixels_done.append(actual_pixel)
        
        return white_pixels

    def get_neighbours(self, actual_pixel):
        neighbours = []
        if actual_pixel[0] < self.noise_image.get_width() - 1 and self.noise_image.get_at((actual_pixel[0] + 1, actual_pixel[1]))[0] > 120:
            neighbours.append((actual_pixel[0] + 1, actual_pixel[1]))
        if actual_pixel[0] > 0 and self.noise_image.get_at((actual_pixel[0] - 1, actual_pixel[1]))[0] > 120:
            neighbours.append((actual_pixel[0] - 1, actual_pixel[1]))
        if actual_pixel[1] < self.noise_image.get_height() - 1 and self.noise_image.get_at((actual_pixel[0], actual_pixel[1] + 1))[0] > 120:
            neighbours.append((actual_pixel[0], actual_pixel[1] + 1))
        if actual_pixel[1] > 0 and self.noise_image.get_at((actual_pixel[0], actual_pixel[1] - 1))[0] > 120:
            neighbours.append((actual_pixel[0], actual_pixel[1] - 1))
        return neighbours
        
    # - Linking white islands
    def pixels_between_points(self, point1, point2):
        pixels = []
        p1 = np.array([point1[0], point1[1]])
        p2 = np.array([point2[0], point2[1]])

        p = p1
        d = p2-p1
        N = np.max(np.abs(d))
        s = d/N

        pixel = (np.rint(p).astype('int')[0], np.rint(p).astype('int')[1])
        pixels.append(pixel)
        for ii in range(0,N):
            p = p+s
            pixel = (np.rint(p).astype('int')[0], np.rint(p).astype('int')[1])
            pixels.append(pixel)

        return pixels

    # - Map style
    def fill_map(self):
        # For each pixel
        for w in range(0, self.noise_image.get_width()):
            for h in range(0, self.noise_image.get_height()):
                if self.noise_image.get_at((w,h))[0] > 120: # White pixel
                    # Draw a line from the pixel to the bottom of the map
                    for y in range(h, self.noise_image.get_height()):
                        self.noise_image.set_at((w,y), self.color_white)
        
    def add_columns(self):
        # Left column
        for w in range(0, 30):
            for h in range(0, self.noise_image.get_height()):
                self.noise_image.set_at((w,h), self.color_black)
        # Right column
        for w in range(self.noise_image.get_width() - 30, self.noise_image.get_width()):
            for h in range(0, self.noise_image.get_height()):
                self.noise_image.set_at((w,h), self.color_black)
    
    def invert_colors(self):
        for w in range(0, self.noise_image.get_width()):
            for h in range(0, self.noise_image.get_height()):
                if self.noise_image.get_at((w,h))[0] > 120:
                    self.noise_image.set_at((w,h), self.color_black)
                else:
                    self.noise_image.set_at((w,h), self.color_white)

    def add_height(self, offset_height=100):
        self.noise_image_new = pygame.Surface( (self.noise_image.get_width(), self.noise_image.get_height() + offset_height) )
        # Copy old image content to new image
        self.noise_image_new.blit(self.noise_image, (0,0))
        # For each pixel at the bottom of the map
        for w in range(0, self.noise_image.get_width()):
            if self.noise_image.get_at((w, self.noise_image.get_height() - 1))[0] < 120: # Black pixel
                # Add a fix height
                for h in range(self.noise_image.get_height(), self.noise_image.get_height() + offset_height):
                    self.noise_image_new.set_at((w,h), self.color_black)

        self.noise_image = self.noise_image_new.copy()

        self.rect.height += offset_height
        self.rect.y -= offset_height

    def transparent_map(self):
        for w in range(0, self.noise_image.get_width()):
            for h in range(0, self.noise_image.get_height()):
                if self.noise_image.get_at((w,h))[0] > 100:
                    self.noise_image.set_at((w,h), self.color_transparent)



    # Noise generation

    def findnoise2(self, x,y):
        n = int(x) + int(y) * 57
        allf = 0xFFFFFFFF
        an = (n << 13) & allf
        n = (an ^ n) & allf
        nn = (n*(n*n*60493+19990303)+1376312589)&0x7fffffff
        return 1.0-(float(nn)/1073741824.0)

    def interpolate(self, a, b, x):
        ft = float(x * 3.1415927)
        f = float((1.0-math.cos(ft))* 0.5)
        return a*(1.0-f)+b*f

    def noise(self, x,y):
        floorx = float(int(x))
        floory = float(int(y))
        s=self.findnoise2(floorx,floory) 
        t=self.findnoise2(floorx+1,floory)
        u=self.findnoise2(floorx,floory+1) 
        v=self.findnoise2(floorx+1,floory+1)
        int1=self.interpolate(s,t,x-floorx) 
        int2=self.interpolate(u,v,x-floorx)
        return self.interpolate(int1,int2,y-floory) 


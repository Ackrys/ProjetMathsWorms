# Class Perlin Noise
#           - Implémente la génération d'un perlin noise
#           - Source : https://gist.github.com/veb/7b9f5393d0c25977e4cb

import pygame
import math
import random

from game_config import *

class MapImage :


    # Initialisation

    def __init__(self, lineheight, complexity):
        # Data
        self.noise_image = pygame.Surface( (GameConfig.WINDOW_W, GameConfig.WINDOW_H - 500) )
        self.lineheight = lineheight
        self.complexity = complexity + 1

        self.x_offset = 0
        self.y_offset = 0

        self.rect = pygame.Rect(0, GameConfig.WINDOW_H - self.noise_image.get_height(), self.noise_image.get_width(), self.noise_image.get_height())
        self.rect_display = self.rect.copy()
        
        # Generation
        self.noise_image.fill((120,40,120))
        
        offset = 0
        while offset < self.noise_image.get_height():
            self.generate_map(offset)
            offset += self.lineheight

        self.noise_image_display = self.noise_image.copy()

    # Methods

    def get_noise_image(self):
        return self.noise_image

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
    def generate_map(self, offset):

        # Generate noise
        scale1 = 2.0
        scale2 = 4.0
        scale3 = 8.0
        for w in range(0, self.noise_image.get_width()):
            for h in range(offset, offset + self.lineheight):
                i = int((self.noise(w/scale1,h/scale1)+1.0) * 42)
                i += int((self.noise(w/scale2,h/scale2)+1.0) * 42)
                i += int((self.noise(w/scale3,h/scale3)+1.0) * 42)
                # Randomize the color
                i = int(i * (random.random() * 0.5 + 0.5))
                # Flat the color
                if(i>255):
                    i=255
                if(i<0):
                    i=0
                self.noise_image.set_at((w,h),(i,i,i))

        # Round Noise Image Pixels To Nearest white or black
        for w in range(0, self.noise_image.get_width()):
            for h in range(offset, offset + self.lineheight):
                if(self.noise_image.get_at((w,h))[0] > 150):
                    self.noise_image.set_at((w,h),(255,255,255))
                else:
                    self.noise_image.set_at((w,h),(0,0,0))

        # Round Image Color For Each Column
        for w in range(0, self.noise_image.get_width()):
            for h in range(offset, offset + self.lineheight):
                if(self.noise_image.get_at((w,h))[0] > 100):
                    self.noise_image.set_at((w,h),(255,255,255))
                else:
                    self.noise_image.set_at((w,h),(0,0,0))

        # Keep [self.complexity] longest lines of the map row
        longest_lines = []
        w = 0
        while w < self.noise_image.get_width():
            if(self.noise_image.get_at((w,0))[0] < 100): # Black pixel
                length = 1
                # Get the length of the line
                w_offset = w
                while self.noise_image.get_at((w_offset,offset))[0] < 100 and w_offset < self.noise_image.get_width() - 1:
                    length += 1
                    w_offset += 1
                
                if len(longest_lines) < self.complexity:
                    longest_lines.append({
                        'length': length,
                        'start': w
                    })
                    w += length - 1
                else :
                    # Find shortest line
                    shortest_line = None
                    for line in longest_lines:
                        if shortest_line == None or line['length'] < shortest_line['length']:
                            shortest_line = line

                    # Replace shortest line by the new one
                    if shortest_line['length'] < length:
                        longest_lines.remove(shortest_line)
                        longest_lines.append({
                            'length': length,
                            'start': w
                        })
                        w += length - 1
            w += 1

        # Fill with white pixels
        for w in range(0, self.noise_image.get_width()):
            for h in range(offset, offset + self.lineheight):
                self.noise_image.set_at((w,h),(255,255,255))

        # Draw the lines
        for line in longest_lines:
            for w in range(line['start'], line['start'] + line['length']):
                for h in range(offset, offset + self.lineheight):
                    self.noise_image.set_at((w,h),(0,0,0))
                    

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


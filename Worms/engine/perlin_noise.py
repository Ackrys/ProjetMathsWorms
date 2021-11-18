# Class Perlin Noise
#           - Implémente la génération d'un perlin noise
#           - Source : https://gist.github.com/veb/7b9f5393d0c25977e4cb

import pygame 
import math

from game_config import *

class NoiseImage :

    def __init__(self):
        self.noise_image = pygame.Surface( (GameConfig.WINDOW_GAME_W, GameConfig.WINDOW_GAME_H) ) 
        self.noise_image.fill((120,40,120))
        scale1 = 2.0
        scale2 = 4.0
        scale3 = 8.0
        for w in range(0, self.noise_image.get_width()):
            for h in range(0, self.noise_image.get_height()):
                i = int((self.noise(w/scale1,h/scale1)+1.0) * 42)
                i += int((self.noise(w/scale2,h/scale2)+1.0) * 42)
                i += int((self.noise(w/scale3,h/scale3)+1.0) * 42)
                if(i>255):
                    i=255
                if(i<0):
                    i=0
                self.noise_image.set_at((w,h),(i,i,i))

    def get_noise_image(self):
        return self.noise_image

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


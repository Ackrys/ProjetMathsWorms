# Class Worm
#       - Correspond à un ver

# Import des modules
# import pygame
from content.projectile import Projectile
from game_config import *
from engine.animation import Animation
from engine.entity import Entity

import math
class Worm(Entity) :

    def __init__(self, x, y, height, width, mass, map):
        super().__init__(x, y, height, width, mass, "standing.png")

        self.define_animation("idle", Animation(["standing.png"]))
        self.define_animation("walk_right", Animation(["R1.png", "R2.png", "R3.png", "R4.png", "R5.png", "R6.png", "R7.png", "R8.png", "R9.png"]))
        self.define_animation("walk_left", Animation(["L1.png", "L2.png", "L3.png", "L4.png", "L5.png", "L6.png", "L7.png", "L8.png", "L9.png"]))

        self.points = []
        self.map = map

        self.touch_down = False
        self.touch_left = False
        self.touch_right = False

        self.is_jumping = False

        self.will_touch_map = False

        self.hp = GameConfig.WORM_HP

    def advance_state(self):
        super().advance_state()

        # Gravity
        if len(self.points) < 1:
            self.vy = self.vy+GameConfig.GRAVITY*GameConfig.DT*self.mass
        else :
            self.touch_right = False
            self.touch_down = False
            self.touch_left = False

            columns = {}

            for i in range(len(self.points)):
                actual_point = (self.points[i][0], self.points[i][1] + self.map.image.rect.y)
                columns.get(actual_point[0])
                if columns.get(actual_point[0]) == None:
                    columns[actual_point[0]] = [actual_point[1]]
                else:
                    columns[actual_point[0]].append(actual_point[1])
                if actual_point[1] > self.rect.y:
                    self.touch_down = True

            # Get the left column nearest to the player
            max_left_column = None
            for i in range(self.rect.x, self.rect.x + self.rect.width // 2):
                if columns.get(i) != None:
                    max_left_column = i
                    break

            if max_left_column != None and len(columns.get(max_left_column)) > 20:
                while self.map.is_touching_map(self):
                    self.rect.x += 1

            # Ge the right column nearest to the player
            max_right_column = None
            for i in range(self.rect.x + self.rect.width, self.rect.x + self.rect.width // 2):
                if columns.get(i) != None:
                    max_right_column = i
                    break
            
            if max_right_column != None and len(columns.get(max_right_column)) > 20:
                while self.map.is_touching_map(self):
                    self.rect.x -= 1
            
            
            if self.touch_down == True :
                self.vy = 0
                while self.map.is_touching_map(self):
                    self.rect.y -= 1

        # Player limits
        if self.rect.bottom >= GameConfig.WINDOW_H:
            self.vy = 0


    def has_touched_map(self, points):
        self.points = points

    def draw(self, screen):
        super().draw(screen)

    def get_cursor_position(self, enemy):
        cursor_x = enemy.rect.x - self.rect.x
        speed = GameConfig.MASS_PROJ * GameConfig.GRAVITY
        temp_worm_x = self.rect.x + self.rect.width/2 - self.rect.width/2
        temp_worm_y = self.rect.y + self.rect.height/2 - self.rect.height/2

        enemy_x = enemy.rect.x + enemy.rect.width/2 - enemy.rect.width/2
        enemy_y = enemy.rect.y + enemy.rect.height/2 - enemy.rect.height/2

        projectile_x = temp_worm_x
        projectile_y = temp_worm_y

        cursor_y = 0
        point_found = False
        while cursor_y > enemy.rect.y and point_found == False:
            racine = abs(math.sqrt((temp_worm_x - cursor_x)** 2 + (temp_worm_y - cursor_y)**2))

            t = 0
            while projectile_y > enemy_y and point_found == False:
                projectile_x = (cursor_x - self.rect.x) / racine * speed * t
                projectile_y = -0.5 * GameConfig().PI * t**2 - (self.cursor_y - self.rect.y) / racine * speed * t + enemy.rect.height
                t += 1
                if projectile_x == enemy_x and projectile_y == enemy_y:
                    point_found = True
            
            cursor_y += 1

        return projectile_x, projectile_y

    def worm_brain(self, ennemy, camera):
        print("IA running")
        cursor_x, cursor_y = self.get_cursor_position(ennemy)
        new_projectile = Projectile(self, 20, 20, GameConfig.MASS_PROJ, cursor_x, cursor_y, camera)
        return new_projectile

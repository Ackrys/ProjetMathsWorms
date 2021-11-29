# Class Worm
#       - Correspond à un ver

# Import des modules
# import pygame
from content.projectile import Projectile
from game_config import *
from game_state import *
from engine.animation import Animation
from engine.entity import Entity

import math
class Worm(Entity) :

    def __init__(self, x, y, height, width, mass, map, id):
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
        self.is_dead = False

        self.will_touch_map = False

        self.max_hp = GameConfig.WORM_HP
        self.hp = GameConfig.WORM_HP

        self.offset_x = 0
        self.offset_y = 0

        self.id = id

    def advance_state(self):
        super().advance_state()

        # Gravity
        if len(self.points) < 1: # No collision with map
            self.vy = self.vy+GameConfig.GRAVITY*GameConfig.DT*self.mass
        else : # Collision with map
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

            # Ge the right column nearest to the player
            max_right_column = None
            for i in range(self.rect.x + self.rect.width, self.rect.x + self.rect.width // 2):
                if columns.get(i) != None:
                    max_right_column = i
                    break

            # Touching right
            if max_right_column != None and len(columns.get(max_right_column)) > 20:
                while self.map.is_touching_map(self):
                    self.rect.x -= 1

            # Touching left
            if max_left_column != None and len(columns.get(max_left_column)) > 20:
                while self.map.is_touching_map(self):
                    self.rect.x += 1

            # Touching down
            if self.touch_down == True :
                self.vy = 0
                while self.map.is_touching_map(self):
                    self.rect.y -= 1

        # Player limits
        if self.rect.bottom >= GameConfig.WINDOW_H:
            self.vy = 0

    # Display methods
    def applyOffset(self, x, y):
        super().applyOffset(x, y)
        self.offset_x = x
        self.offset_y = y

    def has_touched_map(self, points):
        self.points = points

    def draw(self, screen):
        super().draw(screen)
        # Draw HP Bar
        bar_width = 50
        pos_x = self.rect_display.x + self.rect_display.width // 2 - bar_width // 2
        pos_y = self.rect_display.y - 5
        pygame.draw.rect(screen, (255, 0, 0), (pos_x + self.offset_x, pos_y + self.offset_y, bar_width, 5))
        pygame.draw.rect(screen, (0, 255, 0), (pos_x + self.offset_x, pos_y + self.offset_y, bar_width * self.hp / self.max_hp, 5))

    def get_cursor_position(self, enemy):
        speed = GameConfig.MASS_PROJ * GameConfig.GRAVITY
        temp_worm_x = self.rect.x + self.rect.width/2 - self.rect.width/2
        temp_worm_y = self.rect.y + self.rect.height/2 - self.rect.height/2

        enemy_x = enemy.rect.x + enemy.rect.width/2 - enemy.rect.width/2
        enemy_y = enemy.rect.y + enemy.rect.height/2 - enemy.rect.height/2

        projectile_x = 0
        projectile_y = 0

        cursor_y = 0
        point_found = False
        cursor_x = 0
 
        for alpha in range(0, 360):
            rad_alpha = alpha * GameConfig.PI / 180
            attendu_y = -GameConfig.GRAVITY / 2 * (enemy_y / (speed * math.cos(rad_alpha))) + speed * math.sin(rad_alpha) * enemy_x / math.cos(rad_alpha) * self.rect.height
            
            if enemy_y + 10 > attendu_y and enemy_y - 10 < attendu_y:
                return rad_alpha

    
        # while cursor_x < GameConfig.WINDOW_GAME_W and point_found == False:
        #     cursor_x += 1
            
        #     while cursor_y < enemy_y and point_found == False:
        #         racine = abs(math.sqrt((temp_worm_x - cursor_x)** 2 + (temp_worm_y - cursor_y)**2))
        #         t = 0
        #         while projectile_y < enemy_y and point_found == False:
        #             projectile_x = abs((cursor_x - temp_worm_x)) / racine * speed * t
        #             projectile_y = abs(-0.5 * GameConfig().PI * t**2 - abs((cursor_y - temp_worm_y)) / racine * speed * t + 20)
 

        #             if projectile_x == enemy_x and projectile_y == enemy_y:
        #                 point_found = True
        #                 print("Trajectoire trouvé ", point_found)
        #             t += 1

        #             print(cursor_x)
        #             print(cursor_y)
        #         print("Cur avant" , cursor_y)
        #         cursor_y += 1
        #         projectile_x = 0
        #         projectile_y = 0
        #         print("Cur après" , cursor_y)
        return alpha

    def worm_brain(self, ennemy, camera):
        alpha = self.get_cursor_position(ennemy)
        # cursor_x, cursor_y = self.get_cursor_position(ennemy)
        # print("cursor postion ", cursor_x, " | ", cursor_y)
        new_projectile = Projectile(self, 20, 20, GameConfig.MASS_PROJ, alpha, camera)
        return new_projectile

    def take_damages(self, damages):
        self.hp -= damages
        if self.hp <= 0:
            return True
        else:
            return False

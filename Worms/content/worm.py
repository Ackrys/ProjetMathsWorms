# Class Worm
#       - Correspond à un ver

# Import des modules
from content.projectile import Projectile
from game_config import *
from game_state import *
from engine.animation import Animation
from engine.entity import Entity

import math
class Worm(Entity) :

    def __init__(self, x, y, height, width, mass, map, id, team):
        super().__init__(x, y, height, width, mass, "standing.png")

        self.team = team

        if self.team == "BLUE":
            self.define_animation("idle", Animation(["bluestanding.png"]))
            self.define_animation("walk_right", Animation(["blueR1.png", "blueR2.png", "blueR3.png", "blueR4.png", "blueR5.png", "blueR6.png", "blueR7.png", "blueR8.png", "blueR9.png"]))
            self.define_animation("walk_left", Animation(["blueL1.png", "blueL2.png", "blueL3.png", "blueL4.png", "blueL5.png", "blueL6.png", "blueL7.png", "blueL8.png", "blueL9.png"]))
        else:
            self.define_animation("idle", Animation(["redstanding.png"]))
            self.define_animation("walk_right", Animation(["redR1.png", "redR2.png", "redR3.png", "redR4.png", "redR5.png", "redR6.png", "redR7.png", "redR8.png", "redR9.png"]))
            self.define_animation("walk_left", Animation(["redL1.png", "redL2.png", "redL3.png", "redL4.png", "redL5.png", "redL6.png", "redL7.png", "redL8.png", "redL9.png"]))

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

    # Permet de cacluler les a, b, c qui permettront de calculer la parabole que prendra le projectile
    def get_var_funct_parab_position(self, enemy):
        speed = GameConfig.MASS_PROJ * GameConfig.GRAVITY
        temp_worm_x = self.rect.x + self.rect.width/2 - self.rect.width/2
        temp_worm_y = self.rect.y + self.rect.height/2 - self.rect.height/2

        enemy_x = enemy.rect.x + enemy.rect.width/2 - enemy.rect.width/2
        enemy_y = enemy.rect.y + enemy.rect.height/2 - enemy.rect.height/2


        a = math.sqrt(speed**2 -1)/(2 * enemy_x)
        
        b = -(a*(temp_worm_x**2 - enemy_x**2) + enemy_y - temp_worm_y) / (temp_worm_x - enemy_x)

        c = -a*(enemy_x)**2 - b * enemy_x + enemy_y

        return a,b,c

    # Actions de l'IA
    def worm_brain(self, ennemy, camera):
        a, b, c = self.get_var_funct_parab_position(ennemy)
        # Déclenchement de l'envoie du projectile de l'IA
        new_projectile = Projectile(self, 20, 20, GameConfig.MASS_PROJ, a, b, c, camera, ennemy)
        
        return new_projectile

    def take_damages(self, damages):
        self.hp -= damages
        if self.hp <= 0:
            return True
        else:
            return False

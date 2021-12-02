# Class Projectile
#       - Correspond à un projectile

# Import des modules
import pygame
from game_config import *
from engine.animation import Animation
from engine.entity import Entity
import math
import time


class Projectile(Entity):
    # Temps initial
    t0 = 0
    # Point x initial
    x0 = 0
    # Point y initial
    y0 = 0
    # Taux de dégât produit par le projectile
    damage = 70

    def __init__(self, worm, height, width, mass, a, b, c, camera, ennemy):
        self.ennemy = ennemy

        # Définit les variables pour calculer la trajectoire de l'IA
        self.a = a
        self.b = b
        self.c = c

        # Définit la position du curseur lors du clique
        self.cursor_x, self.cursor_y = pygame.mouse.get_pos()

        # Permet de placer les points x et y du worm en son centre
        self.pos_x = worm.rect.x + worm.rect.width/2 - worm.rect.width/2
        self.pos_y = worm.rect.y + worm.rect.height/2 - worm.rect.height/2

        # Construit l'Entité
        super().__init__(self.pos_x, self.pos_y, height, width, mass, "missile.png")

        # Définit les x et y initiaux du worm en son centre
        self.x0 = worm.rect_display.x + worm.rect_display.width/2 - self.rect_display.width/2
        self.y0 = worm.rect_display.y + worm.rect_display.height/2 - self.rect_display.height/2

        # Ajout de la position de la caméra pour replacer correctement le point du worm
        self.x0 += camera.x
        self.y0 += camera.y

        # Définit la direction du vecteur vitesse (speed)
        self.r = abs(math.sqrt((self.rect.x - self.cursor_x)** 2 + (self.rect.y - self.cursor_y)**2))

        # Définit le temps initial
        self.t0 = round(time.time() * 1000)
        

    def draw(self, screen):
        super().draw(screen)

    def advance_state(self):
        self.pull()
        super().advance_state()

    # Calcul les points de la trajectoire que prend le projectile selon la position du curseur du joueur
    # t est le temps initial
    # mass représente la masse du projectile
    def trajectoire(self, t, mass):
        # Vitesse (constante) du projectile
        speed = mass * GameConfig.GRAVITY
        
        # Calcul des points x et y qu'aura le projectile selon l'équation horaire
        x = (self.cursor_x-self.x0)/self.r*speed*t
        y = -0.5*GameConfig.GRAVITY*t**2-(self.cursor_y-self.y0)/self.r*speed*t+self.rect.height
        
        # Permet d'adapter les points x et y du projectile selon la position du worm
        self.rect.x = x + self.pos_x
        self.rect.y = -(y) + self.pos_y

    # Calcul les points de la trajectoire que prend le projectile selon
    # t est le temps initial
    def trajectoire_IA(self, t):
        # Définition du x pour que chaque image le projectile avance d'un pixel (ce qui fait que l'IA ne peut pas tirer en arrière (vers la gauche))
        x = t
        # Définition y selon une fonction parabolique
        y = self.a*(x**2)+self.b*x+self.c

        # Permet d'adapter les points x et y du projectile selon la position du worm
        self.rect.x = x + self.pos_x
        self.rect.y = -(y) + self.pos_y

    # Appel la fonction trajectoire (en fonction de si c'est un joueur physique ou au tour de l'IA)
    def pull(self):
        if self.a == -1 and self.b == -1 and  self.c == -1:
            self.trajectoire((round(time.time() * 1000) - self.t0) / 100, self.mass)
        else:
            self.trajectoire_IA((round(time.time() * 1000) - self.t0) / 100)

        
    # Permet de savoir si le projectile est sortie de la fenêtre de jeu
    # Retourne True si le projectile False sinon
    def out_window(self):
        if self.rect.y > GameConfig.WINDOW_GAME_H:
            return True
        
        return False
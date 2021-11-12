# Fichier principal


# Import des modules
import pygame
from game_config import *


# Boucle principale
def game_loop():
    quitting = False
    while not quitting :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                quitting = True

# Configuration et lancement du jeu
def main() :
    pygame.init()
    GameConfig.init()

    window = pygame.display.set_mode((GameConfig.WINDOW_W,GameConfig.WINDOW_H))
    pygame.display.set_caption("Avoid Bats")

    game_loop()

    pygame.quit()
    quit()


main()

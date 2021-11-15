# Fichier principal


# Import des modules
import pygame
from game_state import *
from game_config import *
from move import *




def get_next_move():
        next_move = Move()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            next_move.right = True
        if keys[pygame.K_LEFT]:
            next_move.left = True
        if keys[pygame.K_UP]:
            next_move.jump = True
        return next_move




# Boucle principale
def game_loop(window):
    game_state = GameState()

    quitting = False
    while not quitting : # Boucle de jeu

        # Gestion des évènements
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                quitting = True

        # Détection des mouvements du joueur
        next_move = get_next_move()

        # Application des mouvements du joueur
        game_state.advance_state(next_move)
        
        # Affichage
        game_state.draw(window)
        pygame.display.update()

        # Délai
        pygame.time.delay(20)

# Configuration et lancement du jeu
def main() :
    pygame.init()
    GameConfig.init()

    window = pygame.display.set_mode((GameConfig.WINDOW_W,GameConfig.WINDOW_H))
    pygame.display.set_caption("Avoid Bats")

    game_loop(window)

    pygame.quit()
    quit()


main()

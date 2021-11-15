# Fichier principal


# Import des modules
import pygame

from game_state import *
from game_config import *

# Boucle principale
def game_loop(window):
    # Créer l'état de jeu
    game_state = GameState()

    game_over = False
    quitting = False

    while not game_over and not quitting : # Boucle de jeu

        # Gestion des évènements
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                quitting = True

        # A remplacer -> Fond noir
        window.fill((0, 0, 0))



        # Fait avancer l'état de jeu
        game_state.advance_state()






        # Affichage des modifications
        game_state.draw(window)







        # Update de l'interface
        pygame.display.update()

        # Délai
        pygame.time.delay(20)

# Configuration et lancement du jeu
def main() :
    pygame.init()

    # Initialisation de la fenêtre
    window = pygame.display.set_mode((GameConfig.WINDOW_W,GameConfig.WINDOW_H))
    pygame.display.set_caption("Worms")

    # Initialisation du jeu
    GameConfig.init()

    # Lancement de la boucle principale
    game_loop(window)

    pygame.quit()
    quit()


main()


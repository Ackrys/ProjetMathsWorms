# Fichier principal


# Import des modules
import pygame
from engine.inputs import Input

from game_state import *
from game_config import *

def get_inputs():
        next_move = Input()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            next_move.right = True
        if keys[pygame.K_LEFT]:
            next_move.left = True
        if keys[pygame.K_UP]:
            next_move.up = True
        if keys[pygame.K_DOWN]:
            next_move.down = True
        if keys[pygame.K_a]:
            next_move.zoom_in = True
        if keys[pygame.K_z]:
            next_move.zoom_out = True
        return next_move

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
        
        inputs = get_inputs()

        # A remplacer -> Fond noir
        window.fill((0, 0, 0))



        # Fait avancer l'état de jeu
        game_state.advance_state(inputs)






        # Affichage des modifications
        game_state.draw(window)







        # Update de l'interface
        pygame.display.update()

        # Délai
        pygame.time.delay(20) # 20

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


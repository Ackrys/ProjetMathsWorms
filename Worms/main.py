# Fichier principal


# Import des modules
import pygame
from engine.inputs import Input

from game_state import *
from game_config import *

def get_inputs():
        next_move = Input()
        keys = pygame.key.get_pressed()
        # Camera
        if keys[pygame.K_d]:
            next_move.camera_right = True
        if keys[pygame.K_q]:
            next_move.camera_left = True
        if keys[pygame.K_z]:
            next_move.camera_up = True
        if keys[pygame.K_s]:
            next_move.camera_down = True
        if keys[pygame.K_a]:
            next_move.camera_zoom_in = True
        if keys[pygame.K_e]:
            next_move.camera_zoom_out = True

        # Player movements
        if keys[pygame.K_UP]:
            next_move.player_move_up = True
        if keys[pygame.K_DOWN]:
            next_move.player_move_down = True
        if keys[pygame.K_LEFT]:
            next_move.player_move_left = True
        if keys[pygame.K_RIGHT]:
            next_move.player_move_right = True

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
        window.fill((25, 25, 25))



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


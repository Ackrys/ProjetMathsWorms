# Fichier principal


# Import des modules
import pygame
from game_state import *
from game_config import *
from move import *



# Renvoie les prochains mouvements effectués par le joueur
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

def display_message(window,text,font_size,x,y) :
    img = GameConfig.FONT20.render(text,True,GameConfig.GREY)
    if font_size == 150 :
        img = GameConfig.FONT150.render(text,True,GameConfig.GREY)
    display_rect = img.get_rect()
    display_rect.center=(x,y)
    window.blit(img,display_rect)

def play_again() :
    pygame.time.delay(2000)
    while True :
        for event in pygame.event.get([pygame.KEYDOWN,pygame.QUIT]) :
            if event.type == pygame.QUIT :
                return False
            elif event.type == pygame.KEYDOWN :
                return True
        pygame.time.delay(500)

# Boucle principale
def game_loop(window):
    game_state = GameState()
    game_over = False
    quitting = False
    while not game_over and not quitting : # Boucle de jeu

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

        # Test jeu terminé
        if game_state.is_over() :
            display_message(window,"Perdu!", 150, (GameConfig.WINDOW_W/2),(GameConfig.WINDOW_H/2-50))
            display_message(window,"Appuyer sur une touche pour continuer", 20, (GameConfig.WINDOW_W/2),(GameConfig.WINDOW_H/2+50))
            game_over = True

        pygame.display.update()
        # Délai
        pygame.time.delay(20)

# Configuration et lancement du jeu
def main() :
    pygame.init()

    # Initialisation de la fenêtre
    window = pygame.display.set_mode((GameConfig.WINDOW_W,GameConfig.WINDOW_H))
    pygame.display.set_caption("Avoid Bats")

    # Initialisation du jeu
    GameConfig.init()
    Player.init_sprites()
    Bat.init_sprites()

    # Lancement de la boucle principale
    game_loop(window)
    if play_again() :
        main()
    pygame.quit()
    quit()


main()

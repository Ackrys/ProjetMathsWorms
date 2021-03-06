#!/usr/bin/python
# -*- coding: utf-8 -*
# Fichier principal


# Import des modules
import pygame
from engine.inputs import Input

from game_state import *
from menu_state import *
from finish_state import *
from game_config import *
from content.projectile import *


def get_inputs(game_state):
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
        
        #player action
        if keys[pygame.K_t]:
            next_move.player_shoot = True
            
        return next_move

# Boucle principale
def game_loop(window):
    # Créer l'etat de jeu menu
    menu_state = MenuState()

    display_menu = True
    quitting = False

    while display_menu and not quitting: # Boucle de menu
        
        # Evenements
        click = False
        pos_click = None

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                quitting = True
            if pygame.mouse.get_pressed()[0] :
                click = True
                pos_click = pygame.mouse.get_pos()





        # Fond uni
        window.fill(GameConfig.COLOR_SKY)





        # Avancer le jeu
        display_menu = menu_state.advance_state(click, pos_click)







        # Afficher le jeu
        menu_state.draw(window)






        # Update de l'interface
        pygame.display.update()

        # Délai
        # pygame.time.delay(20) # 20
        
    # Menu de chargement
    window.fill(GameConfig.COLOR_SKY)
    menu_state.draw_loading(window)
    pygame.display.update()

    # Créer l'etat de jeu jouable
    game_state = GameState()

    game_over = False
    winner = None

    while not game_over and not quitting : # Boucle de jeu

        # Gestion des évènements
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                quitting = True
        
        inputs = get_inputs(game_state)



        # Fond uni
        window.fill(GameConfig.COLOR_SKY)



        # Fait avancer l'état de jeu
        winner = game_state.advance_state(inputs)
        if winner != None :
            game_over = True





        # Affichage des modifications
        game_state.draw(window)







        # Update de l'interface
        pygame.display.update()

        # Délai
        pygame.time.delay(20) # 20

    # Créer l'etat de jeu menu
    finish_state = FinishState(winner)

    display_menu = True

    while display_menu and not quitting: # Boucle de menu
        
        # Evenements
        click = False
        pos_click = None

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                quitting = True
            if pygame.mouse.get_pressed()[0] :
                click = True
                pos_click = pygame.mouse.get_pos()





        # Fond uni
        window.fill(GameConfig.COLOR_SKY)





        # Avancer le jeu
        display_menu = finish_state.advance_state(click, pos_click)







        # Afficher le jeu
        finish_state.draw(window)






        # Update de l'interface
        pygame.display.update()

        # Délai
        # pygame.time.delay(20) # 20
       
    return not display_menu

# Configuration et lancement du jeu
def main() :
    pygame.init()

    # Initialisation de la fenêtre
    window = pygame.display.set_mode((GameConfig.WINDOW_W,GameConfig.WINDOW_H))
    pygame.display.set_caption("Worms")

    # Initialisation du jeu
    GameConfig.init()

    # Lancement de la boucle principale de jeu
    while game_loop(window):
        game_loop(window)

    pygame.quit()
    quit()


main()


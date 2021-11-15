# Class Game State
#       - Correspond à l'état de jeu


# Import des modules
from player import *
from bat import *
import random


class GameState :
    def __init__(self):
        self.player = Player(20)
        self.score = 0

        # Chauve-souris
        self.bats = []
        self.time_till_new_bat = GameConfig.TICKS_BETWEEN_BATS

    def advance_state(self,next_move):
        self.player.advance_state(next_move)

        # Chauve-souris
        for b in self.bats :
            b.advance_state()

            if b.is_dead() :
                self.score += 1

        # Ticks Chauve-souris
        if self.time_till_new_bat == 0 :
            self.time_till_new_bat = GameConfig.TICKS_BETWEEN_BATS
            vx = random.randint(GameConfig.BAT_MIN_SPEED,GameConfig.BAT_MAX_SPEED)
            vx = vx*random.choice([-1,1])
            y = random.randint(
                GameConfig.Y_PLATEFORM-2*GameConfig.PLAYER_H,
                GameConfig.Y_PLATEFORM-GameConfig.BAT_H)
            if vx < 0 :
                self.bats.append(Bat(GameConfig.WINDOW_W,y,vx))
            else :
                self.bats.append(Bat(-GameConfig.BAT_W,y,vx))
        self.time_till_new_bat-=1

    def draw(self, window):
        window.blit(GameConfig.BACKGROUND_IMG,(0,0))
        self.player.draw(window)

        # Chauve-souris
        for b in self.bats :
            b.draw(window)

            if b.is_dead() :
                self.bats.remove(b)

        # Affiche le score
        img = GameConfig.FONT20.render("score : " + str(self.score),True,GameConfig.GREY)
        display_rect = img.get_rect()
        display_rect.center=(50,10)
        window.blit(img,display_rect)

    def is_over(self) :
        for b in self.bats :
            if self.player.is_touching(b) :
                return True
        return False

    def new_level(score):
        if score%5 == 0 and score != 0:
            GameConfig.BAT_MIN_SPEED += 5
            GameConfig.BAT_MAX_SPEED += 10
            GameConfig.TICKS_BETWEEN_BATS -= 5
        return GameConfig.TICKS_BETWEEN_BATS, GameConfig.BAT_MIN_SPEED

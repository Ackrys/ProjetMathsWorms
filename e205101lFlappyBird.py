import pygame
import time
from random import *

class GameConfig:
    windowW = 800
    windowH = 500
    blue = (113,177,227)
    white = (255,255,255)
    imgBalloon = pygame.image.load('Balloon.png')
    balloonW = 50
    balloonH = 66
    imgUpperCloud = pygame.image.load('UpperCloud.png')
    imgLowerCloud = pygame.image.load('LowerCloud.png')
    cloudW = 300
    cloudH = 300
    def displayMessage(window,text,fontSize,x,y) :
        font = pygame.font.Font('BradBunR.ttf',fontSize)
        img = font.render(text,True,GameConfig.white)
        displayRect = img.get_rect()
        displayRect.center=(x,y)
        window.blit(img,displayRect)

class GameState :
    def __init__(self):
        self.balloonX=150
        self.balloonY=200
        self.score = 0
        self.initCloud(6)
    def initCloud(self,speed):
        self.cloudX = GameConfig.windowW
        self.cloudY = randint(-GameConfig.cloudH,20)
        self.cloudSpace = 3*GameConfig.balloonH
        self.cloudSpeed = speed
    def draw(self, window) :
        window.fill(GameConfig.blue)
        window.blit(GameConfig.imgBalloon,(self.balloonX,self.balloonY))
        window.blit(GameConfig.imgUpperCloud,(self.cloudX,self.cloudY))
        window.blit(GameConfig.imgLowerCloud,(self.cloudX,self.cloudY + GameConfig.cloudH + self.cloudSpace))
        GameConfig.displayMessage(window,"Score : " + str(self.score), 16, 50, 10)
    def advanceState(self,nextM) :
        self.balloonY+=nextM
        self.cloudX -= self.cloudSpeed
    def isOver(self):
        return (
        self.balloonY < -10 or self.balloonY + GameConfig.balloonH > GameConfig.windowH + 10
        or ((self.balloonX + GameConfig.balloonW > self.cloudX + 10
        and self.balloonX < self.cloudX + GameConfig.cloudW - 10)
        and ((self.balloonY + GameConfig.balloonH > self.cloudY + GameConfig.cloudH + self.cloudSpace + 10
        or self.balloonY < self.cloudY + GameConfig.cloudH - 10))
        )
        )
    def newLevel(self, score):
        if self.score%3 == 0 and self.score != 0:
            self.cloudSpeed += 2
            self.initCloud(self.cloudSpeed)
        return self.cloudSpeed, self.cloudSpace

class Move :
    Up = -5
    Down = 5

def gameLoop(window, horloge) :
    game_over = False
    gameState = GameState()
    nextMove = 0
    nextScore = False
    while not game_over :
        gameState.draw(window)
        horloge.tick(100)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                game_over = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
                nextMove = Move.Up
            if event.type == pygame.KEYUP :
                nextMove = Move.Down
        if gameState.isOver() == True:
            GameConfig.displayMessage(window, "Boom!", 150, (GameConfig.windowW/2),(GameConfig.windowH/2-50))
            GameConfig.displayMessage(window,"Appuyer sur une touche pour continuer!", 20, (GameConfig.windowW/2),(GameConfig.windowH/2+50))
            game_over = True
        if gameState.cloudX < - GameConfig.cloudW :
            gameState.initCloud(gameState.cloudSpeed)
            gameState.score += 1
            nextScore = True
        if nextScore == True :
            gameState.newLevel(gameState.score)
            nextScore = False
        nextMove = getIACommand(gameState)
        gameState.advanceState(nextMove)
        pygame.display.update()

def playAgain() :
    time.sleep(2)
    while True :
        for event in pygame.event.get([pygame.KEYDOWN,pygame.QUIT]) :
            if event.type == pygame.QUIT :
                return False
            elif event.type == pygame.KEYDOWN :
                return True
        time.sleep(0.5)

def getIACommand(GameState):
    if GameState.balloonY < GameState.cloudY + GameConfig.cloudH + 20 :
        return Move.Down
    elif GameState.balloonY > GameState.cloudY + GameConfig.cloudH + GameState.cloudSpace :
        return Move.Up
    else :
        return Move.Up

def main():
    pygame.init()
    horloge = pygame.time.Clock()
    window = pygame.display.set_mode(
        (
            GameConfig.windowW,
            GameConfig.windowH
        )
    )
    pygame.display.set_caption("Flappy Balloon")
    gameLoop(window, horloge)
    if(playAgain()):
        main()
    pygame.quit()
    quit()

main()

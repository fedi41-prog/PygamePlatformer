import os
os.system('pip install pygame')
import pygame
from GameV1.core.game import Game

if __name__ == "__main__" :
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

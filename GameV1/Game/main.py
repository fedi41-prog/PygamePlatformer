
import pygame
from Game.core.game import Game

def main():
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

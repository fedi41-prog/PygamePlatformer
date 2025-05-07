
import pygame
from Game.entities.player import Player

class GameScene:
    def __init__(self, game):
        self.game = game
        self.player = Player(100, 100)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def update(self):
        self.player.update()

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Schwarz
        self.player.draw(screen)

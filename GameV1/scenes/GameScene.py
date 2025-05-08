import pygame
from GameV1.sprites.player import Player
from GameV1.settings import *
from GameV1.sprites.Tiles.tiletest import TileTest

class GameScene:
    def __init__(self, game):
        self.game = game
        self.player = Player(100, 50)
        self.block1 = TileTest(100, 200)
        self.block2 = TileTest(170, 200)

        self.background_image = pygame.image.load("assets/images/Backgrounds/bg_grasslands.png")
        self.rect = self.background_image.get_rect()
        self.rect.x, self.rect.y = WIDTH/2 - self.rect.width/2, HEIGHT/2 - self.rect.height/2

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def update(self):
        self.player.update([self.block1, self.block2])

    def draw(self, screen):
        screen.blit(self.background_image, self.rect)
        self.player.draw(screen)
        self.block1.draw(screen)
        self.block2.draw(screen)
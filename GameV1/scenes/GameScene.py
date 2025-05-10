import pygame
from GameV1.sprites.player import Player
from GameV1.settings import *
from GameV1.sprites.Tiles.static import StaticBlock

class GameScene:
    def __init__(self, game):
        self.game = game
        self.player = Player(100, 50)
        self.blocks = [

            StaticBlock(100, 200, "grassLeft.png"),
            StaticBlock(170, 200, "grassMid.png"),
            StaticBlock(240, 200, "grassRight.png"),
            StaticBlock(170, 130, "boxAlt.png")

        ]

        self.background_image = pygame.image.load("assets/images/Backgrounds/bg_grasslands.png")
        self.rect = self.background_image.get_rect()
        self.rect.x, self.rect.y = WIDTH/2 - self.rect.width/2, HEIGHT/2 - self.rect.height/2

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def update(self):
        self.player.update(self.blocks)

    def draw(self, screen):
        screen.blit(self.background_image, self.rect)

        for b in self.blocks:
            b.draw(screen)

        self.player.draw(screen)

import pygame

from GameV1.core.camera import Camera
from GameV1.sprites.player import Player
from GameV1.settings import *
from GameV1.sprites.Tiles.static import StaticBlock

class GameScene:
    def __init__(self, game):
        self.game = game
        self.player = Player(100, 50)
        self.blocks = [

            StaticBlock(100, 270, "grassLeft.png"),
            StaticBlock(170, 270, "grassHillLeft2.png"),
            StaticBlock(240, 270, "grassCenter.png"),
            StaticBlock(310, 270, "grassCenter.png"),
            StaticBlock(380, 270, "grassCenter.png"),
            StaticBlock(170, 200, "grassHillLeft.png"),
            StaticBlock(240, 200, "grassMid.png"),
            StaticBlock(310, 200, "grassMid.png"),
            StaticBlock(380, 200, "grassMid.png"),
            StaticBlock(310, 130, "boxAlt.png"),
            StaticBlock(450, 200, "castleHalfMid.png"),
            StaticBlock(520, 200, "castleHalfMid.png"),
            StaticBlock(590, 200, "castleHalfMid.png"),
            StaticBlock(660, 200, "castleHalfMid.png"),
            StaticBlock(730, 200, "castleHalfMid.png"),

        ]

        self.background_image = pygame.image.load("assets/images/Backgrounds/bg_grasslands.png")
        self.rect = self.background_image.get_rect()
        self.rect.x, self.rect.y = WIDTH/2 - self.rect.width/2, HEIGHT/2 - self.rect.height/2

        self.level_width = 2000
        self.level_height = HEIGHT + 500

        self.camera = Camera(800, 600, self.level_width, self.level_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def update(self):
        self.player.update(self.blocks)
        self.camera.update(self.player.hitbox)

    def draw(self, screen):

        # Zeichnen
        screen.blit(self.background_image, self.rect)

        for b in self.blocks:
            b.draw(screen, self.camera)

        self.player.draw(screen, self.camera)

        pygame.display.flip()


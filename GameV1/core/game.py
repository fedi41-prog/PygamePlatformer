import pygame

from GameV1.scenes.GameScene import GameScene
from GameV1.settings import *
from GameV1.assets.assets import AssetManager

class Game:
    def __init__(self):
        print("init game...")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)


        #load spritesheets (:
        AssetManager.load_all_sheets_from_folder("assets/images/spritesheets")


        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = GameScene(self)

    def run(self):
        while self.running:
            self.scene.handle_events()
            self.scene.update()
            self.scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
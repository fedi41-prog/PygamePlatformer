
import pygame
from GameV1.settings import *
from GameV1.scenes.game_scene import GameScene

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
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

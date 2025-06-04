import pygame
from GameV1.assets.assets import AssetsManager


class Deco:
    def __init__(self, x, y, texture, game):
        self.game = game
        self.image = AssetsManager.get(texture)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        pass
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
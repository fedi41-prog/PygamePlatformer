import pygame
from GameV1.assets.assets import AssetManager


class Deco:
    def __init__(self, x, y, sheet, texture, game):
        self.game = game
        self.image = AssetManager.get(sheet, texture)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        pass
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
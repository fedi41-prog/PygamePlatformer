import pygame
from GameV1.assets.assets import AssetManager


class StaticBlock:
    def __init__(self, x, y, texture):
        self.image = AssetManager.get(texture)
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
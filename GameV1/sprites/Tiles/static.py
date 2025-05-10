import pygame
from GameV1.assets.assets import AssetManager


class StaticBlock:
    def __init__(self, x, y, name):
        self.image = AssetManager.get("tiles", name)
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
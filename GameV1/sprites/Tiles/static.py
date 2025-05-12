import pygame
from GameV1.assets.assets import AssetManager


class StaticBlock:
    def __init__(self, x, y, name, is_slope=False):
        self.image = AssetManager.get("tiles", name)
        self.mask = pygame.mask.from_surface(self.image)

        self.is_slope = is_slope

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
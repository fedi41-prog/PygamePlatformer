import pygame
from GameV1.tools.spritesheet import SpriteSheet
from GameV1.assets.assets import AssetManager





class TileTest:
    def __init__(self, x, y):
        self.image = AssetManager.get("tiles", "box.png")
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
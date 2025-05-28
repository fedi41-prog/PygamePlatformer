import pygame

from GameV1.assets.assets import AssetManager
from GameV1.settings import VIRTUAL_WIDTH


class AdminDisplay:
    def __init__(self, game, pos=(VIRTUAL_WIDTH-120, 35)):
        self.game = game
        self.position = pos

        self.font = AssetManager.get_font("DebugFont")

    def update(self):
        pass  # Falls etwas animiert oder dynamisch ist

    def draw(self, surface):
        if self.game.scene.admin:
            text = self.font.render("ADMIN", True, (90, 160, 90))
            text_rect = text.get_rect()
            text_rect.left = self.position[0]
            text_rect.centery = self.position[1]
            surface.blit(text, text_rect)

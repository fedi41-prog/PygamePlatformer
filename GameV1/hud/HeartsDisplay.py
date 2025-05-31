import pygame

from GameV1.assets.assets import AssetManager
from GameV1.settings import VIRTUAL_WIDTH, VIRTUAL_HEIGHT


class HeartsDisplay:
    def __init__(self, game, pos=(VIRTUAL_WIDTH - 225, 5)):
        self.game = game
        self.position = pos

        self.hearts = 0

        self.image_full = AssetManager.get("hud/hud_heartFull")
        self.image_half = AssetManager.get("hud/hud_heartHalf")
        self.image_empty = AssetManager.get("hud/hud_heartEmpty")


    def update(self):

        self.hearts = self.game.scene.player.hearts

    def draw(self, surface):

        for i in range(1, 4):
            if self.hearts+0.5 > i:
                surface.blit(self.image_full, (self.position[0] + i*56, 5))
            elif self.hearts+1 > i:
                surface.blit(self.image_half, (self.position[0] + i * 56, 5))
            else:
                surface.blit(self.image_empty, (self.position[0] + i * 56, 5))








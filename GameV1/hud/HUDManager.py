import pygame
from GameV1.assets.assets import AssetManager
from GameV1.hud.adminDisplay import AdminDisplay
from GameV1.hud.coinDisplay import CoinDisplay


class HUDManager:
    def __init__(self, game):
        self.game = game
        self.elements = []

        self.coin_display = CoinDisplay(game)
        self.elements.append(self.coin_display)
        self.admin_display = AdminDisplay(game)
        self.elements.append(self.admin_display)

    def update(self):
        for element in self.elements:
            element.update()

    def draw(self, surface):
        for element in self.elements:
            element.draw(surface)

    def set_coins(self, amount):
        self.coin_display.set_amount(amount)

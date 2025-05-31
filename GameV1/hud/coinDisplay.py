import pygame

from GameV1.assets.assets import AssetManager


class CoinDisplay:
    def __init__(self, game, pos=(20, 20)):
        self.game = game
        self.position = pos
        self.amount = 0

        self.icon = pygame.transform.scale(AssetManager.get("hud/hud_coins"), (32, 32))
        self.font = AssetManager.get_font("fonts/HudFont", 30)

    def set_amount(self, amount):
        self.amount = amount
    def increase_amount(self, amount):
        self.amount += amount

    def update(self):
        pass  # Falls etwas animiert oder dynamisch ist

    def draw(self, surface):
        surface.blit(self.icon, self.position)
        text = self.font.render(f"x {self.amount}", True, (90, 90, 90))
        text_rect = text.get_rect()
        text_rect.left = self.position[0] + self.icon.get_width() + 10
        text_rect.centery = self.position[1] + self.icon.get_height() // 2
        surface.blit(text, text_rect)

import pygame
from GameV1.assets.assets import AssetManager

class Coin:
    def __init__(self, x, y, sheet, texture, game):
        self.game = game
        self.image = AssetManager.get(sheet, texture)
        self.mask = pygame.mask.from_surface(self.image)

        self.dir = 1
        self.step = 0

        self.to_remove = False

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        player = self.game.scene.player
        if self.step % 2:
            self.rect.y += self.dir
        self.step += 1

        if self.step >= 20:
            self.step = 0
            if self.dir == 1:
                self.dir = -1
            else:
                self.dir = 1

        # Pixelgenaue Kollision: Offset von Spieler- zu Flag-Maske
        offset = (self.rect.x - player.rect.x, self.rect.y - player.rect.y)
        # overlap gibt None oder den ersten überlappenden Pixel zurück
        if player.mask.overlap(self.mask, offset):
            self.to_remove = True
            player.game.scene.hud_manager.coin_display.increase_amount(1)


    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
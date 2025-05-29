import pygame
from GameV1.assets.assets import AssetManager

class Flag:
    def __init__(self, x, y, color, game):
        self.game = game
        self.color = color
        # Initiale hängende Grafik laden
        self.image = AssetManager.get("items", f"flag{color}Hanging.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        # Maske aus dem Bild (transparente Pixel werden ignoriert)
        self.mask = pygame.mask.from_surface(self.image)

        # Animationszustand
        self.active = False
        self.img_nr = 0
        self.step = 0

    def update(self):
        player = self.game.scene.player

        # Pixelgenaue Kollision: Offset von Spieler- zu Flag-Maske
        offset = (self.rect.x - player.rect.x, self.rect.y - player.rect.y)
        # overlap gibt None oder den ersten überlappenden Pixel zurück
        if player.mask.overlap(self.mask, offset):
            self.active = True

        # Wenn aktiv, dann Animation fortsetzen
        if self.active:
            self.step += 0.15
            if self.step >= 1:
                # Bild wechseln
                if self.img_nr == 0:
                    self.image = AssetManager.get("items", f"flag{self.color}.png")
                    self.img_nr = 1
                else:
                    self.image = AssetManager.get("items", f"flag{self.color}2.png")
                    self.img_nr = 0
                # Maske neu erzeugen, damit Animation auch korrekt kollidiert (falls nötig)
                self.mask = pygame.mask.from_surface(self.image)
                self.step = 0

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))

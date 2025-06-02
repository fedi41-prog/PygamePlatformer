import pygame
from GameV1.scenes.GameScene import GameScene
from GameV1.settings import *
from GameV1.assets.assets import AssetManager

class Game:
    def __init__(self):
        print("Init Game...")

        pygame.init()

        # Bildschirminformationen holen
        display_info = pygame.display.Info()
        self.SCREEN_WIDTH = display_info.current_w
        self.SCREEN_HEIGHT = display_info.current_h

        print(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Vollbild-Fenster
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SCALED)
        pygame.display.set_caption(TITLE)

        # Skalierungsfaktor berechnen, um das virtuelle Bild anzupassen
        self.scale_factor = min(self.SCREEN_WIDTH / VIRTUAL_WIDTH, self.SCREEN_HEIGHT / VIRTUAL_HEIGHT)
        self.scaled_width = int(VIRTUAL_WIDTH * self.scale_factor)
        self.scaled_height = int(VIRTUAL_HEIGHT * self.scale_factor)

        # Virtueller Bildschirm (die "echte" Spielauflösung)
        self.virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

        # Asset-Manager vorbereiten
        for r in RESOURCE_PACKS:
            AssetManager.add_resource_pack(r)

        AssetManager.add_resource_pack("assets/default")

        # Spielsystem vorbereiten
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = GameScene.generate_scene_from_xml(self, "scenes/scene2.xml")

    def run(self):
        while self.running:
            self.scene.handle_events()
            self.scene.update()

            # Spielszene auf den virtuellen Bildschirm zeichnen
            self.scene.draw(self.virtual_screen)

            # Virtuellen Bildschirm skalieren
            scaled_surface = pygame.transform.scale(self.virtual_screen, (self.scaled_width, self.scaled_height))

            # Bildschirm schwarz füllen (für Letterbox-Ränder)
            self.screen.fill((0, 0, 0))

            # Zentriert einfügen
            x = (self.SCREEN_WIDTH - self.scaled_width) // 2
            y = (self.SCREEN_HEIGHT - self.scaled_height) // 2
            self.screen.blit(scaled_surface, (x, y))

            pygame.display.flip()
            self.clock.tick(FPS)

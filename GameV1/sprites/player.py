import pygame
import json
from GameV1.tools.spritesheet import SpriteSheet
from GameV1.tools.collisionhelper import CollisionHelper, CollisionResolver
from GameV1.settings import GRAVITY
from GameV1.assets.assets import AssetManager

class Player:
    def __init__(self, x, y):

        # load image
        self.image_name = "p1_stand"
        self.image = AssetManager.get("p1", self.image_name)

        # create rect
        margin = 6

        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(margin, 0)  # oder dein margin

        # create mask
        # kleinere Hitbox mit Abstand vom Rand
        # Hitbox-Rand verkleinern (z. B. 6px an allen Seiten)


        # Maske mit kleinerem Rechteck erzeugen
        self.mask_image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            self.mask_image,
            (255, 0, 0),
            self.hitbox
        )

        self.mask = pygame.mask.from_surface(self.mask_image)

        # initialize velocity
        self.velocity = pygame.math.Vector2(0, 0)

        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        # Springen
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity.y = -15

        # X-Bewegung
        if keys[pygame.K_LEFT]:
            self.velocity.x = -4
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = 4
        else:
            self.velocity.x = 0

        # Kollisionen
        collision_resolver = CollisionResolver()

        collision_resolver.resolve_vertical(self, platforms, gravity=1)
        collision_resolver.resolve_horizontal(self, platforms)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


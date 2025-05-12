import pygame
from GameV1.assets.assets import AssetManager
from GameV1.settings import GRAVITY
from GameV1.tools.collisionhelper import CollisionResolver

class Player:
    def get_hitbox_rect(self):
        """Gibt den Bereich zurück, den die Hitbox innerhalb des Spielerbildes abdeckt"""
        return pygame.Rect(8, 4, self.hitbox.width, self.hitbox.height)  # z. B. kleiner als das Bild

    def sync_rect(self):
        """Synchronisiert das visuelle rect mit der physikalischen hitbox."""
        self.rect.midbottom = self.hitbox.midbottom

    def update_mask(self, rect=None, shrink=5):
        if rect is None:
            rect = self.hitbox
        hitbox = pygame.Rect(shrink, 0, rect.width - 2 * shrink, rect.height)
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 0, 0), hitbox)
        self.mask = pygame.mask.from_surface(surface)

    def __init__(self, x, y):
        # Bild laden
        self.walkAnimation = [
            "alienGreen_walk01",
            "alienGreen_walk02",
            "alienGreen_walk03",
            "alienGreen_walk04",
            "alienGreen_walk05",
            "alienGreen_walk06",
            "alienGreen_walk07",
            "alienGreen_walk08",
            "alienGreen_walk09",
            "alienGreen_walk10",
            "alienGreen_walk11"
        ]
        self.walkStep = 0
        self.image = AssetManager.get("alienGreen", "alienGreen_stand.png")

        # Gesamtrechteck (für Anzeige)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


        margin = 10
        # Hitbox definieren (kleiner als Bild)
        hitbox_width = self.rect.width - margin*2
        hitbox_height = self.rect.height
        hitbox_x = self.rect.centerx - hitbox_width // 2
        hitbox_y = self.rect.bottom - hitbox_height
        self.hitbox = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

        # Maske basierend auf Hitbox
        self.mask_image = pygame.Surface((hitbox_width, hitbox_height), pygame.SRCALPHA)
        pygame.draw.rect(self.mask_image, (255, 0, 0), (0, 0, hitbox_width, hitbox_height))
        self.mask = pygame.mask.from_surface(self.mask_image)

        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False

        self.direction = "right"

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.velocity.y = -15

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -4
            self.direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = 4
            self.direction = "right"
        else:
            self.velocity.x = 0

        # Kollisionen lösen
        collision_resolver = CollisionResolver()
        collision_resolver.resolve_vertical(self, platforms)
        collision_resolver.resolve_horizontal(self, platforms)

    def draw(self, screen, camera):
        self.update_image()
        screen.blit(self.image, camera.apply(self.rect))
        # Optional: Hitbox zum Debuggen anzeigen
        # pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)
    def update_image(self):
        if not self.on_ground:
            self.image = AssetManager.get("alienGreen", "alienGreen_jump.png")
        elif self.velocity.x != 0:
            self.image = AssetManager.get("alienGreenWalk", self.walkAnimation[int(self.walkStep)])
            self.walkStep += 0.35
            if self.walkStep >= len(self.walkAnimation):
                self.walkStep = 0
        else:
            self.image = AssetManager.get("alienGreen", "alienGreen_stand.png")

        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

import pygame
from GameV1.assets.assets import AssetManager

class MovingBlock:
    def __init__(self, game, x, y, xd, yd, texture, speed=2):
        self.image = AssetManager.get(texture)
        self.mask  = pygame.mask.from_surface(self.image)

        self.game = game

        # Start- und Endposition als Vektoren
        self.pos1 = pygame.Vector2(x, y)
        self.pos2 = pygame.Vector2(xd, yd)
        self.speed = speed

        # Interpolationstimer und Richtung
        self._t   = 0.0
        self._dir = 1
        self._total_dist = (self.pos2 - self.pos1).length() or 1

        # Aktuelle Position in Float zum Lerpen, aber Rect in int
        self._pos = self.pos1.copy()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        player = self.game.scene.player

        # 1) Block-Update wie gehabt (Lerp mit Float)
        old_rect = self.rect.copy()

        delta = (self.speed / self._total_dist) * self._dir
        self._t   += delta
        if   self._t >= 1.0: self._t, self._dir = 1.0, -1
        elif self._t <= 0.0: self._t, self._dir = 0.0,  1

        self._pos = self.pos1.lerp(self.pos2, self._t)
        # 2) Ganzzahliges Rect setzen
        new_x = round(self._pos.x)
        new_y = round(self._pos.y)
        self.rect.topleft = (new_x, new_y)

        # 3) Ganzzahligen Offset ermitteln
        dx = self.rect.x - old_rect.x
        dy = self.rect.y - old_rect.y

        # 4) Spieler mitscrollen mit genau diesem Int‑Offset
        if player and (dx != 0 or dy != 0) and player.on_ground:
            tol = 2
            # nur wenn er wirklich vorher oben auf dem Block stand
            if (abs(player.hitbox.bottom - old_rect.top) <= tol and
                player.hitbox.right > old_rect.left    and
                player.hitbox.left  < old_rect.right):
                player.hitbox.x += dx
                player.hitbox.y += dy
                player.sync_rect()

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))

import pygame

class CollisionResolver:
    def __init__(self, sample_rate=5, max_step_up=4, gravity=0.8, max_fall_speed=10):
        self.sample_rate = sample_rate
        self.max_step_up = max_step_up
        self.gravity = gravity
        self.max_fall_speed = max_fall_speed

    def resolve_vertical(self, player, platforms):
        # Schwerkraft anwenden
        player.velocity.y += self.gravity
        if player.velocity.y > self.max_fall_speed and not player.slam_active:
            player.velocity.y = self.max_fall_speed

        # Vertikale Bewegung
        player.hitbox.y += player.velocity.y
        player.update_mask()
        player.on_ground = False

        for platform in platforms:
            offset = (platform.rect.x - player.hitbox.x,
                      platform.rect.y - player.hitbox.y)
            overlap = player.mask.overlap_mask(platform.mask, offset)
            if overlap.count() > 0:
                w, h = overlap.get_size()
                # Fallendes Szenario (Landung)
                if player.velocity.y >= 0:
                    for dy in range(h):
                        for dx in range(0, w, self.sample_rate):
                            if overlap.get_at((dx, dy)):
                                player.hitbox.bottom = player.hitbox.top + dy
                                player.velocity.y = 0
                                player.on_ground = True
                                player.sync_rect()
                                return
                # Aufprall an Decke (Spieler bewegt sich nach oben)
                elif player.velocity.y < 0:
                    w, h = overlap.get_size()
                    for dy in range(h - 1, -1, -1):  # von unten nach oben
                        for dx in range(0, w, self.sample_rate):
                            if overlap.get_at((dx, dy)):
                                # Position berechnen in Weltkoordinaten
                                collision_y = platform.rect.y + dy
                                player.hitbox.top = collision_y + overlap.get_size()[1] - dy
                                player.velocity.y = 0
                                player.sync_rect()
                                return

        # Falls keine Kollision
        player.sync_rect()

    def resolve_horizontal(self, player, platforms):
        player.hitbox.x += player.velocity.x
        player.update_mask()

        for platform in platforms:
            offset = (platform.rect.x - player.hitbox.x, platform.rect.y - player.hitbox.y)
            overlap = player.mask.overlap_mask(platform.mask, offset)
            if overlap.count() > 0:
                if player.on_ground and self.max_step_up > 0:
                    self._try_step_up(player, platform)
                else:
                    self.x_collision(player, platform)
                break

        player.sync_rect()

    def _try_step_up(self, player, platform):
        original_y = player.hitbox.y
        for step in range(1, self.max_step_up + 1):
            test_hitbox = player.hitbox.copy()
            test_hitbox.y = original_y - step
            # Maske für Testposition
            player.update_mask(test_hitbox)
            offset = (platform.rect.x - test_hitbox.x, platform.rect.y - test_hitbox.y)
            if player.mask.overlap_mask(platform.mask, offset).count() == 0:
                player.hitbox = test_hitbox
                player.update_mask()
                return
        # Rücksetzen, wenn kein Step-Up möglich
        player.hitbox.y = original_y
        self.x_collision(player, platform)

    def x_collision(self, player, platform):
        # Pixelweises Zurückschieben
        player_center = player.hitbox.centerx
        direction = 1 if player_center < platform.rect.centerx else -1
        while True:
            offset = (platform.rect.x - player.hitbox.x,
                      platform.rect.y - player.hitbox.y)
            if player.mask.overlap_mask(platform.mask, offset).count() == 0:
                break
            player.hitbox.x -= direction
        player.velocity.x = 0
        player.update_mask()


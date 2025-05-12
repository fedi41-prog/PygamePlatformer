import pygame

class CollisionResolver:
    def __init__(self, sample_rate=2, max_step_up=4, gravity=0.8, max_fall_speed=10):
        self.sample_rate = sample_rate
        self.max_step_up = max_step_up
        self.gravity = gravity
        self.max_fall_speed = max_fall_speed

    def resolve_vertical(self, player, platforms):
        # Anwenden von Schwerkraft
        player.velocity.y += self.gravity
        if player.velocity.y > self.max_fall_speed:
            player.velocity.y = self.max_fall_speed

        # Vertikale Bewegung
        player.hitbox.y += player.velocity.y
        player.update_mask()
        player.on_ground = False

        # Kollisionserkennung und Korrektur
        for platform in platforms:
            offset = (platform.rect.x - player.hitbox.x, platform.rect.y - player.hitbox.y)
            overlap = player.mask.overlap_mask(platform.mask, offset)
            if overlap.count() > 0 and player.velocity.y >= 0:
                # Pixelgenau Landung auf Plattformkante
                w, h = overlap.get_size()
                for dy in range(h):
                    for dx in range(0, w, self.sample_rate):
                        if overlap.get_at((dx, dy)):
                            player.hitbox.bottom = player.hitbox.top + dy
                            player.velocity.y = 0
                            player.on_ground = True
                            player.sync_rect()
                            return
        # Rect synchronisieren
        player.sync_rect()

    def resolve_horizontal(self, player, platforms):
        # Horizontale Bewegung
        player.hitbox.x += player.velocity.x
        player.update_mask()

        for platform in platforms:
            offset = (platform.rect.x - player.hitbox.x, platform.rect.y - player.hitbox.y)
            overlap = player.mask.overlap_mask(platform.mask, offset)
            if overlap.count() > 0:
                # Step-Up-Versuch nur bei Bodenkontakt
                if player.on_ground and self.max_step_up > 0:
                    stepped = False
                    original_y = player.hitbox.y
                    for step in range(1, self.max_step_up + 1):
                        test_hitbox = player.hitbox.copy()
                        test_hitbox.y = original_y - step
                        player.update_mask(test_hitbox)
                        test_offset = (platform.rect.x - test_hitbox.x, platform.rect.y - test_hitbox.y)
                        test_overlap = player.mask.overlap_mask(platform.mask, test_offset)
                        if test_overlap.count() == 0:
                            player.hitbox = test_hitbox
                            stepped = True
                            break
                    if not stepped:
                        player.hitbox.y = original_y
                        self.x_collision(player, platform)
                else:
                    self.x_collision(player, platform)
                break

        # Nach Kollision Rect synchronisieren
        player.sync_rect()

    def x_collision(self, player, platform):
        # Pixelweise Rückschieben, bis keine Überlappung mehr besteht
        original_x = player.hitbox.x
        player_center = player.hitbox.centerx
        direction = 1 if player_center < platform.rect.centerx else -1

        # Wiederhole bis gesamter Überlapp gelöst ist
        while True:
            offset = (platform.rect.x - player.hitbox.x, platform.rect.y - player.hitbox.y)
            overlap = player.mask.overlap_mask(platform.mask, offset)
            if overlap.count() == 0:
                break
            player.hitbox.x -= direction

        # Reset Geschwindigkeit
        player.velocity.x = 0
        player.update_mask()


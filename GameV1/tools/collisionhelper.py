import pygame

class CollisionHelper:
    def __init__(self, sample_rate=2, tolerance=3):
        """
        :param sample_rate: Schrittweite für Rand-Scan bei Richtungserkennung
        :param tolerance: Toleranz in Pixeln für Kollisionen
        """
        self.sample_rate = sample_rate
        self.tolerance = tolerance

    def detect_direction(self, player, platform):
        """Gibt eine Liste zurück mit den Richtungen der Kollision (z. B. ['top', 'left'])"""
        offset = (platform.rect.x - player.rect.x, platform.rect.y - player.rect.y)
        overlap = player.mask.overlap_mask(platform.mask, offset)

        if overlap.count() == 0:
            return []

        directions = set()
        ow, oh = overlap.get_size()

        # horizontal (top / bottom)
        for x in range(0, ow, self.sample_rate):
            if overlap.get_at((x, 0)):
                directions.add("top")
            if overlap.get_at((x, oh - 1)):
                directions.add("bottom")

        # vertikal (left / right)
        for y in range(0, oh, self.sample_rate):
            if overlap.get_at((0, y)):
                directions.add("left")
            if overlap.get_at((ow - 1, y)):
                directions.add("right")

        return list(directions)

    def resolve_sloped_collision(self, player, platform, velocity):
        offset = (platform.rect.x - player.rect.x, platform.rect.y - player.rect.y)
        overlap = player.mask.overlap_mask(platform.mask, offset)

        if overlap.count() == 0:
            return



        # Wir scannen die Overlap-Maske nur, wenn der Spieler nach unten fällt
        if velocity.y >= 0:
            # Suche die tiefste sichtbare Y-Kollision innerhalb der Overlap-Maske
            for dy in range(overlap.get_size()[1]):
                for dx in range(0, overlap.get_size()[0], self.sample_rate):
                    if overlap.get_at((dx, dy)):
                        # Kollisionspunkt in Welt-Koordinaten
                        player.rect.bottom = player.rect.top + dy
                        velocity.y = 0
                        player.on_ground = True
                        return

    def resolve_horizontal_collision(self, player, platform, velocity):
        offset = (platform.rect.x - player.rect.x, platform.rect.y - player.rect.y)
        overlap = player.mask.overlap_mask(platform.mask, offset)

        if overlap.count() == 0:
            return

        # Nur prüfen, wenn Spieler sich horizontal bewegt
        if velocity.x != 0:
            width, height = overlap.get_size()

            # Wir scannen von links nach rechts oder umgekehrt, je nach Bewegungsrichtung
            scan_range = range(width) if velocity.x > 0 else range(width - 1, -1, -1)

            for dx in scan_range:
                for dy in range(0, height, self.sample_rate):
                    if overlap.get_at((dx, dy)):
                        # Wir haben einen Kollisionspunkt gefunden
                        world_x = player.rect.left + dx

                        if velocity.x > 0:
                            # Spieler kam von links → rechter Rand blockiert
                            player.rect.right = world_x
                        else:
                            # Spieler kam von rechts → linker Rand blockiert
                            player.rect.left = world_x

                        velocity.x = 0
                        return


import pygame

class CollisionResolver:
    def __init__(self, sample_rate=2):
        self.sample_rate = sample_rate

    def resolve_vertical(self, player, platforms, gravity):
        player.velocity.y += gravity
        if player.velocity.y > 10:
            player.velocity.y = 10

        player.hitbox.y += player.velocity.y
        player.on_ground = False

        for platform in platforms:
            offset = (platform.rect.x - player.hitbox.x, platform.rect.y - player.hitbox.y)
            overlap = player.mask.overlap_mask(platform.mask, offset)

            if overlap.count() > 0 and player.velocity.y >= 0:
                for dy in range(overlap.get_size()[1]):
                    for dx in range(0, overlap.get_size()[0], self.sample_rate):
                        if overlap.get_at((dx, dy)):
                            player.hitbox.bottom = player.hitbox.top + dy
                            player.velocity.y = 0
                            player.on_ground = True
                            player.rect.centerx = player.hitbox.centerx
                            player.rect.bottom = player.hitbox.bottom
                            return

        player.rect.centerx = player.hitbox.centerx
        player.rect.centery = player.hitbox.centery

    def resolve_horizontal(self, player, platforms):
        player.hitbox.x += player.velocity.x

        for platform in platforms:
            offset = (platform.rect.x - player.hitbox.x, platform.rect.y - player.hitbox.y)
            overlap = player.mask.overlap_mask(platform.mask, offset)

            if overlap.count() > 0:
                width, height = overlap.get_size()
                scan_range = range(width) if player.velocity.x > 0 else range(width - 1, -1, -1)

                for dx in scan_range:
                    for dy in range(0, height, self.sample_rate):
                        if overlap.get_at((dx, dy)):
                            world_x = player.hitbox.left + dx
                            if player.velocity.x > 0:
                                player.hitbox.right = world_x
                            else:
                                player.hitbox.left = world_x
                            player.velocity.x = 0
                            player.rect.centerx = player.hitbox.centerx
                            player.rect.centery = player.hitbox.centery
                            return

        player.rect.centerx = player.hitbox.centerx
        player.rect.centery = player.hitbox.centery

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
        """
        Justiert die Position des Spielers pixelgenau auf die Plattform – funktioniert auch bei schrägen Masken.
        Setzt den Spieler auf die höchste gültige Y-Kollision (von unten betrachtet).
        """
        offset = (platform.rect.x - player.rect.x, platform.rect.y - player.rect.y)
        overlap = player.mask.overlap_mask(platform.mask, offset)

        if overlap.count() == 0:
            return

        ow, oh = overlap.get_size()
        contact_points = []

        for y in range(oh):
            for x in range(ow):
                if overlap.get_at((x, y)):
                    contact_points.append((x, y))

        if not contact_points:
            return

        # Untersten Kollisionspunkt im Overlap suchen
        deepest_y = max(pt[1] for pt in contact_points)

        # Korrektur der y-Position des Spielers
        correction = deepest_y - oh + 1
        player.rect.y += correction
        velocity.y = 0
        player.on_ground = True

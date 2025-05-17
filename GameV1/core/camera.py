import pygame

class Camera:
    def __init__(self, screen_width, screen_height, level_width, level_height, smoothing=0.1):
        self.screen_w = screen_width
        self.screen_h = screen_height
        self.level_w = level_width
        self.level_h = level_height
        self.offset = pygame.Vector2(0, 0)
        self.target_offset = pygame.Vector2(0, 0)
        self.smoothing = smoothing  # Wie schnell die Kamera dem Ziel folgt (zwischen 0.01 und 1.0)

    def update(self, target_rect):
        # Ziel-Offset berechnen (Kamera-Zielposition)
        target_x = target_rect.centerx - self.screen_w // 2
        target_y = target_rect.centery - self.screen_h // 2

        # Clampen (nicht aus dem Level scrollen)
        target_x = max(0, min(target_x, self.level_w - self.screen_w))
        target_y = max(0, min(target_y, self.level_h - self.screen_h))

        self.target_offset.update(target_x, target_y)

        # Sanftes Nachziehen per Interpolation
        self.offset += (self.target_offset - self.offset) * self.smoothing

    def apply(self, rect):
        # Verschiebe ein beliebiges Rect um die Kamera-Offset
        return rect.move(-int(self.offset.x), -int(self.offset.y))


import pygame

class Camera:
    def __init__(self, screen_width, screen_height, level_width, level_height):
        self.screen_w = screen_width
        self.screen_h = screen_height
        self.level_w = level_width
        self.level_h = level_height
        self.offset = pygame.Vector2(0, 0)

    def update(self, target_rect):
        # Ziel in Bildschirmmitte halten:
        x = target_rect.centerx - self.screen_w // 2
        y = target_rect.centery - self.screen_h // 2

        # Nicht über Level-Ränder hinaus scrollen:
        x = max(0, min(x, self.level_w - self.screen_w))
        y = max(0, min(y, self.level_h - self.screen_h))

        self.offset.x = x
        self.offset.y = y

    def apply(self, rect):
        # Verschiebe ein beliebiges Rect um die Kamera-Offset
        return rect.move(-self.offset.x, -self.offset.y)

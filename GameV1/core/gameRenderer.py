import pygame


class GameRenderer:
    def __init__(self, camera_offset=(0, 0)):
        """
        :param camera_offset: Tupel (x, y), das von allen Positionen abgezogen wird
        """
        self.camera_offset = pygame.Vector2(camera_offset)

    def set_camera_offset(self, offset):
        """Setzt den Kamera-Offset (z. B. zum Scrollen der Welt)"""
        self.camera_offset = pygame.Vector2(offset)

    def render(self, surface, sprite_groups):
        """
        Rendert alle Sprites aus den gegebenen Sprite-Gruppen auf das Surface.

        :param surface: Das Ziel-Surface
        :param sprite_groups: Eine oder mehrere pygame.sprite.Group-Objekte (Liste oder einzelnes Objekt)
        """
        if not isinstance(sprite_groups, (list, tuple)):
            sprite_groups = [sprite_groups]

        for group in sprite_groups:
            for sprite in group:
                if hasattr(sprite, 'image') and hasattr(sprite, 'rect'):
                    draw_pos = sprite.rect.topleft - self.camera_offset
                    surface.blit(sprite.image, draw_pos)

    def render_images(self, surface, image_data_list):
        """
        Rendert Bilder, die als (image, (x, y))-Tupel gegeben sind.

        :param surface: Das Ziel-Surface
        :param image_data_list: Liste von (image, (x, y)) Tupeln
        """
        for image, pos in image_data_list:
            draw_pos = pygame.Vector2(pos) - self.camera_offset
            surface.blit(image, draw_pos)

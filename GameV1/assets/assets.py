import os
import pygame

class AssetManager:
    _texture_packs = []  # Liste von dicts: [{"imgname": Surface}, {...}]
    _fonts = {}          # z.B. {"pack1/fontname": {size: Font, ...}}

    @classmethod
    def add_texture_pack(cls, folder_path, default_font_sizes=None):
        """
        Fügt ein neues Texture-Pack hinzu. Lädt alle PNGs und Fonts im Ordner sofort.
        `default_font_sizes` ist ein dict: {"rel/path/fontname": [12, 24, 32]}
        """
        texture_pack = {}
        font_pack = {}

        if default_font_sizes is None:
            default_font_sizes = {}

        for root, _, files in os.walk(folder_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, folder_path).replace("\\", "/")
                key = os.path.splitext(rel_path)[0]  # ohne Endung

                if filename.endswith(".png"):
                    texture_pack[key] = pygame.image.load(full_path).convert_alpha()

                elif filename.endswith(".ttf") or filename.endswith(".otf"):
                    sizes = default_font_sizes.get(key, [24])
                    font_pack[key] = {}
                    for size in sizes:
                        font_pack[key][size] = pygame.font.Font(full_path, size)

        cls._texture_packs.append(texture_pack)
        cls._fonts.update(font_pack)

    @classmethod
    def get(cls, image_name):
        """Sucht ein Bild in allen Texture-Packs in Reihenfolge."""
        for pack in cls._texture_packs:
            if image_name in pack:
                return pack[image_name]
        # Bild nicht gefunden
        raise FileNotFoundError(f"Image '{image_name}' not found in any texture pack.")

    @classmethod
    def get_font(cls, font_name, size=24):
        """Gibt eine Font in gegebener Größe zurück, wenn vorhanden."""
        fonts = cls._fonts.get(font_name)
        if fonts:
            return fonts.get(size)
        # Bild nicht gefunden
        raise FileNotFoundError(f"Image '{font_name}' not found in any texture pack.")

    @classmethod
    def clear(cls):
        cls._texture_packs.clear()
        cls._fonts.clear()

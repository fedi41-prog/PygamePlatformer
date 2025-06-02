import os
import pygame

class AssetManager:
    _texture_packs = []  # Liste von dicts: {"imgname": Surface, "fonts/fontname_size": Font, ...}
    _fonts = {}  # Optional: flache Font-Tabelle, z. B. fuer direkte Abfrage

    @classmethod
    def add_texture_pack(cls, folder_path, font_sizes=None):
        """
        Fügt ein neues Texture-Pack hinzu. Lädt alle PNG-Bilder und Fonts (.ttf/.otf) aus dem Ordner.
        Optional: font_sizes = {"Fontname": [16, 24, 32], ...}
        """
        texture_pack = {}
        font_sizes = font_sizes or {}

        for root, _, files in os.walk(folder_path):
            for filename in files:
                path = os.path.join(root, filename)
                rel_path = os.path.relpath(path, folder_path).replace("\\", "/")
                name, ext = os.path.splitext(rel_path)

                if ext.lower() == ".png":
                    texture_pack[name] = pygame.image.load(path).convert_alpha()

                elif ext.lower() in [".ttf", ".otf"]:
                    font_base = os.path.splitext(os.path.basename(name))[0]
                    sizes = font_sizes.get(font_base, [24])  # Standardgröße
                    for size in sizes:
                        key = f"fonts/{font_base}_{size}"
                        font = pygame.font.Font(path, size)
                        texture_pack[key] = font
                        cls._fonts[key] = font  # Optional in zentrale Map

        cls._texture_packs.append(texture_pack)

    @classmethod
    def get(cls, asset_name):
        """Sucht Bild oder Font in allen Texture-Packs."""
        for pack in cls._texture_packs:
            if asset_name in pack:
                return pack[asset_name]
        raise FileNotFoundError(f"Asset '{asset_name}' not found in any texture pack.")

    @classmethod
    def get_font(cls, name, size):
        """Holt Font mit Format: get_font("Fontname", 24)"""
        key = f"fonts/{name}_{size}"
        return cls.get(key)

    @classmethod
    def clear(cls):
        cls._texture_packs.clear()
        cls._fonts.clear()

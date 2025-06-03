import os
import pygame
import json

class AssetManager:
    _resource_packs = []  # Liste von dicts: {"imgname": Surface, "fonts/fontname_size": Font, ...}
    _fonts = {}  # Optional: flache Font-Tabelle, z. B. fuer direkte Abfrage

    @classmethod
    def add_resource_pack(cls, folder_path, scale_faktor):
        """
        Fügt ein neues Texture-Pack hinzu. Lädt alle PNG-Bilder und Fonts (.ttf/.otf) aus dem Ordner.
        Optional: font_sizes = {"Fontname": [16, 24, 32], ...}
        """
        resource_pack = {}

        with open(folder_path + "/settings.json", "r") as f:
            settings = json.load(f)
            font_sizes = settings["font-sizes"]
            this_scale_faktor = settings["scale"]

        scale_faktor /= this_scale_faktor

        for root, _, files in os.walk(folder_path):
            for filename in files:
                path = os.path.join(root, filename)
                rel_path = os.path.relpath(path, folder_path).replace("\\", "/")
                name, ext = os.path.splitext(rel_path)

                if ext.lower() == ".png":
                    resource_pack[name] = pygame.transform.scale_by(pygame.image.load(path).convert_alpha(), (scale_faktor, scale_faktor))

                elif ext.lower() in [".ttf", ".otf"]:
                    font_base = os.path.splitext(os.path.basename(name))[0]
                    sizes = font_sizes.get(font_base, [24])  # Standardgröße
                    for size in sizes:
                        key = f"fonts/{font_base}_{size}"
                        font = pygame.font.Font(path, size)
                        resource_pack[key] = font
                        cls._fonts[key] = font  # Optional in zentrale Map

        cls._resource_packs.append(resource_pack)

    @classmethod
    def get(cls, asset_name):
        """Sucht Bild oder Font in allen Texture-Packs."""
        for pack in cls._resource_packs:
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
        cls._resource_packs.clear()
        cls._fonts.clear()

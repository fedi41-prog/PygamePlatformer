import os
import pygame
import json

class AssetManager:
    _resource_packs = []  # Liste von dicts: {"imgname": Surface, "fonts/fontname_size": Font, ...}
    _fonts = {}
    _global_scale = 1  # Globale Skalierung, wird durch das erste Pack mit "scale" gesetzt
    _on_scale_change_callback = None  # Optional: Callback für Skalierungsänderungen

    @classmethod
    def set_scale_change_callback(cls, callback):
        cls._on_scale_change_callback = callback

    @classmethod
    def add_resource_pack(cls, folder_path):
        """
        Fügt ein neues Texture-Pack hinzu. Lädt PNG-Bilder und Fonts (.ttf/.otf) aus dem Ordner.
        Erwartet eine settings.json mit "font-sizes" und optional "scale".
        """
        texture_pack = {}

        settings_path = os.path.join(folder_path, "settings.json")
        font_sizes = {}
        scale = 1

        if os.path.exists(settings_path):
            with open(settings_path, "r") as f:
                settings = json.load(f)
                font_sizes = settings.get("font-sizes", {})
                scale = settings.get("scale", 1)

        # Falls noch keine globale Skalierung gesetzt wurde, übernehmen
        if cls._global_scale == 1:
            cls._global_scale = scale
        elif scale != cls._global_scale:
            cls._global_scale = scale
            if cls._on_scale_change_callback:
                cls._on_scale_change_callback(scale)

        for root, _, files in os.walk(folder_path):
            for filename in files:
                path = os.path.join(root, filename)
                rel_path = os.path.relpath(path, folder_path).replace("\\", "/")
                name, ext = os.path.splitext(rel_path)

                if ext.lower() == ".png":
                    image = pygame.image.load(path).convert_alpha()
                    if scale != 1:
                        new_size = (round(image.get_width() * scale), round(image.get_height() * scale))
                        image = pygame.transform.scale(image, new_size)
                    texture_pack[name] = image

                elif ext.lower() in [".ttf", ".otf"]:
                    font_base = os.path.splitext(os.path.basename(name))[0]
                    sizes = font_sizes.get(font_base, [24])
                    for size in sizes:
                        scaled_size = round(size * scale)
                        key = f"fonts/{font_base}_{size}"
                        font = pygame.font.Font(path, scaled_size)
                        texture_pack[key] = font
                        cls._fonts[key] = font

        cls._resource_packs.append(texture_pack)

    @classmethod
    def get(cls, asset_name):
        for pack in cls._resource_packs:
            if asset_name in pack:
                return pack[asset_name]
        raise FileNotFoundError(f"Asset '{asset_name}' not found in any texture pack.")

    @classmethod
    def get_font(cls, name, size):
        key = f"fonts/{name}_{size}"
        return cls.get(key)

    @classmethod
    def get_scale(cls):
        return cls._global_scale

    @classmethod
    def clear(cls):
        cls._resource_packs.clear()
        cls._fonts.clear()
        cls._global_scale = 1
        cls._on_scale_change_callback = None


import pygame
import xml.etree.ElementTree as ET
from GameV1.tools.spritesheet import SpriteSheet
import os

class AssetManager:
    _sheets = {}     # z.B. {"player": {name: Surface, ...}, "items": {...}}
    _fonts = {}      # z.B. {"default": FontObject, "title": FontObject, ...}

    @classmethod
    def load_sheet(cls, key, image_path, xml_path):
        if key in cls._sheets:
            return cls._sheets[key]  # Schon geladen

        ss = SpriteSheet(image_path)
        sprite_dict = ss.load_from_xml(xml_path)

        cls._sheets[key] = sprite_dict
        return sprite_dict

    @classmethod
    def get(cls, sheet_key, sprite_name):
        sheet = cls._sheets.get(sheet_key, {})
        return sheet.get(sprite_name)

    @classmethod
    def getSheet(cls, sheet_key):
        return cls._sheets.get(sheet_key, {})

    @classmethod
    def load_all_sheets_from_folder(cls, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".png"):
                base = os.path.splitext(filename)[0]
                image_path = os.path.join(folder_path, base + ".png")
                xml_path = os.path.join(folder_path, base + ".xml")
                if os.path.exists(xml_path):
                    cls.load_sheet(base, image_path, xml_path)

    # ---------------------- FONT MANAGEMENT ----------------------
    @classmethod
    def load_font(cls, name, path, size):
        if name not in cls._fonts:
            cls._fonts[name] = pygame.font.Font(path, size)
        return cls._fonts[name]

    @classmethod
    def get_font(cls, name):
        return cls._fonts.get(name)

    @classmethod
    def load_fonts_from_folder(cls, folder_path, default_sizes):
        for filename in os.listdir(folder_path):
            if filename.endswith(".ttf") or filename.endswith(".otf"):
                base = os.path.splitext(filename)[0]
                path = os.path.join(folder_path, filename)
                size = default_sizes.get(base, 24)  # Standardgröße: 24
                cls.load_font(base, path, size)
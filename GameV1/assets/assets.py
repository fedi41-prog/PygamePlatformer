import pygame
import xml.etree.ElementTree as ET
from GameV1.tools.spritesheet import SpriteSheet
import os

class AssetManager:
    _sheets = {}     # z.B. {"player": {name: Surface, ...}, "items": {...}}

    @classmethod
    def load_sheet(cls, key, image_path, xml_path, colorkey=None):
        if key in cls._sheets:
            return cls._sheets[key]  # Schon geladen

        ss = SpriteSheet(image_path)
        sprite_dict = ss.load_from_xml(xml_path, colorkey)

        cls._sheets[key] = sprite_dict
        return sprite_dict

    @classmethod
    def get(cls, sheet_key, sprite_name):
        sheet = cls._sheets.get(sheet_key, {})
        return sheet.get(sprite_name)

    @classmethod
    def load_all_sheets_from_folder(cls, folder_path, colorkey=None):
        for filename in os.listdir(folder_path):
            if filename.endswith(".png"):
                base = os.path.splitext(filename)[0]
                image_path = os.path.join(folder_path, base + ".png")
                xml_path = os.path.join(folder_path, base + ".xml")
                if os.path.exists(xml_path):
                    cls.load_sheet(base, image_path, xml_path, colorkey)

import pygame
import json
import os

class AssetsManager:
    # ---- Klassendaten / Shared State ----
    assets_root        = "assets"
    pack_order         = []      # Reihenfolge, in der Packs registriert wurden
    pack_scales        = {}      # z.B. { "hd": 2, "default": 1, ... }
    pack_font_settings = {}      # z.B. { "hd": { "fonts/OpenSans.ttf": [16, 24, 32], ... }, ... }
    max_scale          = 1       # größter gefundener Skalierungsfaktor
    textures           = {}      # { "relativer/pfad.png": pygame.Surface }
    fonts              = {}      # { (relativer/pfad.ttf, base_size): pygame.font.Font }

    @classmethod
    def set_assets_root(cls, path):
        """
        Legt den Basisordner fest, in dem alle Texture-Packs liegen.
        Standard ist "assets".
        """
        cls.assets_root = path

    @classmethod
    def load_resource_pack(cls, pack_name):
        """
        Registriert ein Texture-Pack (Ordner unter assets_root) und liest dessen "settings.json" aus,
        um den darin definierten "scale"-Wert und die Font-Definitionen (Liste von Größen) zu speichern.
        Fügt das Pack in die Liste pack_order ein.

        Erwartetes Format in settings.json:
        {
          "scale": 1.5,
          "fonts": {
            "fonts/OpenSans-Regular.ttf": [16, 24, 32],
            "fonts/TitleFont.ttf": [48, 64]
          }
        }
        """
        if pack_name in cls.pack_order:
            return  # Pack wurde bereits registriert

        settings_path = os.path.join(cls.assets_root, pack_name, "settings.json")
        scale_val = 1
        font_defs = {}  # { "pfad/zur/font.ttf": [größenliste], ... }

        if os.path.isfile(settings_path):
            try:
                with open(settings_path, "r") as f:
                    s = json.load(f)
                # Lese Scale-Wert
                if "scale" in s and isinstance(s["scale"], (int, float)):
                    scale_val = s["scale"]
                # Lese Font-Definitionen, falls vorhanden
                # Erwarte: "fonts": { "fonts/OpenSans.ttf": [16, 24, 32], ... }
                if "fonts" in s and isinstance(s["fonts"], dict):
                    for font_rel_path, sizes in s["fonts"].items():
                        if isinstance(font_rel_path, str) and isinstance(sizes, list):
                            # Filtere nur int-Werte in der Liste
                            valid_sizes = [int(sz) for sz in sizes if isinstance(sz, (int, float)) and int(sz) > 0]
                            if valid_sizes:
                                font_defs[font_rel_path] = valid_sizes
            except Exception:
                scale_val = 1
                font_defs = {}

        cls.pack_order.append(pack_name)
        cls.pack_scales[pack_name] = scale_val
        cls.pack_font_settings[pack_name] = font_defs

    @classmethod
    def finalize_packs(cls):
        """
        Nachdem alle Packs per load_resource_pack(...) registriert sind, wird hier
        der maximale Scale-Faktor aller registrierten Packs berechnet.
        """
        if cls.pack_scales:
            cls.max_scale = max(cls.pack_scales.values())
        else:
            cls.max_scale = 1

    @classmethod
    def load_textures(cls):
        """
        Lädt alle .png-Dateien aus den registrierten Packs (in der Reihenfolge pack_order).
        Für jede Datei:
          1. Wird sie aus dem ersten Pack geladen, in dem sie existiert.
          2. Liegt der Pack-spezifische scale < max_scale? Dann skaliere mit (max_scale / scale_pack).
          3. Speichere das Ergebnis in textures[relativer_pfad].

        Anschließend lädt es alle Fonts, wie in pack_font_settings definiert:
          - Für jeden relativen Font-Pfad und jede Basisgröße:
            * Lade die erste gefundene Font-Datei.
            * Skaliere die Punktgröße: scaled_size = int(base_size * (max_scale / pack_scale)).
            * Speichere in fonts[(rel_path, base_size)].
        """
        cls.textures.clear()
        cls.fonts.clear()

        # 1) Texturen laden und skalieren
        for pack_name in cls.pack_order:
            pack_dir   = os.path.join(cls.assets_root, pack_name)
            pack_scale = cls.pack_scales.get(pack_name, 1)

            for root, _, files in os.walk(pack_dir):
                for fname in files:
                    if not fname.lower().endswith(".png"):
                        continue

                    full_path = os.path.join(root, fname)
                    rel_path  = os.path.relpath(full_path, pack_dir).replace("\\", "/")

                    if rel_path in cls.textures:
                        continue

                    try:
                        img = pygame.image.load(full_path).convert_alpha()
                    except Exception as e:
                        raise RuntimeError(f"Fehler beim Laden von '{full_path}': {e}")

                    factor = float(cls.max_scale) / float(pack_scale)
                    if factor != 1:
                        w, h = img.get_size()
                        new_size = (int(w * factor), int(h * factor))
                        img = pygame.transform.scale(img, new_size)

                    cls.textures[rel_path] = img

        # 2) Fonts laden und skalieren
        for pack_name in cls.pack_order:
            pack_dir   = os.path.join(cls.assets_root, pack_name)
            pack_scale = cls.pack_scales.get(pack_name, 1)
            font_defs  = cls.pack_font_settings.get(pack_name, {})

            for rel_font_path, base_sizes in font_defs.items():
                full_font_path = os.path.join(pack_dir, rel_font_path)
                if not os.path.isfile(full_font_path):
                    continue  # Datei im aktuellen Pack nicht vorhanden

                for base_size in base_sizes:
                    key = (rel_font_path, base_size)
                    if key in cls.fonts:
                        continue  # bereits geladen

                    scaled_size = int(base_size * (cls.max_scale / pack_scale))
                    if scaled_size < 1:
                        scaled_size = 1

                    try:
                        font = pygame.font.Font(full_font_path, scaled_size)
                    except Exception as e:
                        raise RuntimeError(f"Fehler beim Laden der Font '{full_font_path}' mit Basisgröße {base_size}: {e}")

                    cls.fonts[key] = font

    @classmethod
    def get(cls, rel_path):
        """
        Gibt die bereits geladene pygame.Surface zurück.

        :param rel_path: Relativer Pfad innerhalb eines Packs, z.B. "player.png" oder "tiles/grass.png".
        :return: pygame.Surface (bereits skaliert auf max_scale)
        :raises KeyError: Wenn die Textur nicht gefunden wurde.
        """
        if rel_path not in cls.textures:
            raise KeyError(f"Texture '{rel_path}' wurde nicht gefunden. Hast du load_textures() aufgerufen?")
        return cls.textures[rel_path]

    @classmethod
    def get_font(cls, rel_font_path, base_size):
        """
        Gibt die bereits geladene pygame.font.Font zurück.

        :param rel_font_path: Relativer Pfad zur Font, z.B. "fonts/OpenSans-Regular.ttf".
        :param base_size: Die Basis-Punktgröße, wie sie in settings.json angegeben wurde.
        :return: pygame.font.Font (mit skaliertem Punktwert)
        :raises KeyError: Wenn die Font nicht gefunden wurde.
        """
        key = (rel_font_path, base_size)
        if key not in cls.fonts:
            raise KeyError(f"Font '{rel_font_path}' mit Basisgröße {base_size} nicht gefunden. Hast du load_textures() aufgerufen?")
        return cls.fonts[key]

    @classmethod
    def clear_cache(cls):
        """
        Löscht alle geladenen Texturen, Fonts und Pack-Registrierungen.
        Setzt max_scale auf 1 zurück.
        """
        cls.pack_order.clear()
        cls.pack_scales.clear()
        cls.pack_font_settings.clear()
        cls.max_scale = 1
        cls.textures.clear()
        cls.fonts.clear()

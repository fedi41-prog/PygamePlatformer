import cx_Freeze
import os
import sys

# Optional: Pfad zur Ressourcensammlung (Texte, Bilder, Sounds etc.)
include_files = [     # Ordner mit Bildern, Sounds etc.
    "GameV1"    # Dein Spielcode
]

# Hauptskript definieren
executables = [
    cx_Freeze.Executable("GameV1/__init__.py", base=None, target_name="PlatformerGame.exe")
]

# Build-Setup
cx_Freeze.setup(
    name="Pygame Platformer",
    version="1.0",
    description="Ein Platformer mit Pygame",
    options={
        "build_exe": {
            "packages": ["pygame", "os", "sys"],
            "include_files": include_files,
            "excludes": ["tkinter"],  # Falls nicht genutzt
            "build_exe": "buildd",     # Vermeidet Duplikation im Build-Verzeichnis
        }
    },
    executables=executables
)

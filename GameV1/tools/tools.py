import sys
import os

def any_true(items, tests: int | list):
    if tests.__class__ == list:
        for t in tests:
            if items[t]:
                return True
    else:
        if items[tests]:
            return True
    return False

def resource_path(relative_path):
    """Gibt den absoluten Pfad zur Ressource zurück – funktioniert auch bei Build mit cx_Freeze."""
    if hasattr(sys, '_MEIPASS'):  # cx_Freeze oder PyInstaller verwenden diesen Attributnamen
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path).replace("\\", "/")



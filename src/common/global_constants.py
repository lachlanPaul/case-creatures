"""
    Global constants for quick and easy access
"""
import os

# Colours
COLOUR_WHITE = (255, 255, 255)
COLOUR_BLACK = (0, 0, 0)
COLOUR_GREY = (194, 196, 196)
COLOUR_RED = (255, 0, 0)  # Mostly used for debugging collision

COLOUR_PAUSE_MENU = (3, 50, 112)

# File Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JETBRAINS_MONO = os.path.join(ROOT_DIR, "assets", "fonts", "JetBrainsMono-Regular.ttf")

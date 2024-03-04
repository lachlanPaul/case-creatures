"""Title Screen"""

from src.button import Button


def title_screen(screen):
    button = Button(50, 50, 50, 50, "Start")
    button.draw(screen)

"""Title Screen"""

from src.common.button import Button


def title_screen(screen):
    on_title_screen = True

    while on_title_screen:
        button = Button(50, 50, 50, 50, "Start")
        button.draw(screen)

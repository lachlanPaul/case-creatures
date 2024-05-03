"""
    Button clickable using the keys

    Lachlan Paul, 2024
"""

import pygame

from src.common.global_constants import JETBRAINS_MONO, COLOUR_BLACK


class Button:
    def __init__(self, x_y: tuple, width_height: tuple, text, colour, colour_when_selected, font: pygame.font.Font = False):
        pygame.font.init()

        self.rect = pygame.Rect(x_y, width_height)
        self.text = text
        self.colour = colour
        self.colour_when_selected = colour_when_selected
        self.is_selected = False

        if type(font) is pygame.font.Font:
            self.font = font
        else:
            self.font = pygame.font.SysFont(JETBRAINS_MONO, 60)  # Default font

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour_when_selected if self.is_selected else self.colour, self.rect)
        text_surface = self.font.render(self.text, True, COLOUR_BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def set_selected(self):
        """Changes the colour of the button. To be called when the button is selected"""
        self.is_selected = not self.is_selected  # Reverses the bool

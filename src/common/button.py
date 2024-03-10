"""
    Button clickable using the mouse
    TODO: Make buttons selectable using the movement keys

    Lachlan Paul, 2024
"""

import pygame


class Button:
    def __init__(self, x, y, width, height, text, font: pygame.font.Font = False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

        if font:
            self.font = font
        else:
            self.font = pygame.font.Font(None, 36)  # Default font

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0,))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return self.rect.collidepoint(event.pos)

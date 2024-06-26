"""
    Text box used by intractable objects and people
"""

import pygame

from src.common.global_constants import JETBRAINS_MONO, COLOUR_GREY, COLOUR_BLACK


class TextBox:
    def __init__(self, text, name=None):
        pygame.font.init()

        self.text = text
        self.name = name
        self.font = pygame.font.Font(JETBRAINS_MONO, 40)

        self.all_text_sections = [self.text[i:i + 30] for i in range(0, len(self.text), 30)]
        self.current_section = 0

        self.text_box = pygame.rect.Rect(0, 400, 800, 200)
        self.name_box = pygame.rect.Rect(0, 350, 200, 200)

        # A technique I borrowed from FTC.
        # Changing a variable to True or False based on whether the button has been pressed
        # prevents it being registered too many times.
        self.e_key_released = True

        if self.name is not None and len(self.name) > 7:
            raise ("A text box name is too long", ValueError)

    def interact(self, screen, keys):
        try:
            if keys[pygame.K_e]:
                if self.e_key_released:
                    self.e_key_released = False
                    self.current_section += 1
            else:
                self.e_key_released = True

            pygame.draw.rect(screen, COLOUR_GREY, self.text_box)
            text_to_show = self.font.render(self.all_text_sections[self.current_section], True,
                                            COLOUR_BLACK)

            if self.name is not None:
                name_to_show = self.font.render(self.name, True, COLOUR_BLACK)
                pygame.draw.rect(screen, COLOUR_GREY, self.name_box)
                screen.blit(name_to_show, (20, 365))

            screen.blit(text_to_show, (20, 450))

        except IndexError:
            self.current_section = 0
            return True


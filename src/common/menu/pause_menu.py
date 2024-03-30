"""
    Menu opened when Esc is pressed. Contains options to go back to title, access inventory, see stats, etc.
"""

import pygame

from src.common import global_constants
from src.common.global_constants import JETBRAINS_MONO
from src.player_info import player_save_data


class PauseMenu:
    def __init__(self):
        pygame.font.init()

        self.status = pygame.rect.Rect(0, 0, 800, 600)
        self.font = pygame.font.Font(JETBRAINS_MONO, 40)

    def draw(self, screen):
        pygame.draw.rect(screen, global_constants.COLOUR_PAUSE_MENU, self.status)
        status_name = self.font.render(f"Name:\n{player_save_data.get_player_name()}", True,
                                       global_constants.COLOUR_WHITE)
        status_playtime = self.font.render(f"Time Played:\n"
                                           f"{str(player_save_data.hours_played).zfill(2)}:"
                                           f"{str(player_save_data.minutes_played).zfill(2)}:"
                                           f"{str(player_save_data.seconds_played).zfill(2)}", True,
                                           global_constants.COLOUR_WHITE)
        screen.blit(status_name, (50, 50))
        screen.blit(status_playtime, (200, 50))


pause_menu = PauseMenu()

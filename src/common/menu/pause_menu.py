"""
    Menu opened when Esc is pressed. Contains options to go back to title, access inventory, see stats, etc.
"""

import pygame

from src.common import colours

from src.player_info import player_save_data


class PauseMenu:
    def __init__(self):
        self.status = pygame.rect.Rect(10, 10, 800, 600)
        self.font = pygame.font.Font(None, 60)

    def draw(self, screen):
        pygame.draw.rect(screen, colours.GREY, self.status)
        status_name = self.font.render(f"Name:\n{player_save_data.get_player_name()}", True, colours.WHITE)
        status_playtime = self.font.render(f"Time Played:\n"
                                           f"{player_save_data.hours_played}:{player_save_data.minutes_played}:"
                                           f"{player_save_data.seconds_played}", True, colours.WHITE)

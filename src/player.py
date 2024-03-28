"""
    Manages the player's presence in the world.

    Lachlan Paul, 2024
"""
import os

import pygame


class Player:
    def __init__(self):
        SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sprite = pygame.image.load(os.path.join(SRC_DIR, "assets", "player.jpg"))
        self.sprite = pygame.transform.scale(self.sprite, (130, 130))

        # By default, the player is in the centre of the screen
        self.x = 330
        self.y = 230

        self.hitbox = self.sprite.get_rect()

    def draw(self, screen, w, h):
        # Calculate the center of the screen
        x = w // 2
        y = h // 2

        # Calculate the top left position of the sprite
        sprite_x = x - self.sprite.get_width() // 2
        sprite_y = y - self.sprite.get_height() // 2

        screen.blit(self.sprite, (sprite_x, sprite_y))
        self.hitbox.topleft = (sprite_x, sprite_y)

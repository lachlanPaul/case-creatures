"""
    The Player Class

    Lachlan Paul, 2024
"""

import pygame


class Player:
    def __init__(self):
        self.name = "John"
        self.sprite = pygame.image.load("../assets/placeholder.jpg")
        self.sprite = pygame.transform.scale(self.sprite, (130, 130))

        # By default, the player is in the centre of the screen
        self.x = 330
        self.y = 230

        self.hitbox = self.sprite.get_rect()

    def draw(self, screen, x, y):
        screen.blit(self.sprite, (x, y))
        self.hitbox.topleft = (x, y)

    def move_x(self, screen, move_by):
        self.x += move_by

    def move_y(self, screen, move_by):
        self.y += move_by

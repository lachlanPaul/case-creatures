"""
    Contains the class for creating new world objects using images, as well as some common ones used frequently.

    Lachlan Paul, 2024
"""
import pygame

from src.common import colours


class WorldObject:
    def __init__(self, name, sprite_path, width, height, pos_x, pos_y, screen, offset_list):
        """
        :param name: the name of the object. just in case we need it for future reference
        :param sprite_path: image path
        :param offset_list: list to add self to so that it is correctly offset with the rest of the world
        """
        self.name = name

        self.width = width
        self.height = height

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.sprite = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

        self.hitbox = self.sprite.get_rect()

        screen.blit(self.sprite, (self.pos_x, self.pos_y))

        offset_list.append(self)

    def draw(self, screen, x, y):
        screen.blit(self.sprite, (self.pos_x + x, self.pos_y + y))

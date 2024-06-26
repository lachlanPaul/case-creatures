"""
    Contains the class for creating new world objects using images, as well as some common ones used frequently.

    Lachlan Paul, 2024
"""
import pygame

import src.common.menu.text_box
from src.common.global_constants import COLOUR_RED


class InteractRadius:
    def __init__(self, pos_x, pos_y, width, height, interact_method=None, screen=None, keys=None):
        # Creates a radius around the object. This will be used for interactions
        # Please excuse these magic numbers
        self.interact_radius = pygame.rect.Rect(pos_x - 27, pos_y - 30, width + 55, height + 55)

        if type(interact_method) == src.common.menu.text_box.TextBox:
            self.interact_method = interact_method
        else:
            self.interact_method = interact_method

    def draw(self, screen, offset_x, offset_y):
        pygame.draw.rect(screen, (255, 0, 0), self.interact_radius.move(offset_x, offset_y), 2)


class WorldObject:
    def __init__(self, name, sprite_path, width, height, pos_x, pos_y, screen, offset_list, interact_method=None, keys=None):
        """
        :param name: the name of the object. just in case we need it for future reference
        :param sprite_path: image path
        :param width: the width
        :param height: you guessed it, the width
        :param pos_x: their x position in the world
        :param pos_y: their y position in the world
        :param screen: the screen to draw to
        :param offset_list: list to add self to so that it is correctly offset with the rest of the world
        """
        self.name = name

        self.width = width
        self.height = height

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.sprite = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

        self.interact_radius = InteractRadius(self.pos_x, self.pos_y, self.width, self.height, interact_method, screen, keys)

        self.hitbox = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

        screen.blit(self.sprite, (self.pos_x, self.pos_y))

        offset_list.append(self)
        offset_list.append(self.interact_radius)

    def draw(self, screen, x, y):
        screen.blit(self.sprite, (self.pos_x + x, self.pos_y + y))
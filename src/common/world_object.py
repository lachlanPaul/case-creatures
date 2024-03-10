"""
    Contains the class for creating new world objects using images, as well as some common ones used frequently.

    Lachlan Paul, 2024
"""
import pygame


class WorldObject:
    def __init__(self, name, sprite_path, width, height, offset_list):
        """
        :param name: the name of the object. just in case we need it for future reference
        :param sprite_path: image path
        :param offset_list: list to add self to so that it is correctly offset with the rest of the world
        """
        self.name = name
        self.sprite = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (width, height))

        self.hitbox = self.sprite.get_rect()

        offset_list.append(self)

    def draw(self, screen, x, y):
        screen.blit(self.sprite, (x, y))
        self.hitbox.topleft = (x, y)

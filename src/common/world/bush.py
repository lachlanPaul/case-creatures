"""
    Walking through this bush has a chance to start a wild creature encounter

    Lachlan Paul, 2024
"""
import random

import pygame

from src.common.world.world_object import WorldObject


def chance_for_battle(percent_chance):
    return random.random() <= percent_chance / 100.0


class Bush(WorldObject):
    def __init__(self, width, height, pos_x, pos_y, screen, offset_list):
        super().__init__(None, "../assets/bush.png", width, height, pos_x, pos_y, screen, offset_list, None)

        # Bush doesn't need this, so we get this goober out of here
        offset_list.remove(self.interact_radius)
        del self.interact_radius

        self.sprite = pygame.transform.scale(self.sprite, (100, 100))

    def draw(self, screen, x, y):
        for i in range(0, self.width, 100):
            for j in range(0, self.height, 100):
                screen.blit(self.sprite, (self.pos_x + x + i, self.pos_y + y + j))

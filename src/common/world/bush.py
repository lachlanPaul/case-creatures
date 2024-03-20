"""
    Walking through this bush has a chance to start a wild creature encounter

    Lachlan Paul, 2024
"""
import random

from src.common.world.world_object import WorldObject


def chance_for_battle(percent_chance):
    return random.random() <= percent_chance / 100.0


class Bush(WorldObject):
    def __init__(self, offset_list):
        super().__init__(offset_list)

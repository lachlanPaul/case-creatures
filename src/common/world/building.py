"""
    Enter-able buildings. Extends off of WorldObject, and also contains commonly used objects.

    Lachlan Paul, 2024
"""
from src.common.world.world_object import WorldObject


class Building(WorldObject):
    def __init__(self, name, sprite_path, width, height, offset_list, entrance_placement):
        """
        Docs for other parameters can be found in world_object.py
        :param entrance_placement: position of entrance. upon collision, the player will be loaded into the new area.
        """
        super().__init__(name, sprite_path, width, height, offset_list)

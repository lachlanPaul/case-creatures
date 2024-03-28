"""
    This class manages the PLayer's data, such as Name, Team, Boxes, Badges, etc.

    Lachlan Paul, 2024
"""
from src.common.creatures import Creature


class PlayerInfo:
    def __init__(self):
        self.name = None
        self.team = []
        self.box = []

    # Setters and getters are probably a bit pointless for the name,
    # but it might look a bit nicer over player_info.PlayerInfo.name.
    def set_player_name(self, name: str):
        self.name = name

    def get_player_name(self):
        return self.name

    # TODO: Add menu functionality when it happens

    def add_to_team(self, creature: Creature):
        if len(self.team) <= 5:
            self.team.append(creature)
        else:
            # TODO: Make this work
            #  Once menus have been added, this function will most likely be called from there
            pass

    def move_to_box(self, team_index):
        move_this_goober = self.team.pop(team_index)
        self.box.append(move_this_goober)

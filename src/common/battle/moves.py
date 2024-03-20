"""
    Contains the move class, as well as all the moves in the game.

    Lachlan Paul, 2024
"""
import warnings

from src.common.battle.types import Types


class Move:
    instances = []

    def __init__(self,
                 name,
                 description,
                 move_type,
                 required_level: int,
                 base_dam: int,
                 chance_of_hit: int,
                 hits_first: bool
                 ):
        """

            :param name: name to be shown in move select
            :param description: description shown in move select
            :param move_type: determines if a move has different damage properties based on the opposing creature's type
            :param required_level: level required before a creature can learn move
            :param base_dam: base damage before it's modified by the creature's stats
            :param chance_of_hit: a percentage chance between 1 - 100 of the move hitting
            :param hits_first: if true, the move will always hit first, as long as the other move doesn't also
        """

        # TODO: Check these length values and pick ones that make sense
        #  Cause they're just guesses right now
        if len(name) > 15:
            warnings.warn(f"Name of move '{name}' might be too long!")
        self.name = name

        if len(description) > 30:
            warnings.warn(f"Description of move '{name}' might be too long!")
        self.description = description

        if not isinstance(move_type, Types):
            warnings.warn(f"'{name}' has an invalid move type of {move_type}")
        else:
            self.move_type = move_type

        if 0 > required_level > 100:
            warnings.warn(f"Move '{name}' requires a level unattainable")
        self.required_level = required_level

        self.base_dam = base_dam
        self.chance_of_hit = chance_of_hit
        self.hits_first = hits_first

        self.instances.append(self)  # This is for automating lists of moves to be made


quick_hit = Move(
    "Quick Hit",
    "The user quickly attacks",
    Types.BASIC,
    5,
    15,
    80,
    True
)

tackle = Move(
    "Tackle",
    "The user tackles their opponent",
    Types.BASIC,
    1,
    7,
    80,
    False
)

basic_moves = []
furniture_moves = []

all_moves = []

for instance in Move.instances:
    # Automatically updates lists containing all the moves within a certain type
    eval(f'{str(instance.move_type).split(".")[-1].lower()}_moves.append(instance)')  # optemysashun
    all_moves.append(instance)

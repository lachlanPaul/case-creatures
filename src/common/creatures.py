import os
import random
from math import floor

import pygame

from src.common.battle.move_creature_types import Types
from src.common.battle.moves import *
from src.common.global_constants import ROOT_DIR


class Creature:
    def __init__(self,
                 name,
                 description,
                 creature_type,
                 learnable_moves,
                 base_level,
                 base_health,
                 base_atk,
                 base_def,
                 base_spd,
                 ev,
                 sprite=None,
                 in_pedia=True,
                 cannot_be_poisoned = False,
                 ):
        """
        :param name: name of the creature to be shown in various places
        :param description: description of the creature to be shown in encyclopedia
        :param creature_type: creature type: see battle/move_creature_types.py
        :param learnable_moves: a list of all the moves that the creature may randomly learn upon leveling up
        :param base_level: base level expected for the creature to appear. will be overwritten so is more of a guideline
        :param base_health: base health expected for their base level
        :param base_atk: base attack expected for their base level. used for battle calculations
        :param base_def: base defense expected for their base level. used for battle calculations
        :param base_spd: base speed expected for their base level. used for battle calculations
        :param ev: a number of either 1, 2 or 3 which is added to the opposing creature's accumulated EV when defeated,
               which is used when levelling up
        :param sprite: path to the creature's sprite, if left blank the program will look for a file matching 'name'.jpg
        :param in_pedia: defaults to True, as the only creatures not appearing will be for debug and tests
        """

        # TODO: Make string length checks once a size has been decided

        self.name = name
        self.description = description
        self.learnable_moves = learnable_moves

        # Because of the way learnable moves are passed (a list of lists), we use this to combine them into one big list
        if type(self.learnable_moves[0]) == list:
            new_list = []
            for item in self.learnable_moves[0]:
                new_list.append(item)
            self.learnable_moves = new_list

        self.moves = []
        self.in_pedia = in_pedia

        self.attack = base_atk
        self.defense = base_def
        self.speed = base_spd

        self.HEALTH_IV = None
        self.ATK_IV = None
        self.DEF_IV = None
        self.SPD_IV = None

        # Accumulated EV is used by a creature when levelling up
        # EV is the amount added to the creature's accumulation when they defeat the creature
        # This is a bad explanation, go look it up if you care enough
        self.EV = ev
        self.accumulated_ev = ev  # Start off at the creature's base EV

        self.level = base_level
        self.base_health = base_health  # This is here so we can access it in create_stats()
        self.max_health = base_health
        self.current_health = self.max_health

        # Checks for type and sprite validity
        if not isinstance(creature_type, Types):
            raise TypeError(f"{self.name} has an invalid creature type! Must be an object from Types.")
        else:
            self.creature_type = creature_type

        # This shit is very goofy.
        # Basically it just leaps back to the root directory,
        # so that there's no issues when this is called form files in different directories.
        if sprite is None:
            try:
                sprite_path = os.path.join(ROOT_DIR, "assets", "creatures", f"{name}.jpg")
                self.sprite = pygame.image.load(sprite_path)
            except FileNotFoundError:
                warnings.warn(f"{name}'s sprite was not found, setting to missing texture")
                missing_texture_path = os.path.join(ROOT_DIR, "assets", "missing.jpg")
                self.sprite = pygame.image.load(missing_texture_path)
        else:
            self.sprite = pygame.image.load(sprite)
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))

        self.cannot_be_poisoned = cannot_be_poisoned

        self.is_poisoned = False
        self.is_sleeping = False
        self.is_paralysed = False

        self.turns_since_poisoned = 0
        self.turns_since_sleeping = 0
        self.turns_since_paralysed = 0

    def create_creature(self):
        """Randomises all that needs to be randomised in the creature upon encounter"""
        # Random number for variation in stats
        rand_iv = random.randint(0, 31)
        self.HEALTH_IV = rand_iv
        self.ATK_IV = rand_iv
        self.DEF_IV = rand_iv
        self.SPD_IV = rand_iv

        self.randomise_moves()
        self.create_stats()

    def randomise_moves(self):
        """
            ONLY RUN ON CREATURE CREATION IN NEW ROUTES.
            Randomises creatures moves, ensuring that they fit their level.
            This is here instead of init because the creature will most likely have a different level then their base
            level when found, so this ensures the moves they get fit their level.
        """
        self.moves = []  # Just in case something goofed
        for _ in range(4):
            while True:
                move = random.choice(self.learnable_moves)

                # Checks for duplicates
                for i in self.moves:
                    if move == i:
                        continue

                if self.level >= move.required_level:
                    self.moves.append(move)
                else:
                    continue
                break

    def create_stats(self):
        self.max_health = floor(0.01 * (2 * self.base_health + self.HEALTH_IV + floor(
            0.25 * self.accumulated_ev)) * self.level) + self.level + 10

        # TODO: If traits are implemented, add them into equation
        self.attack = floor(0.01 * (2 * self.attack + self.ATK_IV + floor(0.25 * self.accumulated_ev)) * self.level) + 5

        self.defense = floor(
            0.01 * (2 * self.defense + self.DEF_IV + floor(0.25 * self.accumulated_ev)) * self.level) + 5

        self.speed = floor(0.01 * (2 * self.speed + self.SPD_IV + floor(0.25 * self.accumulated_ev)) * self.level) + 5


"""
    All the creatures. Sorted by order in encyclopedia
"""

"""DEBUG AND TEST. NOT INCLUDED IN ENCYCLOPEDIA"""
debug = Creature("DEBUG", "DEBUG", Types.BASIC, all_moves, 999, 999, 999, 999, 999, 3, in_pedia=False)

"""STARTERS"""
chair = Creature("Chair", "A basic wooden chair", Types.FURNITURE,
                 [basic_moves, furniture_moves], 5, 20, 10, 15,
                 7, 1)

"""
    The opposing trainer. This class manages their presence in the world and in battle.
"""
import enum
import random

import pygame


class Directions(enum.Enum):
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3


class Vision:
    def __init__(self, pos_x, pos_y, width, height):
        self.hitbox = pygame.rect.Rect(pos_x - 100, pos_y - 100, width, height)

    def draw(self, screen, offset_x, offset_y):
        """For testing"""
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox.move(offset_x, offset_y), 2)


class Trainer:
    def __init__(self, name: str, character_type: str, possible_creatures: list, team_size: int, pos_x: int, pos_y: int,
                 direction_facing: Directions, sprite_path: str, offset_list: list, team=None, wants_to_battle=None):
        """
        :param name: trainer's name
        :param character_type: the prefix of their name, eg; Karate Boy, Office Worker, etc
        :param possible_creatures: if they don't have a predefined team, they will be given a random team from this list
        :param team_size: the max size their team can be if it's randomised. max size 5
        :param sprite_path: full path to the sprite image
        :param team: a predefined team. a random team will be given if this isn't present
        :param wants_to_battle: if there is one, give them a unique "wants to battle" quote
        """
        self.name = name
        self.character_type = character_type
        if wants_to_battle is None:
            self.wants_to_battle = "wants to battle!"
        else:
            self.wants_to_battle = wants_to_battle  # "wants to throw hands!"

        self.pos_x = pos_x
        self.pos_y = pos_y

        LONG_WAYS_VISION = 250
        SHORT_WAYS_VISION = 130

        self.sprite = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (130, 130))
        self.hitbox = pygame.Rect(self.pos_x - 100, self.pos_y - 100, 130, 130)

        match direction_facing:
            case Directions.UP:
                self.vision = Vision(self.pos_x, self.pos_y - LONG_WAYS_VISION, SHORT_WAYS_VISION, LONG_WAYS_VISION)
            case Directions.LEFT:
                self.vision = Vision(self.pos_x - LONG_WAYS_VISION, self.pos_y, LONG_WAYS_VISION, SHORT_WAYS_VISION)
            case Directions.RIGHT:
                self.vision = Vision(self.pos_x + SHORT_WAYS_VISION, self.pos_y, LONG_WAYS_VISION, SHORT_WAYS_VISION)
            case Directions.DOWN:
                self.vision = Vision(self.pos_x, self.pos_y + SHORT_WAYS_VISION, SHORT_WAYS_VISION, LONG_WAYS_VISION)

        self.is_defeated = False  # This will be set to True when they are defeated, so they're only fight-able once

        self.full_name = character_type + name  # Lawyer Phoenix Wright wants to battle!

        # Generates a random team if none is given
        if team is None:
            self.team = []
            for _ in range(team_size):
                self.team.append(random.choice(possible_creatures))
            while len(self.team) > 5:  # In case I goof
                self.team.remove(-1)
        else:
            self.team = team

        offset_list.append(self)
        offset_list.append(self.hitbox)
        offset_list.append(self.vision)

    def draw(self, screen, x, y):
        screen.blit(self.sprite, ((self.pos_x - 100) + x, (self.pos_y - 100) + y))

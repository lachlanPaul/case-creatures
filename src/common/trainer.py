"""
    The opposing trainer. This class manages their presence in the world and in battle.
"""
import enum
import random

import pygame

from src.common import colours


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
    def __init__(self, name, character_type, possible_creatures, team_size, pos_x, pos_y, direction_facing: Directions,
                 sprite_path, offset_list,
                 team=None):
        """
        :param name: trainer's name
        :param character_type: the prefix of their name, eg; Karate Boy, Office Worker, etc
        :param possible_creatures: if they don't have a predefined team, they will be given a random team from this list
        :param team_size: the max size their team can be if it's randomised. max size 5
        :param sprite_path: full path to the sprite image
        :param team: a predefined team. a random team will be given if this isn't present
        """
        self.name = name
        self.character_type = character_type

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.sprite = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (130, 130))
        self.hitbox = pygame.Rect(self.pos_x - 100, self.pos_y - 100, 130, 130)

        match direction_facing:
            case Directions.UP:
                self.vision = Vision(self.pos_x, self.pos_y - 250, 130, 250)
            case Directions.LEFT:
                self.vision = Vision(self.pos_x - 250, self.pos_y, 250, 130)
            case Directions.RIGHT:
                self.vision = Vision(self.pos_x + 130, self.pos_y, 250, 130)
            case Directions.DOWN:
                self.vision = Vision(self.pos_x, self.pos_y + 130, 130, 250)

        self.team = []
        self.is_defeated = False  # This will be set to True when they are defeated, so they're only fight-able once

        self.full_name = character_type + name  # Lawyer Phoenix Wright wants to battle!

        if team is None:
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
        self.vision.draw(screen, x, y)

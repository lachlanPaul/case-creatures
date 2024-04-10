"""
    All menus that appear during battle and their controls

    Lachlan Paul, 2024
"""

import pygame

import src.common.battle.battle
from src.player_info import player_save_data as player
from src.common.global_constants import COLOUR_GREY
from src.common.menu.button import Button


class BattleMenu:
    def __init__(self, battle_instance: src.common.battle.battle.Battle):
        """
            Creates, draws and manages input for buttons when in battle

            :param battle_instance: an instance of the Battle class
        """
        self.battle_instance = battle_instance

        self.player_inventory = self.battle_instance.player_inventory
        self.player_team = self.battle_instance.player_team
        self.player_current_creature_index = self.battle_instance.player_current_creature_index

        self.BUTTON_NOT_SELECTED_COLOUR = COLOUR_GREY
        self.BUTTON_SELECTED_COLOUR = (164, 166, 166)
        self.BUTTON_WIDTH_HEIGHT = (200, 300)

        # The buttons are arranged in a grid, the numbers correspond to which button
        # What the grid will look like:
        # 1  2
        # 3  4
        self.BUTTON_1_POS = (300, 500)
        self.BUTTON_2_POS = (600, 500)
        self.BUTTON_3_POS = (300, 700)
        self.BUTTON_4_POS = (600, 700)

        self.info_box = pygame.Rect(0, 600, 600, 200)

        # First screen
        self.option_battle = Button(self.BUTTON_1_POS, self.BUTTON_WIDTH_HEIGHT, "Battle",
                                    self.BUTTON_NOT_SELECTED_COLOUR, self.BUTTON_SELECTED_COLOUR)
        self.option_items = Button(self.BUTTON_2_POS, self.BUTTON_WIDTH_HEIGHT, "Items",
                                   self.BUTTON_NOT_SELECTED_COLOUR, self.BUTTON_SELECTED_COLOUR)
        self.option_team = Button(self.BUTTON_3_POS, self.BUTTON_WIDTH_HEIGHT, "Change\nCreature",
                                  self.BUTTON_NOT_SELECTED_COLOUR, self.BUTTON_SELECTED_COLOUR)
        self.option_run = Button(self.BUTTON_4_POS, self.BUTTON_WIDTH_HEIGHT, "Run", self.BUTTON_NOT_SELECTED_COLOUR,
                                 self.BUTTON_SELECTED_COLOUR)

        self.decision_menu_buttons = [self.option_battle, self.option_items, self.option_team, self.option_run]

        self.battle_buttons = []
        self.inventory_buttons = []
        self.team_buttons = []

        self.current_menu_buttons = self.decision_menu_buttons
        self.current_menu_index = 0

        # Creates the lists containing buttons
        for i in self.player_team[self.player_current_creature_index].moves:
            self.battle_buttons.append(i)

        for i in self.player_inventory:
            self.inventory_buttons.append(i)

        for i in self.player_team:
            self.team_buttons.append(i)

    def open_menu(self):
        match self.decision_menu_buttons[self.current_menu_index]:
            case self.option_battle:
                self.current_menu_buttons = self.battle_buttons
            case self.option_items:
                self.current_menu_buttons = self.inventory_buttons
                self.current_menu_index = 0
            case self.option_team:
                self.current_menu_buttons = self.team_buttons
                self.current_menu_index = 0

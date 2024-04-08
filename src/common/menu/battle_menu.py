"""
    All menus that appear during battle and their controls

    Lachlan Paul, 2024
"""

import pygame

from src.common.menu.button import Button


class BattleMenu:
    def __init__(self, player_inventory, player_team, player_creature, enemy_team, enemy_creature):
        self.player_inventory = player_inventory
        self.player_team = player_team
        self.player_creature = player_creature
        self.enemy_team = enemy_team
        self.enemy_creature = enemy_creature

        self.BUTTON_HEIGHT = 200
        self.BUTTON_WIDTH = 300

        self.info_box = pygame.Rect(0, 600, 600, 200)
        self.option_battle = Button(300, 500, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, "Battle")
        self.option_items = Button(600, 500, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, "Items")
        self.option_team = Button(300, 700, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, "Change\nCreature")
        self.option_run = Button(500, 700, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, "Run")

        self.decision_menu_buttons = [self.option_battle, self.option_items, self.option_team, self.option_run]

        self.battle_buttons = []
        self.inventory_buttons = []
        self.team_buttons = []

        self.current_menu_buttons = self.decision_menu_buttons
        self.current_menu_index = 0

        for i in self.player_team[player_creature.moves]:
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

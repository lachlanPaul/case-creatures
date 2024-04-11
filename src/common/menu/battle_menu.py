"""
    All menus that appear during battle and their controls

    Lachlan Paul, 2024
"""

import pygame

from src.common.battle import move_creature_types
from src.common.global_constants import COLOUR_GREY
from src.common.menu.button import Button
from src.common.menu.text_box import TextBox


class BattleMenu:
    def __init__(self, battle_instance, screen):
        """
            Creates, draws and manages input for buttons when in battle

            :param battle_instance: an instance of the Battle class
        """
        self.battle_instance = battle_instance
        self.SCREEN = screen
        self.current_text_box = False  # Defaults to False when there is nothing to show

        self.starting_text = TextBox(f"{battle_instance.enemy.full_name} {battle_instance.enemy.wants_to_battle}")

        self.player_inventory = self.battle_instance.player_inventory
        self.player_team = self.battle_instance.player_team
        self.player_current_creature_index = self.battle_instance.player_current_creature_index

        self.BUTTON_NOT_SELECTED_COLOUR = COLOUR_GREY
        self.BUTTON_SELECTED_COLOUR = (164, 166, 166)
        self.BUTTON_WIDTH_HEIGHT = (200, 300)

        # The buttons are arranged in a grid, the numbers correspond to which button
        # What the grid will look like:
        # 0  1
        # 2  3
        self.BUTTON_0_POS = (300, 500)
        self.BUTTON_1_POS = (600, 500)
        self.BUTTON_2_POS = (300, 700)
        self.BUTTON_3_POS = (600, 700)

        self.info_box = pygame.Rect(0, 600, 600, 200)

        # First screen
        self.option_battle = self.create_grid_button(0, "Battle")
        self.option_items = self.create_grid_button(1, "Items")
        self.option_team = self.create_grid_button(2, "Change\nCreature")
        self.option_run = self.create_grid_button(3, "Run")

        self.decision_menu_buttons = [self.option_battle, self.option_items, self.option_team, self.option_run]

        self.battle_buttons = []
        self.inventory_buttons = []
        self.team_buttons = []

        # Create all the extra menus
        self.create_new_moves_menu()

        for i in self.player_inventory:
            self.inventory_buttons.append(i)

        for i in self.player_team:
            self.team_buttons.append(i)

        self.current_menu_buttons = self.decision_menu_buttons
        self.current_menu_index = 0

    def create_grid_button(self, position, text):
        """
            Creates a new button for the regular 4 button grid layout

            :param position: their position in the grid, on a scale of 0 - 3
            :param text: text to show
            :return: the new button
        """
        # Gets the variable with the position needed for button position
        pos = eval(f"self.BUTTON_{position}_POS")
        return Button(pos, self.BUTTON_WIDTH_HEIGHT, text, self.BUTTON_NOT_SELECTED_COLOUR, self.BUTTON_SELECTED_COLOUR)

    def create_new_moves_menu(self):
        """Display new moves in the menu when it's a new creature"""
        self.battle_buttons = []
        position = 0

        for i in self.player_team[self.player_current_creature_index].moves:
            position += 1
            move_name = i.name
            self.create_grid_button(position, move_name)
            self.battle_buttons.append(i)

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

    def navigate_menu(self, key_pressed):
        # TODO: Make alternate path for when in inventory
        if self.current_menu_buttons is not self.inventory_buttons:
            match key_pressed:
                case pygame.K_w:
                    if self.current_menu_index is (0 or 1):
                        self.current_menu_index += 2
                    else:
                        self.current_menu_index -= 2
                case pygame.K_a:
                    if self.current_menu_index is (0 or 2):
                        self.current_menu_index += 1
                    else:
                        self.current_menu_index -= 1
                case pygame.K_s:
                    if self.current_menu_index is (2 or 3):
                        self.current_menu_index -= 2
                    else:
                        self.current_menu_index += 2
                case pygame.K_d:
                    if self.current_menu_index is (1 or 3):
                        self.current_menu_index -= 1
                    else:
                        self.current_menu_index += 1

    def show_text_message(self, keys):
        if self.current_text_box:
            self.current_text_box.interact(self.SCREEN, keys)

    def announce_attack_effectiveness(self, victim, attack):
        type_modifier = move_creature_types.type_modifier(victim.creature_type, attack.move_type)
        announce_box = False

        match type_modifier:
            case 0:
                announce_box = TextBox("It didn't do anything!")
            case 2.5:
                announce_box = TextBox("It's not very effective")
            case 10:
                announce_box = TextBox("It's super effective!")

        if announce_box:
            self.current_text_box = announce_box

    def draw(self, screen):
        for item in self.current_menu_buttons:
            item.draw(screen)

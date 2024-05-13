"""
    All menus that appear during battle and their controls

    Lachlan Paul, 2024
"""

import pygame

from src.common.battle import move_creature_types
from src.common.global_constants import COLOUR_GREY, COLOUR_BLACK
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

        self.w_key_released = True
        self.a_key_released = True
        self.s_key_released = True
        self.d_key_released = True
        self.e_key_pressed = True

        self.BUTTON_NOT_SELECTED_COLOUR = COLOUR_GREY
        self.BUTTON_SELECTED_COLOUR = (255, 255, 153)
        self.BUTTON_WIDTH_HEIGHT = (200, 100)

        # The buttons are arranged in a grid, the numbers correspond to which button
        # What the grid will look like:
        # 0  1
        # 2  3
        self.BUTTON_0_POS = (100, 350)  # Top left corner
        self.BUTTON_1_POS = (500, 350)  # Top right corner
        self.BUTTON_2_POS = (100, 450)  # Bottom left corner
        self.BUTTON_3_POS = (500, 450)  # Bottom right corner

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

        while True:
            try:
                for i in self.player_team[self.player_current_creature_index].moves:
                    move_name = i.name
                    self.battle_buttons.append(self.create_grid_button(position, move_name))
                    self.create_grid_button(position, move_name)
                break
            except TypeError:
                self.player_team[self.player_current_creature_index].randomise_moves()

    def open_menu(self):
        match self.current_menu_buttons[self.current_menu_index]:
            case self.option_battle:
                self.create_new_moves_menu()
                self.current_menu_buttons = self.battle_buttons
            case self.option_items:
                self.current_menu_buttons = self.inventory_buttons
                self.current_menu_index = 0
            case self.option_team:
                self.current_menu_buttons = self.team_buttons
                self.current_menu_index = 0

    def navigate_menu(self, key_pressed):
        if self.current_menu_buttons is not self.inventory_buttons:
            key_is_pressed = False

            if key_pressed[pygame.K_w]:
                if self.w_key_released:
                    if self.current_menu_index in (0, 1):
                        self.current_menu_index += 2
                    else:
                        self.current_menu_index -= 2
                    key_is_pressed = True
                    self.w_key_released = False
            else:
                self.w_key_released = True

            if key_pressed[pygame.K_a]:
                if self.a_key_released:
                    if self.current_menu_index in (0, 2):
                        self.current_menu_index += 1
                    else:
                        self.current_menu_index -= 1
                    key_is_pressed = True
                    self.a_key_released = False
            else:
                self.a_key_released = True

            if key_pressed[pygame.K_s]:
                if self.s_key_released:
                    if self.current_menu_index in (2, 3):
                        self.current_menu_index -= 2
                    else:
                        self.current_menu_index += 2
                    key_is_pressed = True
                    self.s_key_released = False
            else:
                self.s_key_released = True

            if key_pressed[pygame.K_d]:
                if self.d_key_released:
                    if self.current_menu_index in (1, 3):
                        self.current_menu_index -= 1
                    else:
                        self.current_menu_index += 1
                    key_is_pressed = True
                    self.d_key_released = False
            else:
                self.d_key_released = True

            if key_pressed[pygame.K_e] and self.e_key_pressed:
                self.e_key_pressed = False
                self.open_menu()
            elif not key_pressed[pygame.K_e]:
                self.e_key_pressed = True

            if key_is_pressed:
                for index, i in enumerate(self.current_menu_buttons):
                    if index == self.current_menu_index:
                        self.current_menu_buttons[index].is_selected = True
                    else:
                        self.current_menu_buttons[index].is_selected = False

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

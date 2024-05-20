"""
    Where the game runs.
    This is where the game starts and controls player movement, ui, area loading, as well as save files.

    Lachlan Paul, 2024
"""
import enum
from math import floor

import pygame

import src.common.world.world_object
from player import Player
from src.common import creatures
from src.common.battle.battle import Battle
from src.common.global_constants import JETBRAINS_MONO, COLOUR_BLACK, COLOUR_WHITE
from src.common.menu.button import Button
from src.common.menu.pause_menu import pause_menu
from src.common.menu.text_box import TextBox
from src.common.trainer import Trainer, Directions
from src.common.world.bush import Bush, chance_for_battle
from src.common.world.world_object import WorldObject
from src.player_info import player_save_data


class States(enum.Enum):
    IN_TITLE_SCREEN = 0
    IN_WORLD = 1
    IN_TEXT = 2
    IN_MENU = 3
    IN_BATTLE = 4


class Main:
    def __init__(self):
        pygame.init()

        self.WIDTH = 800
        self.HEIGHT = 600
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Case Creatures")

        self.player = Player()
        self.PLAYER_SPEED = 10
        self.clock = pygame.time.Clock()
        self.FRAMES_PER_SECOND = 30

        self.keys = pygame.key.get_pressed()
        self.seconds_counted = 0

        self.game_running = True
        self.current_state = States.IN_WORLD

        self.current_text_box = None  # This will be set to the most recent text box read for reloading when reading.
        self.current_menu = None
        self.current_interact_radius = None
        self.current_battle = None

        self.offset_x = 0
        self.offset_y = 0

        # The offset reverts to their old variables if there's a collision
        # Or technically, is it "if there's *going* to be a collision?"
        self.old_offset_x = self.offset_x
        self.old_offset_y = self.offset_y

        self.movement_key_pressed = False
        self.in_bush = False

        self.items_to_offset = []
        self.collidable_items = []

        # Test Objects
        self.funny = TextBox("GAHAHA! You my friend, are on the road to glory!!!!!!!!!!!!!!!!!!", "Zangief")
        self.thingo = WorldObject("haus", "../assets/placeholder.jpg", 200, 100, 100, 500, self.SCREEN,
                                  self.items_to_offset, self.funny, self.keys)
        self.troin = Trainer("d", "guy", [creatures.chair], 1, 600, 500, Directions.UP, "../assets/placeholder.jpg",
                             self.items_to_offset)

        # self.butt = Button((20, 20), (20, 20), "a", COLOUR_BLACK, COLOUR_BLACK)
        # self.bush = Bush(200, 200, 200, 26, self.SCREEN, self.items_to_offset)

    def movement_keys(self):
        """Manages movement"""
        if self.keys[pygame.K_w]:
            self.offset_y += self.PLAYER_SPEED
            self.movement_key_pressed = True
        elif self.keys[pygame.K_a]:
            self.offset_x += self.PLAYER_SPEED
            self.movement_key_pressed = True
        elif self.keys[pygame.K_d]:
            self.offset_x -= self.PLAYER_SPEED
            self.movement_key_pressed = True
        elif self.keys[pygame.K_s]:
            self.offset_y -= self.PLAYER_SPEED
            self.movement_key_pressed = True

    def update_world(self):
        """Updates the position of everything, including the player."""
        self.SCREEN.fill(COLOUR_WHITE)

        current_win_size = pygame.display.get_surface().get_size()
        # if self.current_state in [States.IN_WORLD, States.IN_TEXT]:

        for item in self.items_to_offset:
            match type(item):
                case pygame.Rect:
                    # NOTE: Re-enable this for debugging
                    # pygame.draw.rect(self.SCREEN, (255, 0, 0), item.move(self.offset_x, self.offset_y))
                    pass
                case src.common.world.world_object.InteractRadius:
                    # NOTE: For debug
                    # item.draw(self.SCREEN, self.offset_x, self.offset_y)
                    pass
                case _:
                    # NOTE: Most things should have pretty much the same draw method.
                    #   However, the match case should make it easy to accommodate for a unique draw method.
                    if self.current_state not in [States.IN_BATTLE, States.IN_MENU]:
                        item.draw(self.SCREEN, self.offset_x, self.offset_y)
                        self.player.draw(self.SCREEN, current_win_size[0], current_win_size[1])

                        # TODO: When making configuration files and such, set this to be ran if enabled in settings.
                        fps_font = pygame.font.Font(JETBRAINS_MONO, 60)
                        coords_font = pygame.font.Font(JETBRAINS_MONO, 30)
                        fps_text = fps_font.render(str(floor(self.clock.get_fps())), True, COLOUR_BLACK)
                        coords_text = coords_font.render(
                            (str(f"{self.player.x - self.offset_x}, {self.player.y - self.offset_y}")), True,
                            COLOUR_BLACK)
                        self.SCREEN.blit(fps_text, (0, 0))
                        self.SCREEN.blit(coords_text, (0, 80))

    def player_has_collided(self):
        """
            Returns whether the player should be stopped from moving when they collide with certain objects.

            :return: true: the player has collided, and they are stopped from moving
            :return: false: the player has not collided, and they aren't stopped from moving.
                Is sometimes used to trigger things on collision without stopping movement, ie; trainer vision
        """
        self.current_interact_radius = None

        for item in self.items_to_offset:
            match type(item):
                case pygame.rect.Rect():
                    if self.player.hitbox.colliderect(item.move((self.offset_x, self.offset_y))):
                        return True
                case src.common.world.world_object.WorldObject:
                    if self.player.hitbox.colliderect(item.hitbox.move(self.offset_x, self.offset_y)):
                        return True
                case src.common.world.world_object.InteractRadius:
                    if self.player.hitbox.colliderect(item.interact_radius.move(self.offset_x, self.offset_y)):
                        self.current_interact_radius = item
                        return False
                case src.common.trainer.Trainer:
                    if self.player.hitbox.colliderect(item.hitbox.move(self.offset_x, self.offset_y)):
                        return True
                    elif self.player.hitbox.colliderect(item.vision.hitbox.move(self.offset_x, self.offset_y)):
                        print("Saw you!")
                        if not item.is_defeated:
                            self.current_state = States.IN_BATTLE
                            bottle = Battle(self.SCREEN, item)
                            self.current_battle = bottle
                            print("he")
                        return False
                case src.common.world.bush.Bush:
                    if self.player.hitbox.colliderect(
                            item.hitbox.move((item.pos_x + self.offset_x, item.pos_y + self.offset_y))):
                        self.in_bush = True
                        print(True)
                        return False
                case _:
                    continue
        return False

    def when_in_battle(self):
        self.current_battle.menu.draw(self.SCREEN)
        self.current_battle.menu.navigate_menu(self.keys)

    def main(self):
        while self.game_running:
            self.movement_key_pressed = False
            self.in_bush = False
            self.old_offset_x = self.offset_x
            self.old_offset_y = self.offset_y
            self.keys = pygame.key.get_pressed()

            self.clock.tick(self.FRAMES_PER_SECOND)  # Frame rate

            # Updates the world only if it's being shown
            if self.current_state is not (States.IN_WORLD, States.IN_MENU, States.IN_TITLE_SCREEN):
                self.update_world()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_state is not States.IN_MENU and self.current_menu is not pause_menu:
                            self.current_state = States.IN_MENU
                            self.current_menu = pause_menu
                        else:
                            self.current_state = States.IN_WORLD
                            self.current_menu = None
                    elif event.key == pygame.K_e and self.current_state is States.IN_WORLD and self.current_interact_radius is not None:
                        try:
                            if type(self.current_interact_radius.interact_method) is src.common.menu.text_box.TextBox:
                                self.current_interact_radius.interact_method.interact(self.SCREEN, self.keys)

                                self.current_text_box = self.current_interact_radius.interact_method
                                self.current_state = States.IN_TEXT
                                self.current_text_box.current_section -= 1
                        except TypeError:
                            pass

            # Movement
            if self.current_state == States.IN_WORLD:
                self.movement_keys()

                # TODO: This will be changed to check for a few things
                #  If the collided object is a trainer's vision, or
                #  If the collided object is a door or area load trigger
                if self.player_has_collided():
                    self.offset_x = self.old_offset_x
                    self.offset_y = self.old_offset_y

                # TODO: Abnormal walking pattern, experiment.
                if self.movement_key_pressed and pygame.time.get_ticks() % 3 == 0:
                    self.player.sprite = pygame.transform.flip(self.player.sprite, True, False)

                # Checks for random battle when in bush
                if self.movement_key_pressed and self.in_bush:
                    if chance_for_battle(1):
                        print(True)

            # Put anything that needs to be drawn over the top of the world here.
            if self.current_state == States.IN_TEXT:
                if self.current_text_box.interact(self.SCREEN, self.keys):
                    self.current_state = States.IN_WORLD

            if self.current_menu is pause_menu:
                pause_menu.draw(self.SCREEN)

            # Counts towards the overall playtime counter
            # TODO: Fix. It broke since the fps changed
            if self.current_state is not States.IN_TITLE_SCREEN:
                self.seconds_counted += 1

                if self.seconds_counted == 60:
                    self.seconds_counted = 0
                    player_save_data.add_second_to_playtime()

            if self.current_state is States.IN_BATTLE:
                self.when_in_battle()

            pygame.display.update()


if __name__ == '__main__':
    game = Main()
    game.main()

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
from src.common.global_constants import JETBRAINS_MONO, COLOUR_BLACK
from src.common.menu.text_box import TextBox
from src.common.trainer import Trainer, Directions
from src.common.world.bush import Bush, chance_for_battle
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
        self.PLAYER_SPEED = 3
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.seconds_counted = 0

        self.game_running = True
        self.current_state = States.IN_WORLD

        self.current_text_box = None  # This will be set to the most recent text box read for reloading when reading.
        self.current_menu = None

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
        # self.thingo = WorldObject("haus", "../assets/placeholder.jpg", 50, 50, self.items_to_offset)
        self.troin = Trainer("d", "guy", "cock", 5, 900, 100, Directions.UP, "../assets/placeholder.jpg",
                             self.items_to_offset)
        self.bush = Bush(200, 200, 200, 26, self.SCREEN, self.items_to_offset)
        self.funny = TextBox("gheheflaefsnhfwenfweuofweuogherhguoerhgeruohgerhguerhuigheruig", "mario")

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

    def update_everything(self):
        """Updates the position of everything, including the player."""
        current_win_size = pygame.display.get_surface().get_size()

        self.player.draw(self.SCREEN, current_win_size[0], current_win_size[1])

        for item in self.items_to_offset:
            match type(item):
                case pygame.rect.Rect:
                    # NOTE: Re-enable this for debugging
                    # pygame.draw.rect(self.SCREEN, (255, 0, 0), item.move(self.offset_x, self.offset_y))
                    pass
                case _:
                    # NOTE: Most things should have pretty much the same draw method.
                    #   However, the match case should make it easy to accommodate for a unique draw method.
                    item.draw(self.SCREEN, self.offset_x, self.offset_y)

        # TODO: When making configuration files and such, set this to be ran if enabled in settings.
        fps_font = pygame.font.Font(JETBRAINS_MONO, 60)
        fps_text = fps_font.render(str(floor(self.clock.get_fps())), True, COLOUR_BLACK)
        self.SCREEN.blit(fps_text, (0, 0))

    def player_has_collided(self):
        """
            Returns whether the player should be stopped from moving when they collide with certain objects.

            :return: true: the player has collided, and they are stopped from moving
            :return: false: the player has not collided, and they aren't stopped from moving.
                Is sometimes used to trigger things on collision without stopping movement, ie; trainer vision
        """
        for item in self.items_to_offset:
            match type(item):
                case pygame.rect.Rect():
                    if self.player.hitbox.colliderect(item.move((self.offset_x, self.offset_y))):
                        return True
                case src.common.trainer.Trainer:
                    if self.player.hitbox.colliderect(item.hitbox.move(self.offset_x, self.offset_y)):
                        return True
                    elif self.player.hitbox.colliderect(item.vision.hitbox.move(self.offset_x, self.offset_y)):
                        print("Saw you!")
                        return False
                case src.common.world.bush.Bush:
                    if self.player.hitbox.colliderect(
                            item.hitbox.move((item.pos_x + self.offset_x, item.pos_y + self.offset_y))):
                        self.in_bush = True
                        return False
                case _:
                    continue
        return False

    def main(self):
        while self.game_running:
            self.movement_key_pressed = False
            self.in_bush = False
            self.old_offset_x = self.offset_x
            self.old_offset_y = self.offset_y
            self.keys = pygame.key.get_pressed()

            self.clock.tick(60)  # Frame rate
            self.SCREEN.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Input
            if self.current_state == States.IN_WORLD:
                self.movement_keys()

            # TODO: This will be changed to check for a few things
            #  If the collided object is a trainer's vision, or
            #  If the collided object is a door or area load trigger
            if self.player_has_collided():
                self.offset_x = self.old_offset_x
                self.offset_y = self.old_offset_y

            # TODO: Abnormal walking pattern, experiment.
            if self.movement_key_pressed and pygame.time.get_ticks() % 6 == 0:
                self.player.sprite = pygame.transform.flip(self.player.sprite, True, False)

            # Checks for random battle when in bush
            if self.movement_key_pressed and self.in_bush:
                if chance_for_battle(1):
                    print(True)

            self.update_everything()

            if self.current_state == States.IN_TEXT:
                if self.current_text_box.interact(self.SCREEN, self.keys):
                    self.current_state = States.IN_WORLD

            pygame.display.update()

            if self.current_state is not States.IN_TITLE_SCREEN:
                self.seconds_counted += 1

                if self.seconds_counted == 60:
                    self.seconds_counted = 0
                    player_save_data.add_second_to_playtime()


if __name__ == '__main__':
    game = Main()
    game.main()

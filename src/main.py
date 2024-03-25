"""
    Where the game runs.
    This is where the game starts and controls player movement, ui, area loading, as well as save files.

    Lachlan Paul, 2024
"""

import pygame

import src.common.world.world_object
from player import Player
from src.common.text_box import TextBox
from src.common.trainer import Trainer, Directions
from src.common.world.bush import Bush, chance_for_battle
from src.common.world.world_object import WorldObject


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

        self.game_running = True

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
        self.troin = Trainer("d", "guy", "cock", 5, 200, 300, Directions.UP, "../assets/placeholder.jpg",
                             self.items_to_offset)
        self.bush = Bush(200, 200, 200, 26, self.SCREEN, self.items_to_offset)
        self.funny = TextBox("gheheflaefsnhfwenfweuofweuogherhguoerhgeruohgerhguerhuigheruig", "mario")

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

    def player_has_collided(self):
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
                    if self.player.hitbox.colliderect(item.hitbox.move((item.pos_x + self.offset_x, item.pos_y + self.offset_y))):
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

            self.clock.tick(60)  # Frame rate
            self.SCREEN.fill((255, 255, 255))
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Movement
            if keys[pygame.K_w]:
                self.offset_y += self.PLAYER_SPEED
                self.movement_key_pressed = True
            elif keys[pygame.K_a]:
                self.offset_x += self.PLAYER_SPEED
                self.movement_key_pressed = True
            elif keys[pygame.K_d]:
                self.offset_x -= self.PLAYER_SPEED
                self.movement_key_pressed = True
            elif keys[pygame.K_s]:
                self.offset_y -= self.PLAYER_SPEED
                self.movement_key_pressed = True

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

            self.funny.interact(self.SCREEN, keys)
            self.update_everything()

            pygame.display.update()


if __name__ == '__main__':
    game = Main()
    game.main()

"""
    Where the game runs.
    This is where the game starts and controls player movement, ui, area loading, as well as save files.

    Lachlan Paul, 2024
"""

import pygame

import src.common.world.world_object
from player import Player
from src.common.world.world_object import WorldObject


class Main:
    def __init__(self):
        pygame.init()

        self.WIDTH = 800
        self.HEIGHT = 600
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Case Creatures")

        self.player = Player()
        self.clock = pygame.time.Clock()

        self.game_running = True

        self.offset_x = 0
        self.offset_y = 0

        # The offset reverts to their old variables if there's a collision
        # Or technically, is it "if there's *going* to be a collision?"
        self.old_offset_x = self.offset_x
        self.old_offset_y = self.offset_y

        self.items_to_offset = []
        self.collidable_items = []

        self.roct = pygame.Rect(200, 150, 500, 50)
        self.thingo = WorldObject("haus", "../assets/placeholder.jpg", 50, 50, self.items_to_offset)

        self.items_to_offset.append(self.roct)

    def update_everything(self):
        """Updates the position of everything, including the player."""
        current_win_size = pygame.display.get_surface().get_size()

        self.player.draw(self.SCREEN, current_win_size[0], current_win_size[1])

        for item in self.items_to_offset:
            match type(item):
                case pygame.rect.Rect:
                    pygame.draw.rect(self.SCREEN, (255, 0, 0), item.move(self.offset_x, self.offset_y))
                case src.common.world.world_object.WorldObject:
                    item.draw(self.SCREEN, self.offset_x, self.offset_y)

    def player_has_collided(self):
        for item in self.items_to_offset:
            if type(item) is pygame.rect.Rect:
                if self.player.hitbox.colliderect(item.move((self.offset_x, self.offset_y))):
                    return True
            elif self.player.hitbox.colliderect(item.hitbox.move(self.offset_x, self.offset_y)):
                return True
        return False

    def main(self):
        while self.game_running:
            self.old_offset_x = self.offset_x
            self.old_offset_y = self.offset_y

            self.clock.tick(60)
            self.SCREEN.fill((255, 255, 255))
            keys = pygame.key.get_pressed()
            # print(round(self.clock.get_fps()))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Movement
            if keys[pygame.K_w]:
                self.offset_y += 3
            elif keys[pygame.K_a]:
                self.offset_x += 3
            elif keys[pygame.K_d]:
                self.offset_x -= 3
            elif keys[pygame.K_s]:
                self.offset_y -= 3

            # TODO: This will be changed to check for a few things
            #  If the collided object is a trainer's vision, or
            #  If the collided object is a door or area load trigger
            if self.player_has_collided():
                self.offset_x = self.old_offset_x
                self.offset_y = self.old_offset_y

            self.update_everything()

            pygame.display.flip()


if __name__ == '__main__':
    game = Main()
    game.main()

"""
    Where the game runs. This is where the game starts and controls player movement, area loading as well as save files.

    Lachlan Paul, 2024
"""

import pygame

from player import Player


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

        self.items_to_offset = []
        self.collidable_items = []

        self.roct = pygame.Rect(200, 150, 500, 50)

        self.items_to_offset.append(self.roct)

    def update_everything(self):
        for item in self.items_to_offset:
            print(type(item))

    def player_not_collided(self):
        for item in self.items_to_offset:
            if self.player.hitbox.colliderect(item.move((self.offset_x, self.offset_y))):
                print("cock")
                return True
        return False

    def main(self):
        while self.game_running:
            # The offset reverts to their old variables if there's a collision
            # Or technically, is it "if there's *going* to be a collision?"
            old_offset_x = self.offset_x
            old_offset_y = self.offset_y

            self.clock.tick(60)
            self.SCREEN.fill((255, 255, 255))
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

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
            if self.player_not_collided():
                self.offset_x = old_offset_x
                self.offset_y = old_offset_y

            self.player.draw(self.SCREEN, self.player.x, self.player.y)

            pygame.draw.rect(self.SCREEN, (255, 0, 0), self.roct.move(self.offset_x, self.offset_y))
            # update_everything(items_to_offset)
            pygame.display.flip()


if __name__ == '__main__':
    game = Main()
    game.main()

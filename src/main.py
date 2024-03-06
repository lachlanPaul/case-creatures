"""Start the game here. Contains title screen and other functions to run at game start"""

import pygame

from player import Player

from src.scenes.title import title_screen
from button import Button


def update_everything(the_list):
    for item in the_list:
        print(type(item))


def main():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Case Creatures")

    player = Player()

    clock = pygame.time.Clock()

    roct = pygame.Rect(200, 150, 5, 5)

    game_running = True

    offset_x = 0
    offset_y = 0

    items_to_offset = []

    items_to_offset.append(roct)

    while game_running:
        clock.tick(60)
        screen.fill((255, 255, 255))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Movement
        if keys[pygame.K_w]:
            offset_y += 3
        elif keys[pygame.K_a]:
            offset_x += 3
        elif keys[pygame.K_d]:
            offset_x -= 3
        elif keys[pygame.K_s]:
            offset_y -= 3

        player.draw(screen, player.x, player.y)

        pygame.draw.rect(screen, (255, 0, 0), roct.move(offset_x, offset_y))
        # update_everything(items_to_offset)
        pygame.display.flip()


if __name__ == '__main__':
    main()

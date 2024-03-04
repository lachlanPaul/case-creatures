"""Start the game here. Contains title screen and other functions to run at game start"""

import pygame

from player import Player

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Case Creatures")

player = Player()

clock = pygame.time.Clock()

game_running = True


def main():
    while game_running:
        clock.tick(60)
        screen.fill((255, 255, 255))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Movement
        if keys[pygame.K_w]:
            player.move_y(screen, -3)
        elif keys[pygame.K_a]:
            player.move_x(screen, -3)
        elif keys[pygame.K_d]:
            player.move_x(screen, 3)
        elif keys[pygame.K_s]:
            player.move_y(screen, 3)

        player.draw(screen, player.x, player.y)
        pygame.display.flip()


if __name__ == '__main__':
    main()

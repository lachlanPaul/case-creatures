"""Start the game here. Contains title screen and other functions to run at game start"""

import pygame
from button import Button

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Case Creatures")

screen.fill((120, 120, 120))

butt = Button(400, 300, 100, 100, "Cock")
butt.draw(screen)

game_running = True


def main():
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        pygame.display.flip()


if __name__ == '__main__':
    main()

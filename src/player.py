import pygame


class Player:
    def __init__(self):
        self.name = "John"
        self.sprite = pygame.image.load("../assets/placeholder.jpg")

        # By default, the player is in the centre of the screen
        self.x = 350
        self.y = 250

        self.sprite = pygame.transform.scale(self.sprite, (100, 100))

    def draw(self, screen, x, y):
        screen.blit(self.sprite, (x, y))

    def move_x(self, screen, move_by):
        self.x += move_by

    def move_y(self, screen, move_by):
        self.y += move_by

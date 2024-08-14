import pygame
from utilities import colors


class Obstacle:
    def __init__(self, map, position, size, color=colors.C_GRAY):
        self.map = map
        self.position = position
        self.size = size

        self.rect = pygame.Rect(position, size)

        # draw
        pygame.draw.rect(map, color, self.rect)

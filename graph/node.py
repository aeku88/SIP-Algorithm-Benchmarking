import pygame
from utilities import colors


class Node:
    def __init__(self, map, position, draw=True, radius=4, thickness=0, color=colors.C_BLUE):
        # initialize parameters
        self.map = map
        self.position = position
        self.parent = None
        self.children = []

        # render
        if draw:
            pygame.draw.circle(self.map, color, self.position, radius, thickness)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self
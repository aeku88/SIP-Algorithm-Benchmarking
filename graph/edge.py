import pygame
from utilities import colors


class Edge:
    def __init__(self, map, parent, child=None, child_position=None, draw=True, thickness=1, color=colors.C_BLUE):
        self.map = map
        self.parent = parent
        self.child = child

        # render
        if draw:
            if child is not None:
                pygame.draw.line(self.map, color, parent.position, child.position, thickness)
            elif child_position is not None:
                pygame.draw.line(self.map, color, parent.position, child_position, thickness)

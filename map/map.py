import pygame, random
import map.obstacle as obs
import math
from utilities import colors


class Map:
    def __init__(self, width, height, timer, grid, obstacle_count):
        self.obstacle_count = obstacle_count
        self.width = width
        self.height = height
        self.timer = timer
        self.grid = grid

        self.obstacles = []

        pygame.init()

        self.map = pygame.display.set_mode((width, height))
        self.map.fill(colors.C_WHITE)

        # create layers for proper rendering
        self.node_surface = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        self.edge_surface = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        self.obstacle_surface = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        self.ui_surface = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        self.grid_surface = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)

    def create_obstacles(self, start, size):
        obstacles = []
        while len(obstacles) < self.obstacle_count:
            random_position = (int(random.uniform(0, self.width - size[0])),
                               int(random.uniform(0, self.height - size[1])))
            rect = pygame.rect.Rect(random_position, size)

            collide_start_end = rect.collidepoint(start)
            collide_other_obstacle = False
            for other_obstacle in obstacles:
                if rect.colliderect(other_obstacle):
                    collide_other_obstacle = True
                    break

            if not collide_start_end and not collide_other_obstacle:
                obstacle = obs.Obstacle(self.obstacle_surface,
                                        random_position,
                                        size)
                obstacles.append(obstacle)
        self.obstacles.extend(obstacles)
        return obstacles

    def draw(self):
        # draw layers onto map

        self.grid.draw(self.grid_surface)
        self.map.blit(self.grid_surface, (0, 0))
        self.map.blit(self.obstacle_surface, (0, 0))
        self.map.blit(self.edge_surface, (0, 0))
        self.map.blit(self.node_surface, (0, 0))

        self.timer.draw(self.ui_surface)
        self.grid.draw_percentage(self.ui_surface)
        self.map.blit(self.ui_surface, (0, 0))

        pygame.display.update()

    def reset(self):
        self.node_surface.fill(colors.C_WHITE)

        pygame.display.update()

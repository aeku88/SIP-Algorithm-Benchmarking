import pygame, math, time
from utilities import utils, colors
from graph import edge, node
from events import Events
import utilities.analysis.graph


class RRTImproved:
    def __init__(self, map, grid, start, timer, iterations=100, color=colors.C_RED):
        self.map = map
        self.grid = grid
        self.start = start
        self.timer = timer
        self.iterations = iterations
        node.Node(self.map.node_surface, start, radius=10, thickness=1, color=colors.C_GREEN)
        self.nodes = [node.Node(self.map.node_surface, start, color=color)]

        self.on_add_node = Events()
        self.on_add_node.on_change += grid.check_collision

        self.color = color

        self.time_array = []
        self.coverage_array = []

    def nearest(self, position):
        """
        Returns the nearest node to the given node

        :param node: Node
        :return: Node
        """
        min_distance = 10000
        nearest_node = None

        for other_node in self.nodes:
            if utils.distance(other_node.position, position) < min_distance:
                min_distance = utils.distance(other_node.position, position)
                nearest_node = other_node
        return nearest_node

    def is_in_obstacle(self, position):
        obstacles = self.map.obstacles.copy()
        while len(obstacles) > 0:
            obstacle = obstacles.pop(0)
            if obstacle.rect.collidepoint(position):
                return True
        return False

    def step_improved(self, step_size, min_distance_between_nodes=20):
        can_place = False
        scaled_x, scaled_y = 0, 0
        nearest = None

        while not can_place:
            position = utils.sample_environment(self.map)
            nearest = self.nearest(position)

            delta_x, delta_y = position[0] - nearest.position[0], position[1] - nearest.position[1]
            theta = math.atan2(delta_y, delta_x)

            scaled_x, scaled_y = (int(nearest.position[0] + step_size * math.cos(theta)),
                                  int(nearest.position[1] + step_size * math.sin(theta)))

            closest_node = self.nearest((scaled_x, scaled_y))
            closest_distance = utils.distance(closest_node.position, (scaled_x, scaled_y))

            if (not self.is_in_obstacle((scaled_x, scaled_y))
                and not self.cross_obstacle((scaled_x, scaled_y), nearest.position)
                and closest_distance >= min_distance_between_nodes): can_place = True
        new_node = node.Node(self.map.node_surface, (scaled_x, scaled_y), color=self.color)

        self.on_add_node.on_change(new_node)

        self.nodes.append(new_node)
        edge.Edge(self.map.edge_surface, nearest, child=new_node, color=self.color)

    def run(self, iterations, step_size, min_distance_between_nodes=34, tick_delay=0.025,
            exit_when_done=False):
        current = 0
        self.timer.start()

        while True:
            self.time_array.append(self.timer.current_time)
            self.coverage_array.append(self.grid.get_covered_percentage())

            if current < iterations - 1:
                self.step_improved(step_size, min_distance_between_nodes)
                time.sleep(tick_delay)
                current += 1
            else:
                self.timer.stop()
                time.sleep(2)
                return self.coverage_array, self.time_array
                # pygame.quit()

                # utilities.analysis.graph.plot(self.time_array, self.coverage_array)

            self.map.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    def cross_obstacle(self, pos1, pos2):
        obstacles = self.map.obstacles.copy()
        while len(obstacles) > 0:
            obstacle = obstacles.pop(0)
            for i in range(0, 101):
                u = i / 100
                x = pos1[0] * u + pos2[0] * (1 - u)
                y = pos1[1] * u + pos2[1] * (1 - u)
                if obstacle.rect.collidepoint(x, y):
                    return True
        return False

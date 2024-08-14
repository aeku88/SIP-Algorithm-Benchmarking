from graph import node, edge
from utilities import timer, colors, utils, analysis
from events import Events
import pygame, time


class Floodfill:
    def __init__(self, map, grid, start, timer, step_size, draw_nodes=False, color=colors.C_BLACK):
        self.map = map
        self.grid = grid
        self.start = start
        self.timer = timer
        self.step_size = step_size
        self.all_nodes = [node.Node(map.map, start, True, 10, 1, colors.C_GREEN)]

        self.draw_nodes = draw_nodes

        self.on_add_node = Events()
        self.on_add_node.on_change += grid.check_collision

        self.finished = False
        self.color = color

        self.time_array = []
        self.coverage_array = []

    def step(self, queue):
        queue_local = queue.copy()

        #self.sample_nodes(self.step_size)
        if queue_local:
            parent_node = queue_local.pop(0)
            queue_local.extend(self.add_nodes(parent_node, self.step_size))
        else:
            self.timer.stop()
            time.sleep(2)
            self.finished = True

        return queue_local

    def find_nearest_node_position(self, position):
        closest_position = None
        min_distance = 100000000
        for node in self.all_nodes:
            if utils.distance(position, node.position) < min_distance:
                min_distance = utils.distance(position, node.position)
                closest_position = node.position
        return closest_position

    def add_nodes(self, parent_node, step_size):
        nodes = []

        all_directions = [(step_size, 0),  # right
                          (step_size, step_size),  # up right
                          (0, step_size),  # up
                          (-step_size, step_size),  # up left
                          (-step_size, 0),  # left
                          (-step_size, -step_size),  # down left
                          (0, -step_size),  # down
                          (step_size, -step_size)]  # down right
        for direction in all_directions:
            new_position = tuple(map(sum, zip(parent_node.position, direction)))
            if self.can_place_node(new_position):
                current_node = node.Node(self.map.node_surface,
                                         new_position,
                                         self.draw_nodes,
                                         color=self.color)
                self.all_nodes.append(current_node)
                nodes.append(current_node)
                parent_node.add_child(current_node)

                self.on_add_node.on_change(current_node)
            if (not self.is_in_obstacle(new_position)
                    and not self.cross_obstacle(new_position, parent_node.position)
                    and not self.is_out_of_bounds(new_position)):
                edge.Edge(self.map.edge_surface, parent_node, child_position=new_position, color=self.color)

        return nodes

    def run(self):
        queue = [node.Node(self.map.map, self.start, color=self.color)]
        self.timer.start()

        while True:
            if self.finished:
                return self.coverage_array, self.time_array
            self.time_array.append(self.timer.current_time)
            self.coverage_array.append(self.grid.get_covered_percentage())

            queue = self.step(queue)
            self.map.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    def can_place_node(self, new_position):
        return (self.is_new_node(new_position)
                and not self.is_out_of_bounds(new_position)
                and not self.is_in_obstacle(new_position))

    def is_new_node(self, new_position):
        unique = True
        for node in self.all_nodes:
            if node.position == new_position:
                unique = False
        return unique

    def is_out_of_bounds(self, new_position):
        return (new_position[0] > self.map.map.get_size()[0]
                or new_position[0] < 0
                or new_position[1] > self.map.map.get_size()[1]
                or new_position[1] < 0)

    def is_in_obstacle(self, new_position):
        obstacles = self.map.obstacles
        for obstacle in obstacles:
            if obstacle.rect.collidepoint(new_position):
                return True
        return False

    def probe_obstacles(self, position, direction):
        obstacles = self.map.obstacles.copy()
        end_point = tuple(map(sum, zip(position, direction)))
        current_probe_point = None

        while len(obstacles) > 0:
            obstacle = obstacles.pop(0)
            for i in range(0, 101):
                u = i / 100
                last_probe_point = current_probe_point
                current_probe_point = position[0] * u + end_point[0] * (1 - u), position[1] * u + end_point[1] * (1 - u)

                if obstacle.rect.collidepoint(current_probe_point):
                    return last_probe_point
        return end_point

    def cross_obstacle(self, pos1, pos2):
        obs = self.map.obstacles.copy()
        while len(obs) > 0:
            obstacle = obs.pop(0)
            for i in range(0, 101):
                u = i / 100
                x = pos1[0] * u + pos2[0] * (1 - u)
                y = pos1[1] * u + pos2[1] * (1 - u)
                if obstacle.rect.collidepoint(x, y):
                    return True
        return False


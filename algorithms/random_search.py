import pygame, random, time
from utilities import colors, analysis
from graph import edge, node
from events import Events


class RandomSearch:
    def __init__(self, map, grid, start, timer, color=colors.C_BLUE):
        self.map = map
        self.grid = grid
        self.start = start
        self.timer = timer

        node.Node(map.map, start, True, 10, 1, colors.C_GREEN)
        self.all_nodes = [node.Node(map.map, start)]

        self.on_add_node = Events()
        self.on_add_node.on_change += grid.check_collision

        self.color = color

        self.time_array = []
        self.coverage_array = []

    def step(self, min_step_size, max_step_size):
        can_place = False

        while not can_place:
            step_size = random.randint(min_step_size, max_step_size)
            all_directions = [(step_size, 0),  # right
                              (step_size, step_size),  # up right
                              (0, step_size),  # up
                              (-step_size, step_size),  # up left
                              (-step_size, 0),  # left
                              (-step_size, -step_size),  # down left
                              (0, -step_size),  # down
                              (step_size, -step_size)]  # down right
            rand_index = random.randint(0, 7)

            new_position = tuple(map(sum, zip(self.all_nodes[-1].position, all_directions[rand_index])))
            if self.can_place_node(new_position) and not self.cross_obstacle(self.all_nodes[-1].position, new_position):
                can_place = True
        new_node = node.Node(self.map.node_surface,
                             new_position,
                             color=self.color)
        edge.Edge(self.map.edge_surface, self.all_nodes[-1], child=new_node, color=self.color)
        self.all_nodes.append(new_node)

        self.on_add_node.on_change(new_node)

        self.time_array.append(self.timer.current_time)
        self.coverage_array.append(self.grid.get_covered_percentage())

    def run(self, iterations, min_step_size, max_step_size, tick_delay=0.025,
            exit_when_done=False):
        current = 0
        self.timer.start()

        while True:
            if current < iterations - 1:
                self.step(min_step_size, max_step_size)
                time.sleep(tick_delay)
                current += 1
            else:
                self.timer.stop()
                time.sleep(2)
                return self.coverage_array, self.time_array

            self.map.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    def can_place_node(self, new_position):
        return (not self.is_out_of_bounds(new_position)
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
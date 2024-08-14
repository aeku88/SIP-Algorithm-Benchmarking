import pygame

import utilities.colors
from map import map as m, grid as g
from algorithms import rrt_improved, random_search, floodfill
from utilities import timer
from utilities import analysis


def main():
    start = (50, 50)
    obstacle_size = (40, 40)
    map_size = (1344, 756)

    grid = g.Grid(map_size[0], map_size[1], False)
    main_timer = timer.Timer((1196, 706))

    map = m.Map(map_size[0], map_size[1], main_timer, grid, obstacle_count=40)
    map.create_obstacles(start, obstacle_size)

    pygame.display.set_caption('Algorithms')

    random_search_results = random_search.RandomSearch(map, grid, start, main_timer).run(1500, 35, 35, 0)

    map = m.Map(map_size[0], map_size[1], main_timer, grid, obstacle_count=40)
    map.create_obstacles(start, obstacle_size)
    grid.reset()

    floodfill_results = floodfill.Floodfill(map, grid, start, main_timer, 35, draw_nodes=True).run()

    map = m.Map(map_size[0], map_size[1], main_timer, grid, obstacle_count=40)
    map.create_obstacles(start, obstacle_size)
    grid.reset()

    rrt_results = rrt_improved.RRTImproved(map, grid, start, main_timer, color=utilities.colors.C_GREEN).run(1500, 35, 0, 0)

    map = m.Map(map_size[0], map_size[1], main_timer, grid, obstacle_count=40)
    map.create_obstacles(start, obstacle_size)
    grid.reset()

    rrt_improved_results = rrt_improved.RRTImproved(map, grid, start, main_timer, color=utilities.colors.C_RED).run(900, 35,
                                                                                                             25, 0)
    pygame.quit()

    analysis.graph.plot(rrt_improved_results, rrt_results, random_search_results, floodfill_results)


if __name__ == '__main__':
    main()

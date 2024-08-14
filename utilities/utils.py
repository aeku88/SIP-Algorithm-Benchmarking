import math, random

def distance(pos1, pos2):
    return math.hypot(pos1[0] - pos2[0],
                      pos1[1] - pos2[1])


def sample_environment(map):
    """
    Returns a randomly sampled point on the map

    :param map: Map
    :return: tuple
    """
    return int(random.uniform(0, map.width)), int(random.uniform(0, map.height))

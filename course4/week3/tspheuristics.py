"""
Copyright 2020 Dave Huh
Heuristics for Traveling Salesman Problem instead of exact
algorithm
"""

import sys
import numpy as np
import math

from itertools import combinations


class TravelingSalesmanHeuristics:
    """
    Computes shortest distance for the traveling
    salesman problem using a heuristics
    """
    def __init__(self, cities):
        self.cities = cities

    def precompute_all_pair_distances(self):
        """
        Compute all combinations of pairwise distances and stores to dictionary
        """
        cities_keys = self.cities[:,0]
        combinations_city_pairs = combinations(cities_keys, 2)

        combo_array = np.array(list(combinations_city_pairs))
        distances = np.vectorize(self.compute_distance_between_two_cities)(combo_array[:, 0],
                                                                             combo_array[:, 1])
        distances = distances.reshape((distances.shape[0], 1))

        combo_array = np.hstack((combo_array, distances))

        return combo_array

    def compute_distance_between_two_cities(self, city1_key, city2_key):
        """
        Compute squared Eucledean distance between two points
        """
        city1_idx = int(city1_key) - 1
        city2_idx = int(city2_key) - 1

        city1 = self.cities[city1_idx]
        city2 = self.cities[city2_idx]

        x1 = city1[1]
        y1 = city1[2]

        x2 = city2[1]
        y2 = city2[2]

        return (x1 - x2)**2 + (y1 - y2)**2


def compute_minimum_TSP(paths):
    """
    Computes minimum TSP
    """
    visited_vertices = dict()
    total_squared_distance = 0

    paths = paths[np.argsort(paths[:,2])]
    paths[:, 2] = np.vectorize(np.sqrt)(paths[:, 2])
    starting_paths = paths[paths[:,0] == 1]
    remaining_paths = paths[paths[:, 0] != 1]

    first_path = starting_paths[0,:]
#    print('starting path:', first_path)
#    print('original remaining paths:\n', remaining_paths)
    next_starting_point = first_path[1]
#    print('first next starting point:', next_starting_point)
    visited_vertices.update(dict.fromkeys(first_path[:2]))
    total_squared_distance += first_path[2]

    while len(remaining_paths) > 0:
        next_path_mask = False
        next_path = []
        next_path_mask = ((remaining_paths[:, 0] == next_starting_point) | \
            (remaining_paths[:, 1] == next_starting_point)) & \
            (
                ~np.isin(remaining_paths[:, 0], list(visited_vertices), assume_unique=True) | \
                ~np.isin(remaining_paths[:, 1], list(visited_vertices), assume_unique=True)
            )

        next_paths = remaining_paths[next_path_mask]

        next_path = next_paths[0,:]

        visited_vertices.update(dict.fromkeys(next_path[:2]))
        total_squared_distance += next_path[2]

        if next_path[1] in visited_vertices:
            next_starting_point = next_path[0]
        else:
            next_starting_point = next_path[1]

        remaining_path_mask = ~np.isin(remaining_paths[:, 0], list(visited_vertices), assume_unique=True) | \
            ~np.isin(remaining_paths[:, 1], list(visited_vertices), assume_unique=True)
#         print("visited:", visited_vertices)
#         print("remaining paths:\n", remaining_paths)
#         print('remaining mask\n', remaining_path_mask)
        remaining_paths = remaining_paths[remaining_path_mask]
#            print('remaining paths:\n', remaining_paths)

#        else:
#            print('here')
#            next_path = remaining_paths[:]
#            visited_vertices.update(dict.fromkeys(next_path[:2]))
#            total_squared_distance += next_path[2]
#            remaining_paths = []


    next_starting_point = list(visited_vertices)[-1]
#    print("last key: ", next_starting_point)
    final_path_to_start = paths[(paths[:,0] == 1) & (paths[:, 1] == next_starting_point)][0]
    total_squared_distance += final_path_to_start[2]

#    print(visited_vertices)
#    return math.floor(math.sqrt(total_squared_distance))
    return math.floor(total_squared_distance)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 tspheuristics.py <file name>")
        sys.exit(1)

    file = open(sys.argv[1])
    cities = file.read().splitlines()

    file.close()

    cities = [row.split(' ') for row in cities]
    cities = [list(map(float, row)) for row in cities]
    num_cities = int(cities.pop(0)[0])

    cities = np.array(cities)

    tsp = TravelingSalesmanHeuristics(cities)
    paths_combinations = tsp.precompute_all_pair_distances()

    min_dist = compute_minimum_TSP(paths_combinations)
    print('min_dist:', min_dist)

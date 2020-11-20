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
    def __init__(self, cities, num_cities):
        self.cities = cities
        self.num_cities = num_cities
        self.visited_vertices = {}

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

    def compute_path_combinations(self, starting_point, remaining_cities: set):
        """
        Compute all combinations of pairwise distances and stores to dictionary
        """
        cities_keys = remaining_cities
        cities_keys.add(starting_point)
        raw_combos = combinations(cities_keys, 2)
        combinations_city_pairs = [combo for combo in raw_combos \
            if combo[0] == starting_point or combo[1] == starting_point]

        combo_array = np.array(combinations_city_pairs)
        distances = np.vectorize(self.compute_distance_between_two_cities)(combo_array[:, 0],
                                                                             combo_array[:, 1])
        distances = distances.reshape((distances.shape[0], 1))

        combo_array = np.hstack((combo_array, distances))
        combo_array = combo_array[np.argsort(combo_array[:, 2])]

        return combo_array

    def compute_minimum_TSP(self):
        """
        Computes minimum TSP
        """
        total_squared_distance = 0
        next_starting_point = 1
        vertices_to_visit = set(list(range(1, self.num_cities + 1)))

        paths = self.compute_path_combinations(next_starting_point,
                                               vertices_to_visit)

        first_path = paths[0,:]
        first_path[2] = math.sqrt(first_path[2])

        next_starting_point = first_path[1]
        self.visited_vertices.update(dict.fromkeys(first_path[:2]))
        vertices_to_visit -= self.visited_vertices.keys()
        total_squared_distance += first_path[2]

        while len(self.visited_vertices) < self.num_cities:
            next_path_mask = False
            next_path = []

            next_paths = self.compute_path_combinations(next_starting_point,
                                                        vertices_to_visit)
            next_path_mask = (
                (
                    ~np.isin(next_paths[:, 1], list(self.visited_vertices))
                )
                | \
                (
                    ~np.isin(next_paths[:, 0], list(self.visited_vertices))
                )
            )

            next_paths = next_paths[next_path_mask]
            next_path = next_paths[0,:]
            next_path[2] = math.sqrt(next_path[2])

            if next_path[1] in self.visited_vertices:
                next_starting_point = next_path[0]
            else:
                next_starting_point = next_path[1]

            self.visited_vertices.update(dict.fromkeys(next_path[:2]))
            total_squared_distance += next_path[2]

            vertices_to_visit -= self.visited_vertices.keys()

        next_starting_point = list(self.visited_vertices)[-1]
        final_dist = math.sqrt(self.compute_distance_between_two_cities(1, next_starting_point))
        total_squared_distance += final_dist
        print("final path:", next_starting_point, 'to', 1)
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

    tsp = TravelingSalesmanHeuristics(cities, num_cities)

    min_dist = tsp.compute_minimum_TSP()
    print('min_dist:', min_dist)

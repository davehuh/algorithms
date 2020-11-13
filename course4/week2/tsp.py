"""
Copyright 2020 Dave Huh
Traveling salesman problem for special case of small vertices
"""

import sys
import math
import numpy as np

from numba import jit

class City:
    def __init__(self, coordinate_list):
        self.x = coordinate_list[0]
        self.y = coordinate_list[1]


class Traveling_Salesman:
    """
    Traveling salesman algorithm
    Assumes each city is visited once
    """
    def __init__(self, cities_list: list, num_cities: int):
        self.cities_list = cities_list
#        self.ref_matrix = np.full((num_cities + 1, num_cities + 1), np.inf)
        self.ref_matrix = np.zeros((num_cities + 1, num_cities + 1))

    def build_cities_list(self):
        """
        Build list of City object from raw list
        """
        cities = []

        for city in self.cities_list:
            cities.append(City(city))

        self.cities_list = cities

        return self.cities_list

#@jit(nopython=True)
def compute_minimum_dist(source, ref_matrix, num_cities, cities_list):
    """
    Calculates minimum TSP
    """
    if source == 1:
        ref_matrix[source, 1] = 0
    else:
        ref_matrix[source, 1] = np.inf

    global_min_dist = np.inf

    num_cities = num_cities + 1
    for subproblem_size_m in range(2, num_cities):
        set_s = list(range(1, subproblem_size_m + 1))

        for destination_j in set_s:
            if destination_j == 1:
                continue

            city_j = cities_list[destination_j-1]

            for pen_ult_dest_k in set_s:
                if pen_ult_dest_k != destination_j:
                    city_k = cities_list[pen_ult_dest_k-1]
                    cost_k_j = compute_distance(city_k, city_j)

                    ref_matrix[source, destination_j] = \
                        min(ref_matrix[source - destination_j, pen_ult_dest_k] + cost_k_j,
                            ref_matrix[source, destination_j])

            city_1 = cities_list[0]
            cost_j_1 = compute_distance(city_1, city_j)

            global_min_dist = min(global_min_dist,
                                  ref_matrix[1, destination_j] + cost_j_1)
            global_min_dist = min(global_min_dist,
                                  ref_matrix[subproblem_size_m, destination_j] + cost_j_1)

    return global_min_dist


def compute_distance(city_1, city_2):
    """
    Computes Cartegian distance between two 2-D points
    """
    x_1 = city_1[0]
    y_1 = city_1[1]

    x_2 = city_2[0]
    y_2 = city_2[1]

    dist = math.sqrt((x_1-x_2)**2 + (y_1-y_2)**2)
    return dist


if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 tsp.py <file name>")
        sys.exit(1)

    file = open(sys.argv[1])
    vertices = file.read().splitlines()
    file.close()

    vertices = [row.split(' ') for row in vertices]
    vertices = [list(map(float, row)) for row in vertices]

    num_vertices = int(vertices.pop(0)[0])

    ts = Traveling_Salesman(vertices, num_vertices)
#    cities_list = ts.build_cities_list()
    ref_matrix = ts.ref_matrix

    minimum_dist = np.inf
#    for city in range(1, num_vertices+1):
#        minimum_dist = min(minimum_dist,
#                           compute_minimum_dist(city, ref_matrix, num_vertices, vertices))
    minimum_dist = compute_minimum_dist(1, ref_matrix, num_vertices, vertices)

    city_1 = vertices[0]
    cumulated_dist = 0

    for city_idx in range(2, num_vertices+1):
        if city_idx > 2:
            city_1 = vertices[city_idx - 2]
        city_dest = vertices[city_idx - 1]

        cumulated_dist += compute_distance(city_1, city_dest)

    print("check dist: ", cumulated_dist)
    print("answer: ", minimum_dist)

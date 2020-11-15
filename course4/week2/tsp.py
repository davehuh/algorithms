"""
Copyright 2020 Dave Huh
Traveling salesman problem for special case of small vertices
"""

import sys
import math
import numpy as np

from numba import jit
from itertools import combinations


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

def set_generator(source, budget_size, num_cities):
    iterable = range(1, num_cities)
    sets = combinations(iterable, budget_size)

    final_sets = []

    for a_set in sets:
        if source in a_set:
            final_sets.append(a_set)

    return final_sets

def generate_all_sets(source, num_cities):
    sets = []
    budgets = range(1, num_cities)

    for budget in budgets:
        sets.extend(set_generator(source, budget, num_cities))

    print(sets)
    return sets


def compute_num_sets(source, num_cities):
    num_sets = 0
    budgets = range(1, num_cities)

    for budget in budgets:
        num_sets += len(set_generator(source, budget, num_cities))

    return num_sets

#@jit(nopython=True)
def compute_minimum_dist(source, num_cities, cities_list):
    """
    Calculates minimum TSP
    """
    num_cities += 1
    sets = generate_all_sets(source, num_cities)
    num_sets = len(sets)
    ref_matrix = np.zeros((num_sets, num_cities))
    ref_matrix[:, source] = np.inf
    ref_matrix[source, source] = 0

    global_min_dist = np.inf

    set_idx = 0
    for budget_size_m in range(2, num_cities):
        sets = set_generator(source, budget_size_m, num_cities)
        print("budget: ", budget_size_m)
        print(sets)

        for set_s in sets:
            for destination_j in set_s:
                if destination_j == source:
                    continue

                city_j = cities_list[destination_j-1]

                for pen_ult_dest_k in set_s:
                    if pen_ult_dest_k != destination_j:
                        city_k = cities_list[pen_ult_dest_k-1]
                        cost_k_j = compute_distance(city_k, city_j)

                        #  TODO path idx logic needs more thought
                        path_s_k = pen_ult_dest_k
                        shortest_path_source_to_k = ref_matrix[destination_j, pen_ult_dest_k]

                        ref_matrix[source, destination_j] = \
                            min(shortest_path_source_to_k + cost_k_j,
                                ref_matrix[source, destination_j])

            set_idx += 1
#                city_1 = cities_list[0]
#                cost_j_1 = compute_distance(city_1, city_j)

    #            global_min_dist = min(global_min_dist,
    #                                  ref_matrix[1, destination_j] + cost_j_1)
    #            global_min_dist = min(global_min_dist,
    #                                  ref_matrix[subproblem_size_m, destination_j] + cost_j_1)

    print("matrix: \n", ref_matrix)
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

#    ts = Traveling_Salesman(vertices, num_vertices)
#    ref_matrix = ts.ref_matrix

    minimum_dist = np.inf

#    for city in range(1, num_vertices+1):
#        minimum_dist = min(minimum_dist,
#                           compute_minimum_dist(city, ref_matrix, num_vertices, vertices))
    minimum_dist = compute_minimum_dist(1, num_vertices, vertices)
#
#    print("answer: ", minimum_dist)

#    city_1 = vertices[0]
#    cumulated_dist = 0
#
#    for city_idx in range(2, num_vertices+1):
#        if city_idx > 2:
#            city_1 = vertices[city_idx - 2]
#        city_dest = vertices[city_idx - 1]
#
#        cumulated_dist += compute_distance(city_1, city_dest)
#
#    print("check dist: ", cumulated_dist)

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

    return sets

def generate_key_without_j(orig_key, remove_j):
    output_key = list(orig_key)
    output_key.remove(remove_j)
    return tuple(output_key)

#@jit(nopython=True)
def compute_minimum_dist(source, num_cities, cities_list):
    """
    Calculates minimum TSP
    """
    num_cities += 1
    sets = generate_all_sets(source, num_cities)
#    print(sets)
    num_sets = len(sets)

    set_key_indices_dict = {k: v for v, k in enumerate(sets)}

#    ref_matrix = np.zeros((num_sets, num_cities))
    ref_matrix = np.full((num_sets, num_cities), np.inf)
    ref_matrix[:, source] = np.inf
    ref_matrix[source, source] = 0

    global_min_dist = np.inf
    city_source = cities_list[source-1]

    for set_s in sets:
#        print("\n path:", set_s)
        set_s_idx = set_key_indices_dict[set_s]
#        print("set idx:", set_s_idx)
        # base case
        if len(set_s) == 1:
            dest = set_s[0]
            ref_matrix[set_s_idx, dest] = 0


        for destination_j in set_s:
            if destination_j == source:
                continue

            city_j = cities_list[destination_j-1]

            set_key_without_j = generate_key_without_j(set_s, destination_j)
            set_to_k_idx = set_key_indices_dict[set_key_without_j]
#            print("path w/o j:", set_key_without_j, "idx:", set_to_k_idx)

            tmp_min = np.inf
            for pen_ult_dest_k in set_s:
                #  TODO check if condition statement
                if pen_ult_dest_k != destination_j:
                    city_k = cities_list[pen_ult_dest_k-1]
                    cost_k_j = compute_distance(city_k, city_j)
#                    print("k:", pen_ult_dest_k,
#                          "j:" , destination_j,
#                          " cost k to j: ", cost_k_j)

                    #  TODO path idx logic needs more thought
                    shortest_path_source_to_k = ref_matrix[set_to_k_idx, pen_ult_dest_k]

#                    print("dist to k: ", shortest_path_source_to_k)

                    tmp_min = min(shortest_path_source_to_k + cost_k_j, tmp_min)
#                    print("tmp min ", tmp_min)

            ref_matrix[set_s_idx, destination_j] = tmp_min

            if set_s_idx == ref_matrix.shape[0] - 1 and \
                    destination_j != source:
                cost_j_source = compute_distance(city_source, city_j)
                print(cost_j_source)
                global_min_dist = min(global_min_dist,
                                      tmp_min + cost_j_source)

    print("matrix: \n", ref_matrix)
    return math.floor(global_min_dist)


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

    print("answer: ", minimum_dist)

#    for city_idx in range(2, num_vertices+1):
#        if city_idx > 2:
#            city_1 = vertices[city_idx - 2]
#        city_dest = vertices[city_idx - 1]
#
#        cumulated_dist += compute_distance(city_1, city_dest)
#
#    print("check dist: ", cumulated_dist)

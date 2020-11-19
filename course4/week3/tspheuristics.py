"""
Copyright 2020 Dave Huh
Heuristics for Traveling Salesman Problem instead of exact
algorithm
"""

import sys
import numpy as np
import math


def compute_distance_between_two_cities(city1, city2):
    """
    Compute Eucledean distance between two points
    """
    x1 = city1[1]
    y1 = city1[2]

    x2 = city2[1]
    y2 = city2[2]

    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


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
    cities[:, 0] = np.floor(cities[:, 0])

"""
Copyright 2020 Dave Huh
Solves knapsack problem
"""

import sys
import numpy as np


class KnapSack:
    """
    Solves knapsack problem
    """
    def __init__(self, value_weights, size):
        self.size = size
        self.vw = np.array(value_weights)
        self.matrix = np.zeros((len(value_weights), size + 1), dtype=int)

        self.case1 = 0
        self.case2 = 0
        self.lookup = {}

        self.capacity = np.zeros(size + 1)

    def _get_max(self, index, weight):
        """
        returns max value given index of object in self.vw
        """
        value_i = self.vw[index, 0]
        weight_i = self.vw[index, 1]
        case_1_val = self.matrix[index-1, weight]

        case_2_val = 0
        if weight > weight_i:
            case_2_val = self.matrix[index-1, weight - weight_i] + value_i

        if case_1_val > case_2_val:
            return case_1_val
        return case_2_val

    def compute_max_value(self):
        """
        Computes maximum value and within capacity of the knapsack size
        """
        for value in range(1, len(self.vw)):
            for weight in range(self.size + 1):
                self.matrix[value, weight] = self._get_max(value, weight)

        return self.matrix[-1, -1]

    def _sort_vw(self):
        """
        Sorts value weight list by increasing weight
        """
        self.vw = self.vw[np.argsort(self.vw[:, 1])]

    def _get_max_optimal(self, index, capacity):
        """
        returns max value using minimal caching
        """

        # num 4
        if (index, capacity) in self.lookup:
            return self.lookup[(index, capacity)]

        value_i = self.vw[index, 0]
        weight_i = self.vw[index, 1]

        # num 5
        if weight_i > capacity:
            self.lookup[(index, capacity)] = 0
            return 0

        # num 6
        if index == len(self.vw) - 1:
            self.lookup[(index, capacity)] = value_i
            return value_i

        if index == 0:
            self.lookup[(index, capacity)] = 0
            return value_i

        # num 7
        case_1_val = self._get_max_optimal(index-1, weight_i)
        case_2_val = self._get_max_optimal(index-1, capacity - weight_i) + value_i

        if case_1_val > case_2_val:
            self.lookup[(index, capacity)] = case_1_val
            return case_1_val

        self.lookup[(index, capacity)] = case_2_val
        return case_2_val

    def compute_max_optimal(self):
        self._sort_vw()

        maxVal = 0
        currVal = 0
        for item in range(1, len(self.vw)):
            for weight in range(self.size + 1):
                currVal = self._get_max_optimal(item, weight)
                if currVal > maxVal:
                    maxVal = currVal

        return maxVal


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 knapsack.py <file_name>")
        sys.exit(1)

    file = open(sys.argv[1])
    file = file.read().splitlines()

    value_weight_list = [row.split(' ') for row in file]

    value_weight_list = [list(map(int, row)) for row in value_weight_list]

    knapsack_size, number_of_items = value_weight_list.pop(0)

    print("knapsack size: ", knapsack_size)
    print("num items: ", number_of_items)

    knapsack = KnapSack(value_weight_list, knapsack_size)

    print("iterative: ", knapsack.compute_max_value())
#    print(knapsack.matrix)
#    print(np.sum(knapsack.matrix[0,:]))

    print("optimal: ", knapsack.compute_max_optimal())
#    print(knapsack.capacity)

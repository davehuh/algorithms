"""
Copyright 2020 Dave Huh
Solves knapsack problem
"""

import sys



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 knapsack.py <file_name>")
        sys.exit(1)


    file = open(sys.argv[1])
    file = file.read().splitlines()

    value_weight_list = [row.split(' ') for row in file]

    value_weight_list = [list(map(int, row)) for row in value_weight_list]

    knapsack_size, number_of_items = value_weight_list.pop(0)

    print(knapsack_size)
    print(value_weight_list)

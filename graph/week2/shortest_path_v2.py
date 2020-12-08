"""
Copyright 2020 Dave Huh
Shortest path using Dijkstra's algorithm
"""

import sys
import threading
import heapq

def read_file(file_name):
    """
    build adjacency list
    """
    if len(sys.argv) != 2:
        print("Usage: python3 shortest_path_v2.py <file name>")
        sys.exit(1)

    file = open(file_name, 'r')
    a_list = file.readlines()
    file.close()

    a_list = [row.strip().split('\t') for row in a_list]

    for l_idx, line in enumerate(a_list):
        for e_idx, ele in enumerate(line):
            if e_idx == 0:
                a_list[l_idx][e_idx] = int(ele)
                continue
            a_list[l_idx][e_idx] = tuple(map(int, ele.strip().split(',')))
    return a_list


def shortest_path(source, dest):
    """
    find shortest path dist
    """
    dist = 0

    return dist


def main():
    """
    main
    """

    adjacency_list = read_file(sys.argv[1])

    source = 1
    dest_list = [7,37,59,82,99,115,133,165,188,197]
    distances = []

    for idx, vertex in enumerate(dest_list):
        print("progress:", idx+1, '/', len(dest_list))
        distances.append(shortest_path(source, vertex))

    print(distances)


if __name__ == "__main__":
    STACK_SIZE = 67108864
    RECURSION_LIMIT = 2**20

    threading.stack_size(STACK_SIZE)
    sys.setrecursionlimit(RECURSION_LIMIT)

    thread = threading.Thread(target=main)
    thread.start()

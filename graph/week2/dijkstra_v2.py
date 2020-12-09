"""
Copyright 2020 Dave Huh
Dijkstra's algorithm to find minimum cost shortest path
"""

import sys
import threading
from collections import defaultdict
from heapq import heappop, heappush

def build_graph(file_name):
    """
    build graph
    :param file_name: path to input file
    :return: graph dict which has node and values of head cost tuples
    """
    graph = defaultdict(list)

    with open(file_name) as f:
        for line in f:
            line = line.strip().split()
            node = int(line[0])
            heads = [int(ele.split(',')[0]) for ele in line[1:]]
            costs = [int(ele.split(',')[1]) for ele in line[1:]]
            graph[node] = [(head, cost) for head, cost in zip(heads, costs)]

    return graph

def main():
    """
    main
    """
    if len(sys.argv) != 2:
        print("Usage: python3 dijkstra_v2.py <file name>")
        sys.exit(1)

    graph = build_graph(sys.argv[1])

if __name__ == "__main__":
    STACK_SIZE = 67108864
    RECURSION_LIMIT = 2**20

    threading.stack_size(STACK_SIZE)
    sys.setrecursionlimit(RECURSION_LIMIT)
    thread = threading.Thread(target=main)
    thread.start()

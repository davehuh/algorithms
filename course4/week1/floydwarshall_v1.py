"""
Copyright 2020 Dave Huh
All minimum paths problem solved with Floyd-Warshall algorithm
Optimized for memory
"""

from collections import defaultdict
from numba import jit

import sys
import threading
import numpy as np

def build_graph(file_path):
    """
    build graph
    """
    graph, graph_rev, nodes = defaultdict(list), defaultdict(list), set()
    num_nodes = 0
    num_edges = 0

    with open(file_path, "r") as file:
        for line in file:
            line = list(map(int, line.strip().split()))

            if len(line) == 2:
                num_nodes = line[0]
                num_edges = line[1]
                continue

            tail = line[0]
            head = line[1]
            cost = line[2]

            graph[tail].append((cost, head))
            graph_rev[head].append((cost, tail))
            nodes.add(tail)
            nodes.add(head)

    return graph, graph_rev, nodes, num_nodes, num_edges


def find_all_points_shortest_paths():
    """
    find all points shortest paths
    """
    global GRAPH, GRAPH_REV, NODES, NUM_NODES, NUM_EDGES, MATRIX_COST, MATRIX_PATH

    MATRIX_COST = np.full((len(NODES), len(NODES), 2), np.inf)


def main():
    """
    main
    """
    global GRAPH, GRAPH_REV, NODES, NUM_NODES, NUM_EDGES
    GRAPH, GRAPH_REV, NODES, NUM_NODES, NUM_EDGES = build_graph(sys.argv[1])

    find_all_points_shortest_paths()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 floydwarshall_v1.py <file path>")
        sys.exit(1)

    threading.stack_size(67180864)
    sys.setrecursionlimit(10**6)

    thread = threading.Thread(target=main)
    thread.start()

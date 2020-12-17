"""
Copyright 2020 Dave Huh
All minimum paths problem solved with Floyd-Warshall algorithm
Optimized for memory
"""

from collections import defaultdict
from numba import jit
from tqdm import tqdm

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


def initialize_matrices():
    """
    initialize matrices
    """
    global MATRIX_COST, MATRIX_PATH, GRAPH

    MATRIX_COST = np.full((2, len(NODES), len(NODES)), np.inf)
    MATRIX_PATH = [[[[] for _ in range(len(NODES))] for _ in range(len(NODES))] for _ in range(2)]

    # i == j
    np.fill_diagonal(MATRIX_COST[0,:,:], 0)
    np.fill_diagonal(MATRIX_COST[1,:,:], 0)

    # i to j edge in (E)xists
    for tail in GRAPH:
        tail_idx = tail - 1
        for cost, head in GRAPH[tail]:
            head_idx = head - 1

            if not MATRIX_COST[0, tail_idx, head_idx] or \
                    cost < MATRIX_COST[0, tail_idx, head_idx]:
                MATRIX_COST[0, tail_idx, head_idx] = cost
                MATRIX_PATH[0][tail_idx][head_idx] = [tail, head]


def assign_current_cost_path_for_node(visited, curr_budget_idx, prev_budget_idx,
                                      tail_idx, head_idx):
    """
    Assign minimum cost and path to head node
    """
    global GRAPH_REV, MATRIX_COST, MATRIX_PATH

    prev_cost = MATRIX_COST[prev_budget_idx, tail_idx, head_idx]
    prev_path = MATRIX_PATH[prev_budget_idx][tail_idx][head_idx]

    cost_node_pairs = GRAPH_REV.get(head_idx+1, [])

    min_cost = np.inf  # cost from penultimate node to head
    min_node = tail_idx + 1 # penultimate node that yield min cost

    for cost_node in cost_node_pairs:
        if not cost_node:
            break
        cost = cost_node[0]
        node = cost_node[1]
        if node not in visited:
            continue

        if cost < min_cost:
            min_cost = cost
            min_node = node

    alt_cost = MATRIX_COST[prev_budget_idx, tail_idx, min_node-1] + min_cost
    alt_path = MATRIX_PATH[prev_budget_idx][tail_idx][min_node-1] + [head_idx+1]

    if alt_cost < prev_cost:
        MATRIX_COST[curr_budget_idx, tail_idx, head_idx] = alt_cost
        MATRIX_PATH[curr_budget_idx][tail_idx][head_idx] = alt_path
    else:
        MATRIX_COST[curr_budget_idx, tail_idx, head_idx] = prev_cost
        MATRIX_PATH[curr_budget_idx][tail_idx][head_idx] = prev_path

    min_path = MATRIX_PATH[curr_budget_idx][tail_idx][head_idx]

    if min_path and min_path[0] != tail_idx+1:
        MATRIX_PATH[curr_budget_idx][tail_idx][head_idx] = [tail_idx+1] + \
            MATRIX_PATH[curr_budget_idx][tail_idx][head_idx]


def recycle_matrices(tail_idx, curr_budget_idx, prev_budget_idx):
    """
    Recycle matrix to save memory
    """
    global MATRIX_COST, MATRIX_PATH

    MATRIX_COST[prev_budget_idx, tail_idx, :] = MATRIX_COST[curr_budget_idx, tail_idx, :]
    MATRIX_PATH[prev_budget_idx][tail_idx][:] = MATRIX_PATH[curr_budget_idx][tail_idx][:]



# TODO numba optimization
#@jit(nopython=True)
def find_all_points_shortest_paths():
    """
    find all points shortest paths
    Using Floyd-Warshall algorithm
    """
    global GRAPH, GRAPH_REV, NODES, NUM_NODES, NUM_EDGES, MATRIX_COST, MATRIX_PATH

    prev_budget_idx = 0
    curr_budget_idx = 1

    neg_cycle_checksum = 0
    minimum_cost = 0
    for budget_idx in tqdm(range(NUM_NODES)):  # delete tqdm to be numba compatible
        for tail_idx in range(NUM_NODES):
            visited = set([tail_idx+1])
            for head_idx in range(NUM_NODES):
                visited.add(head_idx+1)

                assign_current_cost_path_for_node(visited, curr_budget_idx, prev_budget_idx,
                                      tail_idx, head_idx)

            recycle_matrices(tail_idx, curr_budget_idx, prev_budget_idx)


def main():
    """
    main
    """
    global GRAPH, GRAPH_REV, NODES, NUM_NODES, NUM_EDGES, MATRIX_PATH, MATRIX_COST

    GRAPH, GRAPH_REV, NODES, NUM_NODES, NUM_EDGES = build_graph(sys.argv[1])

    initialize_matrices()
    find_all_points_shortest_paths()

    print("COST MATRIX:\n", MATRIX_COST[1, :, :])
    print("PATH MATRIX:\n", np.array(MATRIX_PATH[1], dtype=list))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 floydwarshall_v1.py <file path>")
        sys.exit(1)

    threading.stack_size(67180864)
    sys.setrecursionlimit(10**6)

    thread = threading.Thread(target=main)
    thread.start()

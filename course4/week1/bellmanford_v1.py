"""
Bellman-Ford algorithm
"""

import sys
import numpy as np
import threading

from collections import defaultdict
from heapq import heapify


def build_graph(file_path):
    """
    build graph from file
    :param file_path: path to input file
    :return graph: a dict graph
    :return graph_rev: graph with edges reversed
    :return nodes: a set of actual nodes
    """
    graph, graph_rev, nodes = defaultdict(list), defaultdict(list), set()
    num_nodes = 0
    num_edges = 0

    with open(file_path, 'r') as file:
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

def find_shortest_path(source):
    """
    find shortest path from source vertex to destination
    :param source: key for starting vertex
    :param dest: key for final vertex
    :return cost: total cost of shortest path
    :return path: path of shortest path
    """
#    global GRAPH, GRAPH_REV, NODES, NUM_NODES, NUM_EDGES, MATRIX, MATRIX_PATH
    global GRAPH, GRAPH_REV, NODES, NUM_NODES, NUM_EDGES, MATRIX
    shortest_cost = np.inf
#    shortest_path = None

    MATRIX = np.full((2, len(NODES)), np.inf)
#    MATRIX_PATH = np.full((2, len(NODES)), (np.inf))

    MATRIX[0, source-1] = 0  # i = budget(prev:curr), j = node(0:len(nodes)); cost

    neg_cycle_checksum = np.inf
    early_exit_checksum = np.inf

    for budget in range(len(NODES) + 1):
        budget_prev = 0
        budget_curr = 1
        for node in NODES:
            node_key = node - 1
            previous_cost = MATRIX[budget_prev, node_key]
#            previous_path = MATRIX_PATH[budget_prev, node_key]

#            alt_cost, alt_path, penultimate_node = find_min_w_to_v(node, MATRIX, MATRIX_PATH)
            alt_cost, penultimate_node = find_min_w_to_v(node, MATRIX)

            if previous_cost <= alt_cost:
                MATRIX[budget_curr, node_key] = previous_cost
                early_exit_checksum = min(early_exit_checksum, previous_cost)
#                shortest_path = previous_path
            else:
#                new_shortest_path = alt_path + (penultimate_node, node,)
                MATRIX[budget_curr, node_key] = alt_cost
#                MATRIX_PATH[budget_curr, node_key] = new_shortest_path

                early_exit_checksum = min(early_exit_checksum, alt_cost)
#                shortest_path = new_shortest_path

            # reuse memory
            MATRIX[budget_prev, node_key] = MATRIX[budget_curr, node_key]
#            MATRIX_PATH[budget_prev, node_key] = MATRIX_PATH[budget_curr, node_key]

        # check for early exit
        if early_exit_checksum == shortest_cost:  # shortest_cost is currently previously shortest
            shortest_cost = early_exit_checksum
#            return shortest_cost, shortest_path
            return shortest_cost

        shortest_cost = early_exit_checksum

        # check for negative cycle
        if budget == len(NODES) - 1:
            neg_cycle_checksum = shortest_cost

        if budget == len(NODES) and shortest_cost < neg_cycle_checksum:
#            return None, None  # detected negative cycle
            return None  # detected negative cycle

#    return shortest_cost, shortest_path
    return shortest_cost



#def find_min_w_to_v(dest, matrix, matrix_path):
def find_min_w_to_v(dest, matrix):
    """
    find the minimum path distance from penultimate vertex w
    to destination vertex v
    :param dest: key to final destination vertex
    :param matrix: reference matrix that stores cost
    """
    global GRAPH_REV
    min_cost = np.inf
#    min_path = None
    min_node = None

    penultimate_vertices = GRAPH_REV.get(dest, [])  # (cost, penultimate_node)
    penultimate_vertices = list(zip(*penultimate_vertices))

    if penultimate_vertices:
        costs = penultimate_vertices[0]
        nodes = penultimate_vertices[1]
        for idx, node in enumerate(nodes):
            cost = costs[idx]
            node_key = node-1
            curr_cost = matrix[0, node_key]
#            curr_path = matrix_path[0, node_key]

            if curr_cost + cost < min_cost:
                min_cost = curr_cost
#                min_path = curr_path
                min_node = node

#    return min_cost, min_path, min_node
    return min_cost, min_node


def main():
    """
    main
    """
    global GRAPH, GRAPH_REV, NODES, NUM_NODES, NUM_EDGES, MATRIX

    GRAPH, GRAPH_REV, NODES, NUM_NODES, NUM_EDGES = build_graph(sys.argv[1])

    find_shortest_path(1)
    print(MATRIX)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 bellmanford_v1.py <file name>")
        sys.exit(1)

    threading.stack_size(67180864)
    sys.setrecursionlimit(10**6)

    thread = threading.Thread(target=main)
    thread.start()

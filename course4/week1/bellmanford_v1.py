"""
Bellman-Ford algorithm
"""

from collections import defaultdict
from tqdm import tqdm

import threading
import sys
import numpy as np

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


def assign_current_cost_path_for_node(node, node_key, budget_curr, budget_prev, visited):
    """
    Assign cost and path to current budget iteration
    and node
    :param node: current destination node
    :param node_key: index to current node
    :param budget_curr: current idx to save memory space
    :param budget_prev: previous idx to save memory space
    :param visited: a set to keep track of visited nodes
    """
    global MATRIX, MATRIX_PATH
    previous_cost = MATRIX[budget_prev, node_key]
    previous_path = MATRIX_PATH[budget_prev][node_key]

    alt_cost, penultimate_node, alt_path = find_min_w_to_v(node, visited)

    if previous_cost <= alt_cost:
        MATRIX[budget_curr, node_key] = previous_cost
        MATRIX_PATH[budget_curr][node_key] = previous_path
    else:
        MATRIX[budget_curr, node_key] = alt_cost
        MATRIX_PATH[budget_curr][node_key] = alt_path


def recycle_reference_matrices(node_key, budget_curr, budget_prev):
    """
    Recycle references matrices to save memory space
    :param node_key: index to node
    :param budget_curr: index to current budget iteration
    :param budget_prev: index to previous budget iteration
    """
    global MATRIX, MATRIX_PATH
    MATRIX[budget_prev, node_key] = MATRIX[budget_curr, node_key]
    MATRIX_PATH[budget_prev][node_key] = MATRIX_PATH[budget_curr][node_key]

def find_shortest_path(source):
    """
    find shortest path from source vertex to destination
    :param source: key for starting vertex
    :param dest: key for final vertex
    :return cost: total cost of shortest path
    :return path: path of shortest path
    """
    global GRAPH, GRAPH_REV, NODES, MATRIX, MATRIX_PATH
    shortest_cost = np.inf

    MATRIX = np.zeros((2, len(NODES)))  # row 1 is previous budget, row 2 is curr budget
    MATRIX_PATH = [[[] for _ in range(len(NODES))] for _ in range(2)]

    MATRIX[0, :] = np.inf
    MATRIX[0, source-1] = 0  # row is budget iterations, columns are nodes

    neg_cycle_checksum = np.inf
    early_exit_checksum = np.inf

    visited = set([source])

    for budget in tqdm(range(1, len(NODES) + 1)):
        budget_prev = 0
        budget_curr = 1
        for node in NODES:
            visited.add(node)
            node_key = node - 1
            assign_current_cost_path_for_node(node, node_key, budget_curr, budget_prev, visited)

            early_exit_checksum = min(early_exit_checksum, MATRIX[budget_curr, node_key])

            # reuse same memory space
            recycle_reference_matrices(node_key, budget_curr, budget_prev)

        # check for early exit
        if early_exit_checksum == shortest_cost:  # shortest_cost is currently previously shortest
            shortest_cost = early_exit_checksum
            print("early exit")
            return shortest_cost

        shortest_cost = early_exit_checksum

        # check for negative cycle
        if budget == len(NODES) - 1:
            neg_cycle_checksum = shortest_cost

        if budget == len(NODES) and shortest_cost < neg_cycle_checksum:
            return None  # detected negative cycle

    return shortest_cost


def find_min_w_to_v(dest, visited):
    """
    find the minimum path distance from penultimate vertex w
    to destination vertex v
    :param dest: key to final destination vertex
    :param matrix: reference matrix that stores cost
    :param visited: set of visited matrix, those that are valid to be considered
    """
    global GRAPH_REV, MATRIX, MATRIX_PATH, SOURCE
    min_cost = np.inf
    min_node = None
    min_path = []

    penultimate_vertices = GRAPH_REV.get(dest, np.array([]))  # (cost, penultimate_node)
    penultimate_vertices = list(zip(*penultimate_vertices))

    if penultimate_vertices:
        costs = penultimate_vertices[0]
        nodes = penultimate_vertices[1]
        for idx, node in enumerate(nodes):
            if node not in visited:
                continue
            cost = costs[idx]
            node_key = node-1
            curr_cost = MATRIX[0, node_key]

            if curr_cost + cost < min_cost:
                min_cost = curr_cost + cost
                min_node = node
                min_path = MATRIX_PATH[0][node_key] + [dest]

    if min_path and min_path[0] != SOURCE:
        min_path = [SOURCE] + min_path

    return min_cost, min_node, min_path


def main():
    """
    main
    """
    global GRAPH, GRAPH_REV, NODES, NUM_NODES, NUM_EDGES, MATRIX, MATRIX_PATH, SOURCE

    GRAPH, GRAPH_REV, NODES, NUM_NODES, NUM_EDGES = build_graph(sys.argv[1])

    SOURCE = 1

    shortest_cost = find_shortest_path(SOURCE)
    if not shortest_cost:
        print(shortest_cost, "detected negative cycle")
    else:
        print("cost matrix:", MATRIX[1])
        print("path matrix:", MATRIX_PATH[1])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 bellmanford_v1.py <file name>")
        sys.exit(1)

    threading.stack_size(67180864)
    sys.setrecursionlimit(10**6)

    thread = threading.Thread(target=main)
    thread.start()

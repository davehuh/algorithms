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


def find_shortest_path(graph, source, dest):
    """
    Compute shortest path from source to destination vertices
    :param graph: is a dict objet of adjacent vertices
    :param source: is a key to the starting vertex
    :param dest: is a key to the final vertex
    return: cost and path
    """
    # queue: cost, key, path
    queue, visited, mins = [(0, source, ())], set(), {source: 0}

    while queue:
        cost, key, path = heappop(queue)
        if key not in visited:
            visited.add(key)
            path = path + (key,)
            if key == dest:
                return cost, path

            for head, c in graph.get(key, ()):
                curr_cost = mins.get(head, None)
                new_cost = cost + c
                if not curr_cost or new_cost < curr_cost:
                    mins[head] = new_cost
                    heappush(queue, (new_cost, key, path))

    return 10**6, None


def main():
    """
    main
    """
    if len(sys.argv) != 2:
        print("Usage: python3 dijkstra_v2.py <file name>")
        sys.exit(1)

    graph = build_graph(sys.argv[1])

    source = 1
    dest_list = [7,37,59,82,99,115,133,165,188,197]
    num_dest = len(dest_list)
    distances = []

    for idx, dest in enumerate(dest_list):
        print('progress:', idx+1, '/', num_dest)
        distances.append(find_shortest_path(graph, source, dest)[0])

    print(distances)

if __name__ == "__main__":
    STACK_SIZE = 67108864
    RECURSION_LIMIT = 2**20

    threading.stack_size(STACK_SIZE)
    sys.setrecursionlimit(RECURSION_LIMIT)
    thread = threading.Thread(target=main)
    thread.start()

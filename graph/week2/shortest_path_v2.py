"""
Copyright 2020 Dave Huh
Shortest path using Dijkstra's algorithm
"""

import sys
import threading

from collections import defaultdict
from heapq import heappop, heappush

def read_file(file_name):
    """
    build graph structure
    :param file_name: string file path
    :return: graph structure
    """
    if len(sys.argv) != 2:
        print("Usage: python3 shortest_path_v2.py <file name>")
        sys.exit(1)


    graph = defaultdict(list)

    with open(file_name) as f:
        for lines in f:
            line = lines.split()
            if line:
                node = int(line[0])
                heads = [int(ln.split(',')[0]) for ln in line[1:]]
                costs = [int(ln.split(',')[1]) for ln in line[1:]]
                graph[node] = [(head, cost) for head, cost in zip(heads, costs)]

    return graph


def shortest_path(graph, source, dest):
    """
    compute shortest path distance with Dijkstra's shortest path algorithm
    :param graph: dict representing graph struture
    :param source: origin vertex
    :param dest: end vertex
    :return: shortest distance from source to destination vertices
    """
    queue, visited, mins = [(0, source, ())], set(), {source: 0}

    while queue:
        (cost, vertex, path) = heappop(queue)
        if vertex not in visited:
            visited.add(vertex)
            path = path + (vertex,)
            if vertex == dest:
                return cost, path

            for head, c in graph.get(vertex, ()):
                curr_cost = mins.get(head, None)
                new_cost = cost + c
                if curr_cost is None or new_cost < curr_cost:
                    mins[head] = new_cost
                    heappush(queue, (new_cost, head, path))

    return 10**6, None


def main():
    """
    main
    """

    graph = read_file(sys.argv[1])

    source = 1
    dest_list = [7,37,59,82,99,115,133,165,188,197]
    distances = []

    for idx, vertex in enumerate(dest_list):
        print("progress:", idx+1, '/', len(dest_list))
        distances.append(shortest_path(graph, source, vertex)[0])

    print(distances)


if __name__ == "__main__":
    STACK_SIZE = 67108864
    RECURSION_LIMIT = 2**20

    threading.stack_size(STACK_SIZE)
    sys.setrecursionlimit(RECURSION_LIMIT)

    thread = threading.Thread(target=main)
    thread.start()

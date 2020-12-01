"""
Copyright 2020 Dave Huh
Another implementation of DFS
"""

import sys

from collections import deque

class Vertex:
    def __init__(self, val):
        self.val = val
        self.visited = False
        self.order = -1

def build_edges_vertices(edges):
    """
    builds dict of edges and vertices
    """
    global EDGES
    global VERTICES

    for edge in edges:
        tail = edge[0]
        head = edge[1]

        if tail in EDGES:
            EDGES[tail].append(head)
        else:
            EDGES[tail] = [head]

        if tail not in VERTICES:
            VERTICES[tail] = Vertex(tail)
        if head not in VERTICES:
            VERTICES[head] = Vertex(head)

    return EDGES, VERTICES

def dfs(key, order):
    """
    DFS algorithm
    """
    global VERTICES
    global EDGES

    stack = deque([key])

    while len(stack) > 0:
        next_key = stack.pop()
        VERTICES[next_key].visited = True

        v_edges = EDGES[next_key]

        for edge in v_edges:
            if not VERTICES[edge].visited:
                stack.append(edge)

        VERTICES[next_key].order = order
        order += 1

    return order


def compute_topological_sort(source=1):
    """
    Compute topological sort of vertices
    """
    global EDGES
    global VERTICES
    curr_order = 1

    vertex = VERTICES[source]
    curr_order = dfs(source, curr_order)

    for vertex_key in VERTICES:
        vertex = VERTICES[vertex_key]
        if not vertex.visited:
            curr_order = dfs(vertex.val, curr_order)

    return VERTICES

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 second_implementation_dfs.py <file name>")
        sys.exit(1)

    file = open(sys.argv[1], 'r')

    edge_list = file.readlines()
    file.close()
    edge_list = [list(map(int, row.strip().split(' '))) for row in edge_list]

    EDGES = {}
    VERTICES = {}

    EDGES, VERTICES = build_edges_vertices(edge_list)

    VERTICES = compute_topological_sort()

    for vertex_key in VERTICES:
        vertex = VERTICES[vertex_key]
        print("val:", vertex.val, "order:", vertex.order)

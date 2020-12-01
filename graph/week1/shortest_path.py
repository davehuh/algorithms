"""
Copyright 2020 Dave Huh
Shortest path using bfs algorithm
"""

import sys

from collections import deque


class Vertex:
    def __init__(self, val):
        self.val = val
        self.visited = False
        self.dist = float("inf")

def build_edges_vertices(edge_list):
    """
    build graph from a list of edges
    returns dict of edges and dict of vertices
    """
    edges = {}
    vertices = {}

    for edge in edge_list:
        head = edge[0]
        tail = edge[1]

        if head in edges:
            edges[head].append(tail)
        else:
            edges[head] = [tail]

        if head not in vertices:
            vertices[head] = Vertex(head)

        if tail not in vertices:
            vertices[tail] = Vertex(tail)

    return edges, vertices

def compute_shortest_path(source=1, target=8):
    """
    Find shortest path from source to target nodes.
    Return shortest distance
    """
    global edges
    global vertices

    queue = deque([source])

    vertices[source].dist = 0

    while len(queue) > 0:
        vertex_key = queue.popleft()

        if vertices[vertex_key].visited:
            continue

        curr_dist = vertices[vertex_key].dist

        neighbor_keys = edges[vertex_key]

        for key in neighbor_keys:
            if vertices[key].visited:
                continue
            if vertices[key].dist > curr_dist + 1:
                vertices[key].dist = curr_dist + 1
            if key == target:
                return vertices[key].dist
            queue.append(key)

        vertices[vertex_key].visited = True

    return -1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python shortest_path.py <file name>")
        sys.exit(1)

    edges = {}
    vertices = {}

    file = open(sys.argv[1], 'r')
    edge_list = file.readlines()
    file.close()

    edge_list = [list(map(int, row.strip().split(' '))) for row in edge_list]

    edges, vertices= build_edges_vertices(edge_list)

    source = 1
    target = 3
    print("source target:", source, target)
    print("min dist:", compute_shortest_path(source, target))

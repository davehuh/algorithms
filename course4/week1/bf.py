"""
Copyright 2020 Dave Huh
Bellman-Ford algorithm
"""

import sys
import numpy as np

from collections import deque
from numba import jit


class Edge:
    def __init__(self, tail, head, length):
        self.tail = tail
        self.head = head
        self.length = length


class Graph:
    def __init__(self, vl):
        self.vl = vl
        self.dict = {}
        self.num_edges = len(vl)
        self.vertices_set = set()

    def build_graph(self):
        """
        Builds graph
        """
        for row in self.vl:
            tail = row[0]  # key
            head = row[1]
            length = row[2]

            edge = Edge(tail, head, length)

            if tail in self.dict:
                self.dict[tail].append(edge)
            else:
                self.dict[tail] = [edge]

            # add vertices to ref set
            self.vertices_set.update([tail, head])


class BellmanFord:
    """
    Computes Bellman-Ford algorithm to find shortest distance
    between two vertices in a graph for a general case
    without assumption of negative edge lengths and cycles
    """
    def __init__(self, edgeList, graph, num_vert, num_edges):
        self.el = edgeList
        self.graph = graph
        self.num_vert = num_vert
        self.num_edges = num_edges
        self.matrix = np.full((num_edges+1, num_vert), np.inf)

    def compute_shortest_path(self, source):
        """
        copmutes shortest path between source and destination
        """
        self.matrix[0, source-1] = 0

        vertex_queue = deque([source])

        min_distance = np.inf

        negative_cycle_checksum = 0
        for num_edge in range(1, self.num_edges + 1):

#            print("edge budget: ", num_edge)

            if not vertex_queue:
                break

            new_vertices = deque()

            seen_vertices = set()
            while vertex_queue:
                vertex = vertex_queue.pop()

                if vertex in seen_vertices:
                    continue
                else:
                    seen_vertices.add(vertex)

                vertex_edges = []
                if vertex in self.graph.dict:
                    vertex_edges = self.graph.dict[vertex]

                seen_vertices_in_iter = set()

                for edge in vertex_edges:
                    head = edge.head
                    tail = edge.tail
                    cost = edge.length

                    case1 = self.matrix[num_edge-1, head-1]

                    case2 = self.matrix[num_edge-1, tail-1] + cost

                    min_case1_or_case2 = min(case1, case2)

                    min_distance = min(min_distance, min_case1_or_case2)

                    self.matrix[num_edge, head-1] = min(self.matrix[num_edge, head-1],
                                                        min_case1_or_case2)

                    if head not in seen_vertices_in_iter:
                        seen_vertices_in_iter.add(head)
                        new_vertices.appendleft(head)

            vertex_queue = deque(new_vertices)

            if num_edge == self.num_edges - 1:
                negative_cycle_checksum = min_distance
            elif num_edge == self.num_edges:
                if negative_cycle_checksum == min_distance:
                    break
                else:
                    return None

        return min_distance


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 bf.py <file_name>")
        sys.exit(1)

    file = open(sys.argv[1]).read().splitlines()
    file = [row.split(' ') for row in file]
    vertices_lengths = [list(map(int, row)) for row in file]

    num_vert, num_edges = vertices_lengths.pop(0)
    print("vert: ", num_vert, " edges: ", num_edges)

    graph_ = Graph(vertices_lengths)
    graph_.build_graph()

    min_dist = np.inf

    vertices = graph_.vertices_set

    for vertex in vertices:
        bf = BellmanFord(vertices_lengths, graph_, num_vert, num_edges)
        min_from_bf = bf.compute_shortest_path(vertex)

        if min_from_bf:
            min_dist = min(min_dist, min_from_bf)
        else:
            min_dist = None
            break

    print('min dist: ', min_dist)

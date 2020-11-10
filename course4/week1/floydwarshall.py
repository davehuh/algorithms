"""
Copyright 2020 Dave Huh
Implementation of Floyd-Warshall algorithm to solve
all points shortest distance problem
"""

import sys
import numpy as np


class Edge:
    """
    A directed edge of a graph
    """
    def __init__(self, head, tail, cost=0):
        self.head = head
        self.tail = tail
        self.cost = cost

class Graph:
    """
    A directed graph
    """
    def __init__(self, edges):
        self.edges = edges
        self.directed_graph = {}

    def build_graph(self):
        """
        Builds directed graph using edges
        """
        for edge in self.edges:
            target = edge.head
            origin = edge.tail
            cost = edge.cost

            if origin in self.directed_graph:
                self.directed_graph[origin].append(edge)
            else:
                self.directed_graph[origin] = [edge]

        return self.directed_graph


class FloydWarshall:
    def __init__(self, _graph, num_edges, num_vertices):
        self.graph = _graph  # graph object with edge objects
        self.num_edges = num_edges  # int type
        self.num_vertices = num_vertices  # int type
        self.reference_matrix = np.full((num_vertices+1,
                                         num_vertices+1, num_vertices+1), np.inf)
        self.seen_vertices = set()  # reduce extra work if vertices were considered

    def initialize_reference_matrix(self):
        """
        Initialize reference matrix
        """
        np.fill_diagonal(self.reference_matrix[:,:,0], 0)

        for i in range(1, self.num_vertices+1):
            for j in range(1, self.num_vertices+1):
                if i == j:
                    continue

                if i in self.graph:
                    edges = self.graph[i]

                    for edge in edges:
                        target = edge.head
                        if target == j:
                            self.reference_matrix[i, j, 0] = edge.cost


    def compute_all_points_shortest_path_distances(self):
        """
        Compute minimum of all points shortest path distances
        """
        min_dist = np.inf
        for k in range(1, self.num_vertices+1):
            for i in range(1, self.num_vertices+1):
                for j in range(1, self.num_vertices+1):
                    case_1 = self.reference_matrix[i, j, k-1]
                    case_2 = self.reference_matrix[i, k, k-1] + \
                        self.reference_matrix[k, j, k-1]
                    self.reference_matrix[i,j,k] = min(case_1, case_2)

                    min_dist = min(self.reference_matrix[i,j,k], min_dist)

        return min_dist


def build_edge_list(edges):
    _edge_list = []
    for edge in edges:
        head = edge[0]
        tail = edge[1]
        cost = edge[2]

        _edge_list.append(Edge(head, tail, cost))

    return _edge_list


def read_file(file):
    """
    Reads file.
    Outputs header with number of nodes and edges
    and list of edges
    """
    if not file:
        sys.exit(1)

    input_file = open(file).read().splitlines()
    input_file = [row.split(' ') for row in input_file]
    edge_list = [list(map(int, row)) for row in input_file]
    num_vertices, num_edges = edge_list.pop(0)

    return num_vertices, num_edges, edge_list

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 floydwarshall.py <file name>")
        sys.exit(1)

    input_file = sys.argv[1]
    num_vertices, num_edges, edge_list = read_file(input_file)

    edge_list = np.array(edge_list)
    edge_list = build_edge_list(edge_list)

    graph = Graph(edge_list)
    graph = graph.build_graph()

    floyd_warshall = FloydWarshall(graph, num_edges, num_vertices)
    floyd_warshall.initialize_reference_matrix()
    shortest_distance = floyd_warshall.compute_all_points_shortest_path_distances()

"""
Copyright 2020 Dave Huh
Bellman-Ford algorithm
"""

import sys
import numpy as np

from collections import deque


class Edge:
    def __init__(self, tail, head, length):
        self.tail = tail
        self.head = head
        self.length = length


class Graph:
    def __init__(self, vl):
        self.vl = vl
        self.dict = {}
        self.numEdges = len(vl)

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


class BellmanFord:
    """
    Computes Bellman-Ford algorithm to find shortest distance
    between two vertices in a graph for a general case
    without assumption of negative edge lengths and cycles
    """
    def __init__(self, edgeList, graph, numVert, numEdges):
        self.el = edgeList
        self.graph = graph
        self.numVert = numVert
        self.numEdges = numEdges
        self.matrix = np.zeros((numEdges, numVert))
        self._buildMatrix()

    def _buildMatrix(self):
        """
        Builds a reference matrix of edge cost
        """
        self.matrix[0, :] = np.inf
#        for edge in self.el:
#            row = edge[0]
#            col = edge[1]
#            val = edge[2]
#            self.matrix[row, col] = val

    def _getMinEdgeCost(self, tail, head):
        _minCost = np.inf

        _edgeList = self.graph[tail]

        for edge in _edgeList:
            tail = edge.tail
            headCheck = edge.head
            cost = edge.length
            if headCheck == head:
                _minCost = min(cost, _minCost)
        return _minCost

    def _evaluateCase2(self, vertex, penUltVertices, edge):
        _case2 = np.inf
        _minVert = -1

        for pVert in penUltVertices:
            costWtoV = self._getMinEdgeCost(pVert, vertex)
            lookup = self.matrix[edge-1, pVert] + costWtoV

            if lookup < _case2:
                _minVert = pVert
                _case2 = lookup

        return _case2

    def computeShortestPath(self, source):
        """
        Performs shortest path between source and destination
        """
        self.matrix[0, source] = 0

        penUltVert_Dict = {}  # w (penultimate) vertices

        for edge in range(1, self.numEdges):
            for vertex in range(self.numVert):
                case1 = self.matrix[edge-1, vertex]

                case2 = np.inf

                # evalute case 2
                if vertex in penUltVert_Dict:
                    penUltVertices = penUltVert_Dict[vertex]

                    case2 = self._evaluateCase2(vertex, penUltVertices, edge)

                self.matrix[edge, vertex] = min(case1, case2)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 bf.py <file_name>")
        sys.exit(1)

    file = open(sys.argv[1]).read().splitlines()
    file = [row.split(' ') for row in file]
    vertices_lengths = [list(map(int, row)) for row in file]

    numVert, numEdges = vertices_lengths.pop(0)

    s = 1
    v = 3

    graph_ = Graph(vertices_lengths)
    graph_.build_graph()
#
#    print(graph_.dict)
#
#    bf = BellmanFord(graph_.dict, numVert, numEdges)
    bf = BellmanFord(vertices_lengths, graph_, numVert, numEdges)
    bf.computeShortestPath(s, v)

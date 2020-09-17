"""
Copyright 2020 Dave Huh
Clustering algorithm
"""

import sys
from functools import total_ordering
import heapq


class Node:
    def __init__(self, key):
        self.key = key


@total_ordering
class Edge:
    def __init__(self, v1, v2, cost):
        self.v1 = v1
        self.v2 = v2
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.cost == other.cost


class Graph:
    def __init__(self):
        self.edges = []
        self.nodes = set()

    def buildGraph(self, listGraph):
        for edge in listGraph:
            v1 = edge[0]
            v2 = edge[1]
            cost = edge[2]
            self.nodes.update([v1, v2])
            edge = Edge(v1, v2, cost)
            heapq.heappush(self.edges, edge)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 cluster.py <file name>")
        sys.exit(1)

    textFile = open(sys.argv[1])
    textFile = textFile.read().splitlines()
    numNodes = textFile.pop(0)
    list_graph = [list(map(int, ele.split(" "))) for ele in textFile]
    graph = Graph()
    graph.buildGraph(list_graph)

    print(list_graph[:5])

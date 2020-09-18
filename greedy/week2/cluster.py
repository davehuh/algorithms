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


class Cluster:
    def __init__(self, k, graph):
        self.k = k
        self.graph = graph
        self.clusters = []

    def buildCluster(self):
        edges = self.graph.edges
        self.clusters = dict.fromkeys(self.graph.nodes, None)
#        print("clusters before: ", self.clusters)
#       while len(self.clusters) > k:
        while len(edges) > 0:
            edge = heapq.heappop(edges)
            v1 = edge.v1
            v2 = edge.v2

            # stopping condition
            if len(self.clusters) == k:
                if v1 in self.clusters and v2 in self.clusters:
                    print("final: ", self.clusters)
                    return edge.cost
                else:
                    continue

            if v1 not in self.clusters or v2 not in self.clusters:
                continue
            if v1 in self.clusters and v2 in self.clusters and \
                    self.clusters[v1] and self.clusters[v2]:
                self.clusters[v1].add(v2)
                for key in self.clusters[v2]:
                    self.clusters[v1].add(key)
                self.clusters.pop(v2, None)
                continue

            if v1 in self.clusters:
                if not self.clusters[v1]:
                    self.clusters[v1] = {v2}
                else:
                    self.clusters[v1].add(v2)
                self.clusters.pop(v2, None)

        print("final: ", self.clusters)
        return edges[0].cost


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

    k = 4  # a priori number of clusters
    clusters = Cluster(k, graph)
    max_spacing = clusters.buildCluster()
    print("max spacing: ", max_spacing)

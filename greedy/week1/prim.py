"""
Copyright 2020 Dave Huh
Generates minimal spanning tree using Prim's algorithm
"""

import sys
import heapq
from functools import total_ordering
import pandas as pd


class Node:
    """
    Vertex of a graph
    Variables:
        key: the key of the vertex
        neighbors: a heap of edges that connect to neighboring nodes
    """
    def __init__(self, key):
        self.key = key
        self.neighbors = []

    def addEdge(self, neighbor, weight):
        """
        Adds a neighboring edge to the node

        Input:
            neighbor: is the key for the neighboring vertex of the vertex
            weight: is the weighted distance from the
                vertex to the neighbor
        """
        edge = Edge(neighbor, weight)
        heapq.heappush(self.neighbors, edge)


@total_ordering
class Edge:
    """
    Edge in a graph
    This object is a component of the node object.
    It assumes that the edge is stored in an origin node object
    Hence no need to store pointers or keys to the origin.

    Global variables:
        endVertex: vertex connected by the edge
        weight: weighted distance from origin vertex to end vertex
    """
    def __init__(self, endVertex, weight):
        self.endVertex = endVertex
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        return self.weight == other.weight

    def __repr__(self):
        return 'end vertex: ' + str(self.endVertex)


class Graph:
    def __init__(self):
        """
        graph contains
        """
        self.graph = {}
        self.obsVertex = {}

    def addNode(self, key):
        """
        Adds node to graph

        Input:
            key: is the key for the new vertex

        Output:
            returns node to allow for further manipulations
        """
        newVertex = Node(key)
        self.graph[key] = newVertex

        return self.graph[key]

    def buildGraph(self, graphDF):
        """
        Builds graph by going row by row in adjacency list data frame
        """
        for index, vertex in graphDF.iterrows():
            key = vertex['v1']
            otherVertex = vertex['v2']
            weight = vertex['cost']

            # create new vertex if doesn't exist in graph
            if key not in self.graph:
                node = self.addNode(key)
            if otherVertex not in self.graph:
                otherNode = self.addNode(otherVertex)

            node = self.graph[key]
            node.addEdge(otherVertex, weight)

            otherNode = self.graph[otherVertex]
            otherNode.addEdge(key, weight)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 prim.py <file name>")
        sys.exit(1)

    textFile = open(sys.argv[1])
    textFile = textFile.read().splitlines()
    numNodesEdges = textFile.pop(0)
    listGraph = [list(map(int, ele.split(" "))) for ele in textFile]
    dfGraph = pd.DataFrame(listGraph)
    dfGraph = dfGraph.rename(columns={0: 'v1', 1: 'v2', 2: 'cost'})
    weightedGraph = Graph()
    weightedGraph.buildGraph(dfGraph)

    for vertex in weightedGraph.graph.values():
        print("vertex: ", vertex.key)
        print(vertex.neighbors)

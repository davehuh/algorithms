"""
Copyright 2020 Dave Huh
Generates minimal spanning tree using Prim's algorithm
"""

import sys
import heapq
import pandas as pd
from functools import total_ordering


class Node:
    def __init__(self, key, neighbors=None):
        self.key = key

        if not neighbors:
            self.neighbors = []
        else:
            self.neighbors = neighbors


@total_ordering
class Edge:
    def __init__(self, key, weight):
        self.key = key
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        return self.weight == other.weight


class Graph:
    def __init__(self):
        """
        graph contains
        """
        self.graph = {}
        self.obsVertex = {}

    def addNode(self, key, neighbor=None, weight=None):
        """
        Adds node to graph

        Input:
            key: is the key for the new vertex
            neighbor: is the key for the neighboring vertex of the new vertex
            weight: is the weighted distance from the
                new vertex to the neighbor
        """
        newVertex = Node(key)
        self.graph[key] = newVertex
        weightedNeighbor = []
        # check if neighbor vertex exists
        if neighbor not in self.graph:
            self.addNode(neighbor, key, weight)

        if neighbor:
            edge = Edge(neighbor, weight)
            heapq.heappush(weightedNeighbor, edge)

        newVertex.neighbors = weightedNeighbor

    def addEdge(self, key, neighbor, weight):
        """
        Adds a neighboring edge to existing node to the graph

        Input:
            key: is the key for the exisiting vertex
            neighbor: is the key for the neighboring vertex of the vertex
            weight: is the weighted distance from the
                vertex to the neighbor
        """
        node = self.graph[key]
        edge = Edge(neighbor, weight)
        heapq.heappush(node.neighbors, edge)

        neighborVertex = self.graph[neighbor]
        neighborEdge = Edge(key, weight)
        heapq.heappush(neighborVertex.neighbors, neighborEdge)

    def buildGraph(self, graphDF):
        """
        Builds graph by going row by row in adjacency list data frame
        """
        for index, vertex in graphDF.iterrows():
            key = vertex['v1']
            otherVertex = vertex['v2']
            weight = vertex['cost']

            print(key, otherVertex, weight)

            # create new vertex if doesn't exist in graph
            if key not in self.graph:
                print("here")
                self.addNode(key, otherVertex, weight)

            # add neighbors if it doesn't exist in graph
#            if key in self.graph:
#                neighbors = self.graph[key].neighbors
#                # check if neighbors exist
#                if otherVertex not in neighbors:
#                    self.addNeighbor(key, otherVertex, weight)
#
#            if otherVertex in self.graph:
#                neighbors = self.graph[otherVertex].neighbors
#                # check if neighbors exist
#                if key not in neighbors:
#                    self.addNeighbor(otherVertex, key, weight)


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

    print("num of nodes and edges: ", numNodesEdges)

    for vertex in weightedGraph.graph:
        print(vertex)

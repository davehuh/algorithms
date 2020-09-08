"""
Copyright 2020 Dave Huh
Generates minimal spanning tree using Prim's algorithm
"""

import sys
import heapq
from functools import total_ordering
import pandas as pd
import random


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
        edge = Edge(self.key, neighbor, weight)
        heapq.heappush(self.neighbors, edge)

    def removeEdge(self, key, weight):
        """
        Removes an edge

        Input:
            key is the end vertex key
            weight is the weighted distance between the node and the end vertex
        """

        raise NotImplementedError


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
    def __init__(self, originVertex, endVertex, weight):
        self.originVertex = originVertex
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


class MinimumSpanningTree:
    def __init__(self, graphObj):
        self.graph = graphObj
        self.seenVertex = set()
        self.seenEdge = []
        self.cost = 0

    def computeWeightsOfMinimumSpanningTree(self):
        """
        Computes total weight of minimum spanning tree

        Output:
            self.cost: the total weight of minimum spanning tree
        """
        selectedNode = random.randrange(1, len(self.graph) + 1, 1)
#        selectedNode = 1
        print("random seed: ", selectedNode)

        vertex = self.graph[selectedNode]
        heapq.heappush(self.seenEdge, vertex.neighbors[0])

#        while len(self.seenEdge) > 0:
        while len(self.seenVertex) != len(self.graph):
            edge = heapq.heappop(self.seenEdge)

            originVertex = self.graph[edge.originVertex]
            otherVertex = self.graph[edge.endVertex]

            if originVertex.key in self.seenVertex and \
                    otherVertex.key in self.seenVertex:
                continue

            if originVertex.neighbors:
                heapq.heappop(originVertex.neighbors)

            # remove same edge from the endVertex
            if otherVertex.neighbors:
                for i in range(len(otherVertex.neighbors)):
                    otherEdge = otherVertex.neighbors[i]

                    if otherEdge.endVertex == originVertex.key:
                        otherVertex.neighbors.pop(i)
                        heapq.heapify(otherVertex.neighbors)
                        break

#            print("vertex: ", originVertex.key, "num neighbors: ",
#                  originVertex.neighbors)

            self.cost += edge.weight
            self.seenVertex.add(originVertex.key)
            self.seenVertex.add(otherVertex.key)
#            print("seen vertex: ", self.seenVertex)

            # next in queue
            if originVertex.neighbors:
                self.seenEdge = self.seenEdge + originVertex.neighbors
                heapq.heapify(self.seenEdge)
#                heapq.heappush(self.seenEdge, originEdge)
#                print("pushing: ", originEdge.weight)
#                print("from origin: ", originEdge.originVertex,
#                      "weight: ", originEdge.weight)

#                originOtherVertexKey = originEdge.endVertex
#                originOtherVertex = self.graph[originOtherVertexKey]
#                if originOtherVertex.neighbors:
#                    for i in range(len(originOtherVertex.neighbors)):
#                        otherVertexEdge = originOtherVertex.neighbors[i]
#                        if otherVertexEdge.endVertex == \
#                                originEdge.originVertex:
#                            originOtherVertex.neighbors.pop(i)
#                            heapq.heapify(originOtherVertex.neighbors)
#                            break

            if otherVertex.neighbors:
                self.seenEdge = self.seenEdge + otherVertex.neighbors
                heapq.heapify(self.seenEdge)
#                heapq.heappush(self.seenEdge, originEdge)
#                print("other pushing: ", originEdge.weight)
#                print("from end: ", originEdge.originVertex,
#                      "weight: ", originEdge.weight)

#                originOtherVertexKey = originEdge.endVertex
#                originOtherVertex = self.graph[originOtherVertexKey]
#                if originOtherVertex.neighbors:
#                    for i in range(len(originOtherVertex.neighbors)):
#                        otherVertexEdge = originOtherVertex.neighbors[i]
#                        if otherVertexEdge.endVertex == \
#                                originEdge.originVertex:
#                            originOtherVertex.neighbors.pop(i)
#                            heapq.heapify(originOtherVertex.neighbors)
#                            break

        return self.cost


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

#    for vertex in weightedGraph.graph.values():
#        print("vertex: ", vertex.key)
#        print(vertex.neighbors)

    spanningTree = MinimumSpanningTree(weightedGraph.graph)
    totalWeightsMST = spanningTree.computeWeightsOfMinimumSpanningTree()
    print("Minimum Spanning Tree total weights: ", totalWeightsMST)

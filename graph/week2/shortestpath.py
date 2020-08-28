"""
Copyright 2020 Dave Huh
Implementation of Dijkstra's shortest path algorithm using heap data structure
"""

import sys
import heapq
from functools import total_ordering
import re

# class ShortestPath:
#    raise NotImplementedError


@total_ordering
class Vertex:
    """
    Value is the value of the vertex
    Neighbors are key-value pairs of heads and distances from the vertex (tail)
    Explored is a boolean variable whether or not the vertex has been visited
    """
    def __init__(self, value, neighbors=None):
        self.value = value
        self.neighbors = {}
        self.explored = False
        self.scoreFromSource = float("inf")

        if neighbors:
            self.addEdges(neighbors)

    def addEdges(self, neighbors):
        """
        Edges are key-value pairs where keys represent head vertexes
        and values represent distances from tail

        Input: neighbors is a dict type with key value pairs of
        head vertex as key and distance as value
        """
        # don't add if there are duplicates
        edges = neighbors.keys()

        # assumes edges is dict type
        for edge in edges:  # edge is a key
            if edge not in self.neighbors \
                    or self.neighbors[edge] != neighbors[edge]:
                self.neighbors[edge] = neighbors[edge]

    def __lt__(self, other):
        return self.scoreFromSource < other.scoreFromSource

    def __eq__(self, other):
        return self.scoreFromSource == other.scoreFromSource

    def __repr__(self):
        return '{0.__class__.__name__}(value={0.value})'


class Graph:
    def __init__(self):
        self.graph = None

    def buildGraph(self, al):
        """
        build graph from an adjacency list
        """
        for line in al:
            value = line[0]
            edges = line[1]  # assumes line has len > 1
            edgeKeys = edges.keys()  # assumes edges has dict type

            # check if graph has required lengths for storing vertexes
            minNumberOfNodesRequired = max([value] + list(edgeKeys))
            if not self.graph:
                self.graph = [None] * minNumberOfNodesRequired
            elif len(self.graph) < minNumberOfNodesRequired:  # expand length
                self.graph = self.graph + [None] * (minNumberOfNodesRequired
                                                    - len(self.graph))

            # check if vertex with the value exists
            vertex = self.graph[value - 1]
            if vertex:
                vertex.addEdges(edges)
            else:
                self.graph[value - 1] = Vertex(value, edges)

            # check if vertex with each edge values exists
            for edge in edgeKeys:
                newEdgeVertex = self.graph[edge - 1]
                if not newEdgeVertex:
                    self.graph[edge - 1] = Vertex(edge)

        return self.graph


class ShortestPath:
    """
    Compute shortest path from source to all vertices with paths in a graph
    using Dijkstra's implementation
    """
    def __init__(self, graphObj):
        self.graph = graphObj
        self.verticesProcessed = {}  # X
        self.verticesNotProcessed = []  # V - X
        self.shortestPathDistances = {}

    def determineNextVertexToProcess(self, vertex):
        """
        Use Dijkstra's greedy criterion to solve which head vertexes
        in the frontier to process next
        Input:
            vertex that needs its neighbors (heads) pushed into queue
        """
        sourceScore = vertex.scoreFromSource

        # push all edges (heads) from vertex to heap
        for headKey in vertex.neighbors:
            head = self.graph[headKey - 1]
            distanceTohead = vertex.neighbors[headKey]
            score = sourceScore + distanceTohead
            if head.scoreFromSource > score:
                head.scoreFromSource = score

            if headKey not in self.verticesProcessed:
                heapq.heappush(self.verticesNotProcessed, head)

    def computeShortestPaths(self, source):
        sourceVertex = self.graph[source - 1]
        sourceVertex.scoreFromSource = 0
        sourceVertex.explored = True
        self.shortestPathDistances[sourceVertex.value] = \
            sourceVertex.scoreFromSource
        self.verticesProcessed[sourceVertex.value] = \
            sourceVertex.scoreFromSource
        self.determineNextVertexToProcess(sourceVertex)

#        while len(self.verticesProcessed) != len(self.graph):
        while len(self.verticesNotProcessed) > 0:
#            print("length: ", len(self.verticesProcessed))

            sourceVertex = heapq.heappop(self.verticesNotProcessed)
            sourceVertex.explored = True
            self.verticesProcessed[sourceVertex.value] = \
                sourceVertex.scoreFromSource
            self.determineNextVertexToProcess(sourceVertex)

        for k, v in self.verticesProcessed.items():
            print(k, v)


def buildList(al):
    """
    Build adjacency list from text file
    First element in the raw adjacency list is the vertex
    The subsequent entries are key value pairs of tails from the vertex
    and weights/distances to the tail vertex. The key-value pairs are
    organized into dict type.

    Input: adjacency list with first element being key for the vertex
    and following elements which are key-value pairs of heads

    Output: graphList is a list of key and dictionary of key-value pairs
    """
    if not al:
        print("invalid input")
        sys.exit(1)

    graphList = [None]*(len(al))

    for lineNum in range(len(al)):
        al[lineNum] = al[lineNum].strip()
        al[lineNum] = re.sub('\s+', ' ', al[lineNum])
        al[lineNum] = al[lineNum].split(' ')

        # except this first value, put everything else into dict
        graphList[lineNum] = [(int(al[lineNum][0]))]
        keyValueList = {}
        for eleNum in range(1, len(al[lineNum])):
            keyValuePair = list(map(int, al[lineNum][eleNum].split(',')))
            keyValueList[keyValuePair[0]] = keyValuePair[1]

        graphList[lineNum].append(keyValueList)

    return graphList


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 shortestpath.py <file name>")
        sys.exit(1)

    textFile = open(sys.argv[1])
    adjacencyList = textFile.read().splitlines()
    adjacencyList = buildList(adjacencyList)
    graph = Graph()
    graph = graph.buildGraph(adjacencyList)

    shortestPaths = ShortestPath(graph)
    shortestPaths.computeShortestPaths(1)

#    vertices = [7,37,59,82,99,115,133,165,188,197]
#
#    for vertex in vertices:
#        if vertex in shortestPaths.shortestPathDistances:
#            print("vertex: ", vertex, " dist: ",
#                  shortestPaths.shortestPathDistances[vertex])
#        else:
#            print("vertex: ", vertex, " dist: inf")

"""
Copyright 2020 Dave Huh
Implementation of Dijkstra's shortest path algorithm using heap data structure
"""

import sys
import heapq

# class ShortestPath:
#    raise NotImplementedError

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
            if self.neighbors:
                # add edges if not already present or need to update distances
                edgeAlreadyExist = self.neighbors[edge]
                if not edgeAlreadyExist or neighbors[edge] != edgeAlreadyExist:
                    self.neighbors[edge] = neighbors[edge]


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
        al[lineNum] = al[lineNum].split('\t')

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
    graph.buildGraph(adjacencyList)
    graph = graph.graph
    for vertex in graph:
        print(vertex.value)

"""
Copyright 2020 Dave Huh
"""

import sys


class Vertex:
    """
    Vertex in a graph
    """
    def __init__(self, value, edges):
        self.value = value
        self.edges = edges  # contains a list of keys
        self.explored = False
        self.ts = 0  # topological sort ranking


class Graph:
    """
    A graph with vertexes and edges
    """
    def __init__(self):
        self.graph = []

    def buildGraph(self, al):
        """
        Build a graph from adjacency list
        """
        if not al:
            print("invalid input")
            sys.exit(1)

        # create vertexes
        for node in al:
            value = node[0]
            edges = node[1:]
            nodeObj = Vertex(value, edges)
            self.graph.append(nodeObj)

        return self.graph


class DFS:
    """
    Depth first search algorithm
    """
    def __init__(self):
        self.currentLabel = 0

    def search(self, graphObj, start):
        node = graphObj[start - 1]
        node.explored = True
        for edge in node.edges:
            vertex = graphObj[edge - 1]
            if not vertex.explored:
                self.search(graphObj, edge)

        node.ts = self.currentLabel
        self.currentLabel -= 1

    def topologicalSort(self, graphObj):
        self.currentLabel = len(graphObj)
        print("starting label:", self.currentLabel)
        for vertex in graphObj:
            if not vertex.explored:
                self.search(graphObj, vertex.value)

            print("vertex: ", vertex.value, " ts: ", vertex.ts)


def buildList(al):
    """
    Build a list from raw adjacency list format
    """
    for lineNum in range(len(al)):
        al[lineNum] = al[lineNum].strip()
        al[lineNum] = list(map(int, al[lineNum].split('\t')))

    return al


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 dfs.py <file name>")
        sys.exit(1)

    textFile = open(sys.argv[1])
    adjacencyList = textFile.read().splitlines()
    adjacencyList = buildList(adjacencyList)
    graph = Graph()
    graph = graph.buildGraph(adjacencyList)
    dfs = DFS()
    dfs.topologicalSort(graph)

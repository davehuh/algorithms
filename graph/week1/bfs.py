"""
Copyright 2020 Dave Huh
"""

import sys


class Node:
    """
    Node of a graph
    """
    def __init__(self, val, edges):
        self.value = val
        self.edges = edges
        self.explored = False
        self.distance = float("inf")


class Graph:
    """
    Graph
    """
    def __init__(self):
        self.nodes = []

    def createGraph(self, al):
        """
        creates a graph from an adjacent list
        """
        self.nodes = [None]*len(al)
        for node in al:
            value = node[0]
            edges = node[1:]
            newNode = Node(value, edges)
            self.nodes[value - 1] = newNode  # key is 1 - value of nodes

        return self.nodes


class BFS:
    """
    Breadth first search
    Output shortest paths
    """
    def __init__(self, graph):
        self.graph = graph
        self.toExplore = []

    def search(self, start, target):
        """
        Traverses through graph from the start node towards the target node
        if there is a path.
        Uses breadth-first-search algorithm to find shorest path.
        Returns shortest path in integer
        """
        if start is None or target is None:
            print("invalid input")
            sys.exit(1)

        if start == target:
            return 0

        self.graph[start - 1].distance = 0

        self.toExplore.append(self.graph[start - 1])

        while self.toExplore:
            node = self.toExplore.pop()
            if node.value == target:
                return node.distance

            for edge in node.edges:
                edge = self.graph[edge - 1]
                if not edge.explored:
                    edge.explored = True
                    edge.distance = node.distance + 1
                    self.toExplore.append(edge)

    def findConnectedComponents(self):
        """
        TODO
        connected components
        yield number of communities in graph
        """
        raise NotImplementedError


def buildList(al):
    """
    Build a list from delimited adjacent list
    """
    for i in range(len(al)):
        al[i] = al[i].strip()
        al[i] = list(map(int, al[i].split('\t')))

    return al


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 bfs.py <file name>")
        sys.exit(1)

    txtFile = open(sys.argv[1])
    adjacent_list = txtFile.read().splitlines()

    adjacent_list = buildList(adjacent_list)
    graph = Graph()
    graph = graph.createGraph(adjacent_list)

    # search

    # find connected components

    bfs = BFS(graph)
    print(bfs.search(5, 6))
    print(bfs.search(5, 8))

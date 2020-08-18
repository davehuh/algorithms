"""
Copyright 2020 Dave Huh
"""

import sys

class Node:
    """
    Node of a graph
    """
    def __init__(self, val, an):
        self.value = val
        self.explored = False
        self.adjacentNodes = an

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
            adjacentList = node[1:]
            newNode = Node(value, adjacentList)
            self.nodes[value - 1] = newNode  # key is 1 - value of nodes


class BFS:
    """
    Breadth first search
    Output shortest paths
    """
    def search(self, graph, start, target):
        """
        Traverses through graph from the start node towards the target node
        if there is a path.
        Uses breadth-first-search algorithm to find shorest path.
        Returns shortest path in integer
        """
        if start is None or target is None:
            print("invalid input")
            sys.exit(1)

        raise NotImplementedError

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
    graph.createGraph(adjacent_list)
    bfs = BFS()

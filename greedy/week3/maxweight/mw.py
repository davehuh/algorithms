"""
Copyright 2020 Dave Huh
Computes maximum-weight independent set of a path graph
"""

import sys

class Node:
    def __init__(self, val, weight):
        self.val = val
        self.weight = weight

class Graph:
    def __init__(self):
        self.nodes = []

    def buildNodes(self, vertices):
        i = 1

        for weight in vertices:
            newNode = Node(i, weight)
            self.nodes.append(newNode)
            i += 1
            print(newNode.val, newNode.weight)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 mw.py <file_name>")
        sys.exit(1)

    file = open(sys.argv[1])
    file = file.read().splitlines()
    numNodes = file.pop(0)
    vert_weights = list(map(int, file))

    graph = Graph()
    graph.buildNodes(vert_weights)

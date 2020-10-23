"""
Copyright 2020 Dave Huh
Computes maximum-weight independent set of a path graph
"""

import sys
import numpy as np


class Node:
    """
    Node of a graph
    """
    def __init__(self, val, weight):
        self.val = val
        self.weight = weight

    def __add__(self, other):
        return self.weight + other

    def __radd__(self, other):
        return other + self.weight

    def get_val(self):
        """
        Utility function to return value of node (key)
        """
        return self.val


class Graph:
    """
    Graph to solve maximum weight independent set
    """
    def __init__(self):
        self.nodes = []
        self.lookupWeights = {}  # memoization of subset solutions
        self.lookupNodes = {}  # reconstruction of nodes

    def build_nodes(self, vertices):
        """
        Creates nodes and inserts into graph obj
        """
        i = 1

        for weight in vertices:
            newNode = Node(i, weight)
            self.nodes.append(newNode)
            i += 1

    def populate_lookup(self):
        """
        Populate lookup list for MWIS calculations
        """
        self.lookupWeights[0] = 0
        self.lookupWeights[1] = self.nodes[0].weight

        self.lookupNodes[0] = []
        self.lookupNodes[1] = [self.nodes[0]]

        i = 2

        while i < len(self.nodes) + 1:
            node = self.nodes[i - 1]  # current node

            if self.lookupWeights[i - 1] > self.lookupWeights[i - 2] + \
                    node.weight:
                self.lookupWeights[i] = self.lookupWeights[i - 1]
                self.lookupNodes[i] = self.lookupNodes[i - 1]
            else:
                self.lookupWeights[i] = self.lookupWeights[i - 2] + \
                    node.weight
                self.lookupNodes[i] = self.lookupNodes[i - 2] + \
                    [node]

            i += 1


    def compute_MWIS(self):
        """
        Computes maximum-weight independent set
        returns maximum weight and M-W set
        """
        set1 = self.lookupNodes[len(self.nodes)]
        set2 = self.lookupNodes[len(self.nodes) - 1]

        sumSet1 = self.lookupWeights[len(self.nodes)]
        sumSet2 = self.lookupWeights[len(self.nodes) - 1]

        if sumSet1 > sumSet2:
            return set1, sumSet1

        return set2, sumSet2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 mw.py <file_name>")
        sys.exit(1)

    file = open(sys.argv[1])
    file = file.read().splitlines()
    numNodes = file.pop(0)
    vert_weights = list(map(int, file))

    graph = Graph()
    graph.build_nodes(vert_weights)
    graph.populate_lookup()

    maxSet, maxWeight = graph.compute_MWIS()

    testNodes = [1,2,3,4,17,117,517,997]
    bits = ''

    vecfunc = np.vectorize(Node.get_val, otypes=[object])
    vals = set(vecfunc(maxSet))

    for test in testNodes:
        if test in vals:
            bits = bits + '1'
        else:
            bits = bits + '0'

    print("weight: ", maxWeight)
    print("bits: ", bits)

#    print("lookup weights: ", graph.lookupWeights)
#    print("lookup nodes: ", vals)

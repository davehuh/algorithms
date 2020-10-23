"""
Copyright 2020 Dave Huh
Computes maximum-weight independent set of a path graph
"""

import sys
import numpy as np


class Node:
    def __init__(self, val, weight):
        self.val = val
        self.weight = weight

    def __add__(self, other):
        return self.weight + other

    def __radd__(self, other):
        return other + self.weight

    def getVal(self):
        return self.val


class Graph:
    def __init__(self):
        self.nodes = []

    def buildNodes(self, vertices):
        i = 1

        for weight in vertices:
            newNode = Node(i, weight)
            self.nodes.append(newNode)
            i += 1

    def computeMWIS(self):
        """
        Computes maximum-weight independent set
        returns maximum weight and M-W set
        """
        set1 = np.array(self.nodes[0::2])
        set2 = np.array(self.nodes[1::2])

        sumSet1 = set1.sum()
        sumSet2 = set2.sum()

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
    graph.buildNodes(vert_weights)
    maxSet, maxWeight = graph.computeMWIS()

    testNodes = [1,2,3,4,17,117,517,997]
    bits = ''

    vecfunc = np.vectorize(Node.getVal, otypes=[object])
    vals = set(vecfunc(maxSet))

    for test in testNodes:
        if test in vals:
            bits = bits + '1'
        else:
            bits = bits + '0'

    print("weight: ", maxWeight)
    print("bits: ", bits)

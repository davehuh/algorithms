"""
Copyright 2020 Dave Huh
Clustering of graph with bit format
"""
from itertools import combinations

import sys
import faulthandler
import numpy as np

faulthandler.enable()


def generateCombinationsByHammingDist(bitvalues, distance):
    """
    Generate combinations of a list of bits
    Input:
        bitvalues: list of bits with length n
        distance: hamming distance. r = len(bitvalues) - distance
    """
    combo = list(combinations(enumerate(bitvalues), distance))
    comboInd = []
    for node in combo:
        bitIndices = []
        for ind_bit_pair in node:
            ind = ind_bit_pair[0]
            bitIndices.append(ind)
        comboInd.append(bitIndices)

    finalCombos = set()

    for nodeIndices in comboInd:
        if nodeIndices:
            manipulatedVertex = list(bitvalues)
            for nodeIndex in nodeIndices:
                index = int(nodeIndex)
                if manipulatedVertex[index] == '0':
                    manipulatedVertex[index] = '1'
                else:
                    manipulatedVertex[index] = '0'

            manipulatedVertex = "".join(manipulatedVertex)
            finalCombos.add(manipulatedVertex)

    return finalCombos

#    for nodeIndex in range(len(comboInd)):
#        prevInd = -1
#        indToManipulate = []
#        for ind in comboInd[nodeIndex]:
#            if prevInd + 1 != ind:
#                for i in range(prevInd + 1, ind):
#                    indToManipulate.append(i)
#
#            prevInd = ind
#
#            if len(indToManipulate) == distance:
#                break
#
#        assembledNode = list(bitvalues)  # list of a node str
#        if indToManipulate:
#            for i in indToManipulate:
#                a_bit = assembledNode[i]
#                if a_bit == '0':
#                    assembledNode[i] = '1'
#                else:
#                    assembledNode[i] = '0'
#
#        assembledNode = ''.join(assembledNode)
#
#        checkDist = computeDistanceBetweenNodes(bitvalues, assembledNode)
#
#        if checkDist == distance:
#            finalCombos.add(assembledNode)


def computeDistanceBetweenNodes(seq1, seq2):
    """
    Computes Hammer distance between two sequences of bits

    Input:
        seq1: first sequence
        seq2: second sequence to be compared to the first sequence

    Output:
        distance: Hammer distance between two bit sequences
    """
    if isinstance(seq1, str):
        seq1 = list(seq1)
        seq1 = [int(digit) for digit in seq1]
        seq1 = np.array(seq1)
    if isinstance(seq2, str):
        seq2 = list(seq2)
        seq2 = [int(digit) for digit in seq2]
        seq2 = np.array(seq2)

    diff = seq1 - seq2
    distance = np.count_nonzero(diff)
    return distance


class Clustering:
    def __init__(self, graph, maxHammingDist):
        self.graph = set(graph)  # graph in list
        self.clusters = []  # list of clusters
        self.references = {}  # hashmap of nodes with specified hamming dist
        self.maxHammingDist = maxHammingDist  # maximum hamming distance
        self.observedNodes = set()

    def buildRefTable(self):
        for row in self.graph:
            key = row
            hammingDistances = list(range(self.maxHammingDist + 1))
            reference = set()
            for dist in hammingDistances:
                newRefs = generateCombinationsByHammingDist(row, dist)

                reference.update(newRefs)

            self.references[key] = reference

    def findAllNeighbors(self, node, cluster=set()):
        if node in self.observedNodes:
            return cluster

        stack = []
        stack.append(node)

        while len(stack) > 0:
            currNode = stack.pop()

            self.observedNodes.add(currNode)
            refs = self.references[currNode]

            for ref in refs:
                if ref not in self.observedNodes and ref in self.graph:
                    cluster.add(ref)
                    stack.append(ref)

        return cluster

    def computeNumClusters(self):
        for vertex in self.graph:
            if vertex in self.observedNodes:
                continue

            newCluster = self.findAllNeighbors(vertex)

            self.clusters.append(newCluster)
            self.observedNodes.update(newCluster)

        return len(self.clusters)


if __name__ == "__main__":
    textFile = open(sys.argv[1])
    textFile = textFile.read().splitlines()
    header = textFile.pop(0)
    numNodes, bitsLength = header.split(" ")

    print("header: ", header)
    graphList = [''.join(row.split(' ')) for row in textFile]

    hammingDist = 2

    clustering = Clustering(graphList, hammingDist)
    clustering.buildRefTable()

    numK = clustering.computeNumClusters()

    print("K: ", numK)

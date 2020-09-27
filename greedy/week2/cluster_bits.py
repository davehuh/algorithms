"""
Copyright 2020 Dave Huh
Clustering of graph with bit format
"""
import faulthandler; faulthandler.enable()

from functools import total_ordering
from itertools import combinations, combinations_with_replacement, \
    permutations

import sys
import heapq

import numpy as np

sys.setrecursionlimit(1500)


@total_ordering
class Node:
    """
    Node in a graph.
    Node is represented in bits
    """
    def __init__(self, key, value):
        """
        key is sum of bits in value
        value is list of bits representing the node
        """
        self.key = key
        self.value = value

    def __lt__(self, other):
        return self.key < other.key

    def __eq__(self, other):
        return self.key == other.key


def generateCombinationsByHammingDist(bitvalues, distance):
    """
    Generate combinations of a list of bits
    Input:
        bitvalues: list of bits with length n
        distance: hamming distance. r = len(bitvalues) - distance
    """
#    print("NODE: ", bitvalues)
#    print("DISTANCE: ", distance)
    combo = list(combinations(enumerate(bitvalues), distance))
    comboInd = []
    for node in combo:
        bitIndices = []
        for ind_bit_pair in node:
            ind = ind_bit_pair[0]
            bitIndices.append(ind)
        comboInd.append(bitIndices)

#    print("num combos ref: ", len(comboInd))
#    print("combos ref: ", comboInd)

    finalCombos = set()

    for nodeIndices in comboInd:
        if nodeIndices:
            manipulatedVertex = list(bitvalues)
#            print("mani vertex before: ", ''.join(manipulatedVertex))
            for nodeIndex in nodeIndices:
                index = int(nodeIndex)
                if manipulatedVertex[index] == '0':
                    manipulatedVertex[index] = '1'
                else:
                    manipulatedVertex[index] = '0'

            manipulatedVertex = "".join(manipulatedVertex)
#            print("mani vertex after:  ", manipulatedVertex)
            finalCombos.add(manipulatedVertex)

#    print("num combinations for dist: ", len(finalCombos))
#    print("combinations: ", finalCombos)

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


class Cluster:
    def __init__(self):
        self.minHeap = []
        self.maxHeap = []
        self.flatList = []

    def addNodeToCluster(self, node):
        heapq.heappush(self.minHeap, node)  # add to min heap

        node.key = -node.key
        heapq.heappush(self.maxHeap, node)  # add to max heap

        self.flatList.append(node.value)

    def addNodeBitsToCluster(self, values):
        if len(self.flatList) == 0:
            self.flatList.append(values)
            self.flatList = np.array(self.flatList)
            return
        np.append(self.flatList, [values])


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
#            print("key: ", key)
            hammingDistances = list(range(self.maxHammingDist + 1))
            reference = set()
#            reference = []
            for dist in hammingDistances:
                newRefs = generateCombinationsByHammingDist(row, dist)
#                print("new combos: ", newRefs)
#                print("new ref length: ", len(newRefs))
#                print("intermediaries length before: ", len(reference))

                reference.update(newRefs)
#                reference.append(newRefs)

#                print("intermediaries length after: ", len(reference))

#            print("ref final len: ", len(reference))
            self.references[key] = reference

    def findAllNeighbors(self, node):
        newCluster = set(node)
        refs = self.references[node]
        for ref in refs:
            if ref not in self.observedNodes and ref in self.graph:
                self.observedNodes.add(ref)
                newCluster.add(ref)
                refCluster = self.findAllNeighbors(ref)
                newCluster.update(refCluster)

        self.observedNodes.add(node)
        return newCluster

    def computeNumClusters(self):
        # build hash map of nodes that fall within max hamming dist
        self.buildRefTable()

        print("graph length: ", len(self.graph))

        vertexProgressCounter = 0
        for vertex in self.graph:
            vertexProgressCounter += 1
#            print("progress: ", vertexProgressCounter)

            if vertex in self.observedNodes:
                continue

            newCluster = self.findAllNeighbors(vertex)
#            newCluster = set(vertex)
#            refs = self.references[vertex]
#            for ref in refs:
#                if ref in self.observedNodes:
#                    break
#                if ref in self.graph:
#                    newCluster.add(ref)

            self.clusters.append(newCluster)
            self.observedNodes.update(newCluster)

        print("observedNodes: ", len(self.observedNodes))

        return len(self.clusters)


if __name__ == "__main__":
#    if len(sys.argv) != 2:
#        print("Usage: python3 cluster_bits.py <file name>")
#        sys.exit(1)

    textFile = open(sys.argv[1])
    textFile = textFile.read().splitlines()
    header = textFile.pop(0)
    numNodes, bitsLength = header.split(" ")

    print("header: ", header)
    graphList = [''.join(row.split(' ')) for row in textFile]

    hammingDist = 2

    clustering = Clustering(graphList, hammingDist)
    numK = clustering.computeNumClusters()

    print("K: ", numK)
#    print("main, clusters: ", clustering.clusters)

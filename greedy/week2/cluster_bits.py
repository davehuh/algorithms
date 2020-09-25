"""
Copyright 2020 Dave Huh
Clustering of graph with bit format
"""

from functools import total_ordering
from itertools import combinations, combinations_with_replacement, \
    permutations

import sys
import heapq

import numpy as np


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
    print("NODE: ", bitvalues)
    print("DISTANCE: ", distance)
    combo = list(combinations(enumerate(bitvalues), len(bitvalues) - distance))
    comboInd = []
    for node in combo:
        bitIndices = []
        for ind_bit_pair in node:
            ind = ind_bit_pair[0]
            bitIndices.append(ind)
        comboInd.append(bitIndices)

    print("num combos ref: ", len(comboInd))

    finalCombos = set()
    for nodeIndex in range(len(comboInd)):
        prevInd = -1
        indToManipulate = []
        for ind in comboInd[nodeIndex]:
            if prevInd + 1 != ind:
                for i in range(prevInd + 1, ind):
                    indToManipulate.append(i)

            prevInd = ind

            if len(indToManipulate) == distance:
                break

        assembledNode = list(bitvalues)  # list of a node str
        if indToManipulate:
            for i in indToManipulate:
                a_bit = assembledNode[i]
                if a_bit == '0':
                    assembledNode[i] = '1'
                else:
                    assembledNode[i] = '0'

        assembledNode = ''.join(assembledNode)
        finalCombos.add(assembledNode)

    print("num combinations: ", len(finalCombos))
    print("combinations: ", finalCombos)

    return finalCombos

#    combo = [ind_bit_tuple[0] for ind_bit_tuple
#             in combinations(enumerate(bitvalues),
#                             len(bitvalues) - distance)]
#    combo = [''.join(nodeBits) for nodeBits in combo]
#    print("combination: ", combo)

#    return combo
#    combo = combinations(bitvalues, len(bitvalues) - distance)
#    combo = [''.join(nodeBits) for nodeBits in combo]
#
#    bits = '01'
#    bitCombos = set()
#    bitCombos_part1 = combinations_with_replacement(bits, distance)
#    bitCombos_part2 = permutations(bits, distance)
#    bitCombos.update(bitCombos_part1)
#    bitCombos.update(bitCombos_part2)
#    bitCombos = [''.join(bitChain) for bitChain in bitCombos]
#    print("NODE: ", bitvalues)
#    print("DISTANCE: ", distance)
##    print("node combinations: ", list(combo))
#    print("bit combinations: ", list(bitCombos))
#
#    comboSet = set()
#    for nodeFragment in combo:
#        print("node fragment: ", nodeFragment)
#        for bitFragment in bitCombos:
##            print("bit fragment: ", bitFragment)
#            nodeTest = nodeFragment + bitFragment
#            hDist = computeDistanceBetweenNodes(bitvalues, nodeTest)
#            if hDist <= distance:
##                print("joined node: ", nodeTest)
##                print("calculated distance: ", hDist)
#                comboSet.add(nodeTest)
#            nodeTest = bitFragment + nodeFragment
#            hDist = computeDistanceBetweenNodes(bitvalues, nodeTest)
#            if hDist <= distance:
##                print("joined node: ", nodeTest)
##                print("calculated distance: ", hDist)
#                comboSet.add(nodeTest)
#
#    print("num combinations: ", len(comboSet))
#
#    return comboSet


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

    def buildRefTable(self):
        for row in self.graph:
            key = row
            hammingDistances = list(range(self.maxHammingDist + 1))
            reference = []
            for dist in hammingDistances:
                newRefs = generateCombinationsByHammingDist(row, dist)

                reference.append(newRefs)

#            reference = set()
#            for dist in hammingDistances:
#                newRefs = generateCombinationsByHammingDist(row, dist)
#                print("from combo: ", len(list(newRefs)))
#
#                newList = []
#                for values in newRefs:
#                    values = ''.join(values)
#                    if len(values) == len(row):
#                        newList.append(values)
#
#                reference.update(newList)

            self.references[key] = reference

    def computeNumClusters(self):
        # build hash map of nodes that fall within max hamming dist
        self.buildRefTable()

#        print("Ref hash map: \n", self.references)

        for vertex in self.graph:
            vertexRefs = self.references[vertex]
            vertexCluster = set(vertex)
            addNewCluster = True
            for ref in vertexRefs:
                if ref in self.graph:
                    vertexCluster.add(ref)

            if len(self.clusters) > 0:
                for cluster in self.clusters:
                    if vertex in cluster:
                        # update cluster
                        cluster.update(vertexCluster)
                        addNewCluster = False
                        break

            if len(self.clusters) == 0 or addNewCluster:
                self.clusters.append(vertexCluster)

        return len(self.clusters)

#        nodeCount = 0
#        for row in self.graph:
#            nodeCount += 1
#            print("node: ", nodeCount)
#            value = row

#            addNewCluster = True
#
#            for cluster in self.clusters:
#                # Hammer distances
#                diff = cluster.flatList - value
#                distances = np.count_nonzero(diff, axis=1)
#                distances = set(distances)
#
#                if 3 in distances or 2 in distances or 1 in distances:
#                    cluster.addNodeBitsToCluster(value)
#                    addNewCluster = False
#                    break
#
#            if len(self.clusters) == 0 or addNewCluster:
#                cluster = Cluster()
#                cluster.addNodeBitsToCluster(value)
#                self.clusters.append(cluster)
#
#        return len(self.clusters)

#        threshold = 2
#        nodeCount = 0
#        k = 0
#        for row in self.graph:
#            nodeCount += 1
#            print(nodeCount)
#            # create node
#            key = row.sum()
#            value = row
#            node = Node(key, value)

#            # iterate through clusters
#            appendNewCluster = True
#            for cluster in self.clusters:
#                min_node = cluster.minHeap[0]
#                max_node = cluster.maxHeap[0]
#
#                if key >= min_node.key - threshold and key <= -max_node.key + \
#                        threshold:
#
#                    nodesInCluster = np.array(cluster.flatList)
#                    diff = nodesInCluster - value
#                    distances = np.count_nonzero(diff, axis=1)
#
#                    if np.any(distances < 3):
#                        cluster.addNodeToCluster(node)
#                        appendNewCluster = False
#                        break
#
#            if len(self.clusters) < 1 or appendNewCluster:
#                cluster = Cluster()
#                cluster.addNodeToCluster(node)
#                self.clusters.append(cluster)

#        return len(self.clusters)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 cluster_bits.py <file name>")
        sys.exit(1)

    textFile = open(sys.argv[1])
    textFile = textFile.read().splitlines()
    header = textFile.pop(0)
    numNodes, bitsLength = header.split(" ")

    graphList = [''.join(row.split(' ')) for row in textFile]
#    graphList = [row.strip(" ") for row in textFile]
#    graphList = [list(map(int, bit.strip().split(" "))) for bit in textFile]
#    graphList = np.array(graphList)
    print(graphList)

    hammingDist = 2

    clustering = Clustering(graphList, hammingDist)
    numK = clustering.computeNumClusters()

    print("K: ", numK)
    print(clustering.clusters)

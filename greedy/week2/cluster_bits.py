"""
Copyright 2020 Dave Huh
Clustering of graph with bit format
"""

from functools import total_ordering

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


def computeDistanceBetweenNodes(seq1, seq2):
    """
    Computes Hammer distance between two sequences of bits

    Input:
        seq1: first sequence
        seq2: second sequence to be compared to the first sequence

    Output:
        distance: Hammer distance between two bit sequences
    """
    diff = seq1 - seq2
    distance = np.count_nonzero(diff)
    return distance


class Clustering:
    def __init__(self, graph):
        self.graph = graph
        self.clusters = []

    def computeNumClusters(self):
        threshold = 2
        for row in self.graph:
            # create node
            key = row.sum()
            value = row
            node = Node(key, value)

            # iterate through clusters
            appendNewCluster = True
            for cluster in self.clusters:
                min_node = cluster.minHeap[0]
                max_node = cluster.maxHeap[0]

                if key >= min_node.key - threshold and key <= -max_node.key + \
                        threshold:

                    nodesInCluster = np.array(cluster.flatList)
                    diff = nodesInCluster - value
                    distances = np.count_nonzero(diff, axis=1)

                    if np.any(distances < 3):
                        cluster.addNodeToCluster(node)
                        appendNewCluster = False
                        break

            if len(self.clusters) < 1 or appendNewCluster:
                cluster = Cluster()
                cluster.addNodeToCluster(node)
                self.clusters.append(cluster)

        return len(self.clusters)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 cluster_bits.py <file name>")
        sys.exit(1)

    textFile = open(sys.argv[1])
    textFile = textFile.read().splitlines()
    header = textFile.pop(0)
    numNodes, bitsLength = header.split(" ")

    graphList = [list(map(int, bit.strip().split(" "))) for bit in textFile]
    graphList = np.array(graphList)

    clustering = Clustering(graphList)
    numK = clustering.computeNumClusters()

    print("K: ", numK)

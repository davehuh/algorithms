"""
Copyright 2020 Dave Huh
Huffman algorithm to find variable length encodings
"""

import sys

from collections import deque


class HuffmanCodes:
    def __init__(self, nodes):
        self.nodes = nodes
        self.queue1 = deque()
        self.queue2 = deque()
        self.tree = []

    def mergeNodes(self):
        self.queue1 = deque(self.nodes)

        print("before: ", self.queue1)

        while len(self.queue1) > 2:
            smallestNode = self.queue1.pop()
            self.queue2.append(smallestNode)

            smallerNode = self.queue1.pop()
            self.queue2.append(smallerNode)

            mergedNodes = smallestNode + smallerNode
            self.queue1.append(mergedNodes)

        print("after: ", self.queue1)
        print("mergedNodes: ", self.queue2)

    def constructTree(self):
        raise NotImplementedError


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 huffman.py <file name>")
        sys.exit(1)

textFile = open(sys.argv[1])
textFile = textFile.read().splitlines()
numNodes = textFile.pop(0)
vertices = list(map(int, textFile))
vertices.sort(reverse=True)

huffman = HuffmanCodes(vertices)
huffman.mergeNodes()
huffman.constructTree()

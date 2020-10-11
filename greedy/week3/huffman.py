"""
Copyright 2020 Dave Huh
Huffman algorithm to find variable length encodings
"""

import sys

from collections import deque
from functools import total_ordering


class Node:
    """
    Treenode for variable length encoding
    """
    def __init__(self, symbol="", bit=None,
                 left=None, right=None):
        if isinstance(symbol, int):
            symbol = str(symbol)

        self.symbol = symbol  # using weight, currently int type
        self.bit = bit
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.symbol < other.symbol

    def __eq__(self, other):
        return self.symbol == other.symbol


class HuffmanCodes:
    def __init__(self, nodes):
        self.nodes = nodes
        self.set = set(nodes)
        self.queue_nodes = deque()
        self.queue_merged = deque()
        self.tree = Node()

    def initializeNodes(self):
        for node in self.nodes:
            self.queue_nodes.append(Node(symbol=node))

    def findMin(self):
        """
        Utility function to find min weight node between two queues
        """
        if not self.queue_merged:
            return self.queue_nodes.pop()

        if not self.queue_nodes:
            return self.queue_merged.pop()

        if self.queue_nodes[-1] < self.queue_merged[-1]:
            return self.queue_nodes.pop()

        return self.queue_merged.pop()

    def mergeNodes(self):
        while self.queue_nodes or len(self.queue_merged) > 1:
            left = self.findMin()
            left.bit = 0
            right = self.findMin()
            right.bit = 1

            symbol = left.symbol + right.symbol

            top = Node(symbol)
            top.left = left
            top.right = right

            self.queue_merged.append(top)


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
huffman.initializeNodes()
huffman.mergeNodes()

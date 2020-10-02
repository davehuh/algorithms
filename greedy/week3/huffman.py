"""
Copyright 2020 Dave Huh
Huffman algorithm to find variable length encodings
"""

import sys

from collections import deque


class Node:
    """
    Treenode for variable length encoding
    """
    def __init__(self, symbol="", bit=None,
                 left=None, right=None, parent=None):
        if isinstance(symbol, int):
            symbol = str(symbol)

        self.symbol = symbol  # using weight, should be str type
        self.bit = bit
        self.left = left
        self.right = right
        self.parent = parent


class HuffmanCodes:
    def __init__(self, nodes):
        self.nodes = nodes
        self.set = set(nodes)
        self.queue_merged = deque()
        self.queue_reconstructSteps = deque()
        self.tree = Node()

    def mergeNodes(self):
        self.queue_merged = deque(self.nodes)

        print("before: ", self.queue_merged)

        while len(self.queue_merged) > 2:
            smallestNode = self.queue_merged.pop()
            self.queue_reconstructSteps.append(smallestNode)

            smallerNode = self.queue_merged.pop()
            self.queue_reconstructSteps.append(smallerNode)

            mergedNodes = smallestNode + smallerNode
            self.queue_merged.append(mergedNodes)

        print("after: ", self.queue_merged)
        print("mergedNodes: ", self.queue_reconstructSteps)

    def constructTree(self):
        """
        Runs after mergeNode. Reconstructs tree by decreasing weights
        """
        rightWeight = self.queue_merged.pop()
        rightNode = Node(symbol=rightWeight, bit=1)

        leftWeight = self.queue_merged.pop()
        leftNode = Node(symbol=leftWeight, bit=0)

        rootNode = Node(left=leftNode, right=rightNode)

        rightNode.parent = rootNode
        leftNode.parent = rootNode

        currNode = rootNode.right

        while len(self.queue_reconstructSteps) > 0:
            nextWeight = self.queue_reconstructSteps.pop()

            if nextWeight in self.set:
                # valid node and not merge of nodes
                nextLeftNode = Node(symbol=nextWeight, bit=0)
                parentNode = Node(bit=1, left=nextLeftNode)

                print("nextWeight: ", nextWeight)
                if currNode.parent:
                    currNode.parent.right = parentNode
                currNode = parentNode
            else:
                nextRightNode = Node(symbol=nextWeight, bit=1, parent=currNode)
                currNode.right = nextRightNode
                currNode = nextRightNode

        self.tree = rootNode

    def findMaximumLength(self):
        """
        returns maximum length
        """
        currNode = self.tree
        maxLength = 0
        while currNode:
            maxLength += 1

            currNode = currNode.right

        return maxLength


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
print("max length: ", huffman.findMaximumLength())

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
    def __init__(self, symbol=-1, bit='',
                 left=None, right=None, isNode=False):
#        if isinstance(symbol, int):
#            symbol = str(symbol)

        self.symbol = symbol  # using weight, currently int type
        self.bit = bit
        self.left = left
        self.right = right
        self.isNode = isNode
        self.visitedMax = False
        self.visitedMin = False

    def __lt__(self, other):
        return self.symbol < other.symbol

    def __eq__(self, other):
        return self.symbol == other.symbol


class HuffmanCodes:
    def __init__(self, nodes):
        self.nodes = nodes
        self.queue_nodes = deque()
        self.queue_merged = deque()
        self.tree = Node()
        self.nodeBits = []

    def initializeNodes(self):
        for node in self.nodes:
            self.queue_nodes.append(Node(symbol=node, isNode=True))

    def findMin(self):
        """
        Utility function to find min weight node between two queues
        """
        if not self.queue_merged:
            return self.queue_nodes.pop()

        if not self.queue_nodes:
            return self.queue_merged.popleft()

        if self.queue_nodes[-1] < self.queue_merged[0]:
            return self.queue_nodes.pop()

        return self.queue_merged.popleft()

    def mergeNodes(self):
#        print(self.nodes)
        while self.queue_nodes or len(self.queue_merged) > 1:
            left = self.findMin()
            left.bit = str(0)

            right = self.findMin()
            right.bit = str(1)

            symbol = left.symbol + right.symbol

            top = Node(symbol)
            top.left = left
            top.right = right

#            print("------------------")
#            print("top: ", symbol)
#            print("left: ", left.isNode, left.symbol)
#            print("right: ", right.isNode, right.symbol)

            self.queue_merged.append(top)

#            for node in self.queue_merged:
#                print(node.symbol)

        self.tree = self.queue_merged[0]
        return self.tree

    def findMaxDepth(self, root):
        if not root:
            return 0

        leftDepth = 0
        rightDepth = 0

        if root.left:
            leftDepth = self.findMaxDepth(root.left)

        if root.right:
            rightDepth = self.findMaxDepth(root.right)

        if leftDepth > rightDepth:
            return leftDepth + 1

        return rightDepth + 1

    def findMinDepth(self, root):
        if not root:
            return 0

        leftDepth = 0
        rightDepth = 0

        if root.left:
            leftDepth = self.findMinDepth(root.left)

        if root.right:
            rightDepth = self.findMinDepth(root.right)

        if leftDepth < rightDepth:
            return leftDepth + 1

        return rightDepth + 1
    def findMaxLength(self, root):
        if root is None:
            return

        currNode = root


#        nextNodes = deque()
#        bitsTracker = deque()
#        while currNode:
#            bits = bits + currNode.bit
#            if currNode.left:
#                nextNodes.append(currNode.left)
#                bitsTracker.append(bits)
#            if currNode.right:
#                nextNodes.append(currNode.right)
#                bitsTracker.append(bits)
#
#            if nextNodes:
#                currNode = nextNodes.pop()
#                bits = bitsTracker.pop()
#            else:
#                currNode = None
#            print(bits)
#
#        return max(bitsTracker, key = len)

        bitCodeLeft = ''
        bitCodeRight = ''

        if currNode.left:
#            print('left: ', currNode.left.symbol)
            bitCodeLeft = bitCodeLeft + str(currNode.left.bit)
            bits = self.findMaxLength(currNode.left)
            bitCodeLeft = bitCodeLeft + bits

            if not currNode.isNode and len(bitCodeLeft) > 0:
                self.nodeBits.append(bitCodeLeft)

        if currNode.right:
#            print('right: ', currNode.right.symbol)
            bitCodeRight = bitCodeRight + str(currNode.right.bit)
            bits = self.findMaxLength(currNode.right)
            bitCodeRight = bitCodeRight + bits

            if not currNode.isNode and len(bitCodeRight) > 0:
                self.nodeBits.append(bitCodeRight)

        if bitCodeLeft and len(bitCodeLeft) > len(bitCodeRight):
            return currNode.bit + bitCodeLeft

        return currNode.bit + bitCodeRight

    def findMinLength(self, root):
        if root is None:
            return

        currNode = root
        bitCodeLeft = ''
        bitCodeRight = ''

        if currNode.left:
#            print('left: ', currNode.left.symbol)
            bitCodeLeft = bitCodeLeft + str(currNode.left.bit)
            bits = self.findMinLength(currNode.left)
            bitCodeLeft = bitCodeLeft + bits

        if currNode.right:
#            print('right: ', currNode.right.symbol)
            bitCodeRight = bitCodeRight + str(currNode.right.bit)
            bits = self.findMinLength(currNode.right)
            bitCodeRight = bitCodeRight + bits

        if bitCodeLeft and len(bitCodeLeft) < len(bitCodeRight):
            return bitCodeLeft

        return bitCodeRight

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
tree = huffman.mergeNodes()

maxDepth = huffman.findMaxDepth(tree)
print("max depth: ", maxDepth)

minDepth = huffman.findMinDepth(tree)
print("min depth: ", minDepth)

#longestBits = huffman.findMaxLength(tree)
#print(longestBits, "\n length: ", len(longestBits))
#shortestBits = huffman.findMinLength(tree)
#print(shortestBits, "\n length: ", len(shortestBits))
#maxLength = len(max(huffman.nodeBits, key=len))
#minLength = min(huffman.nodeBits, key=len)
#print("len version 2: ", maxLength)

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
        """
        Invariant: nodes must be sorted
        """
        nodes = deque(self.nodes)

        print("nodes: ", nodes)

        while len(nodes) > 2:
            # nodes can come from nodes or merged nodes queue
            # determine which two nodes to merge

            # determine smallest node
            nodeFromNodes = nodes[-1]

            nodeFromMerged = None

            if self.queue_merged:
                nodeFromMerged = self.queue_merged[-1]

            smallestNode = None
            if not nodeFromMerged or nodeFromNodes < nodeFromMerged:
                smallestNode = nodes.pop()
            else:
                smallestNode = self.queue_merged.pop()

            self.queue_reconstructSteps.append(smallestNode)

            # determine smaller node
            nodesFromNodesSmaller = None
            if nodes:
                nodeFromNodesSmaller = nodes[-1]

            nodeFromMergedSmaller = None

            if self.queue_merged:
                nodeFromMergedSmaller = self.queue_merged[-1]

            smallerNode = None
            if nodesFromNodesSmaller and nodeFromNodesSmaller < \
                    nodeFromMergedSmaller:
                smallerNode = nodes.pop()
            elif self.queue_merged:
                smallerNode = self.queue_merged.pop()

            self.queue_reconstructSteps.append(smallerNode)

            mergedNodes = smallestNode + smallerNode

            self.queue_reconstructSteps.append(mergedNodes)

            # determine where mergedNodes should belong
            if nodes and nodes[-1] >= mergedNodes:
                nodes.append(mergedNodes)
            else:
                self.queue_merged.append(mergedNodes)

        while self.queue_merged:
            nodeFromMergedQueue = self.queue_merged.pop()

            nodeFromNodes = None
            if nodes:
                nodeFromNodes = nodes.pop()

            smallestNode = None
            if nodeFromNodes and nodeFromNodes < nodeFromMergedQueue:
                smallestNode = nodeFromNodes
            else:
                smallestNode = nodeFromMergedQueue

            self.queue_reconstructSteps.append(smallestNode)

            smallerNode = None
            nodeFromNodesSmaller = None
            if nodes:
                nodeFromNodesSmaller = nodes.pop()

            nodeFromMergedSmaller = None
            if self.queue_merged:
                nodeFromNodesSmaller = self.queue_merged.pop()

            if nodeFromNodesSmaller and nodeFromMergedSmaller:
                if nodeFromMergedSmaller <= nodeFromNodesSmaller:
                    smallerNode = nodeFromMergedSmaller
                else:
                    smallerNode = nodeFromNodesSmaller
            elif nodeFromNodesSmaller:
                smallerNode = nodeFromNodesSmaller
            else:
                smallerNode = nodeFromMergedSmaller

            self.queue_reconstructSteps.append(smallerNode)

            mergedNodes = smallestNode + smallerNode

            self.queue_reconstructSteps.append(mergedNodes)

            nodes.append(mergedNodes)

        print("nodes after: ", nodes)
        print("reconstruction steps: ", self.queue_reconstructSteps)

#        self.queue_merged = deque(self.nodes)
#
#        print("before: ", self.queue_merged)
#
#        tmp_queue = deque()
#
#        """
#        Invariant 1:
#            self.queue_merged must maintain sorted order
#        """
#        while len(self.queue_merged) > 2:
#            smallestNode = None
#            if not tmp_queue:
#                smallestNode = self.queue_merged.pop()
#            else:
#                fromTmpNode = tmp_queue[-1]
#                fromQueue = self.queue_merged[-1]
#                if fromTmpNode <= fromQueue:
#                    smallestNode = tmp_queue.pop()
#                else:
#                    smallestNode = self.queue_merged.pop()
#
#            print("node1 merge: ", smallestNode)
#            self.queue_reconstructSteps.append(smallestNode)
#
#            smallerNode = None
#
#            if not tmp_queue:
#                smallerNode = self.queue_merged.pop()
#            else:
#                fromTmpNode = tmp_queue[-1]
#                fromQueue = self.queue_merged[-1]
#                if fromTmpNode <= fromQueue:
#                    smallerNode = tmp_queue.pop()
#                else:
#                    smallerNode = self.queue_merged.pop()
#
#            print("node2 merge: ", smallerNode)
#            self.queue_reconstructSteps.append(smallerNode)
#
#            mergedNodes = smallestNode + smallerNode
#
#            # Check if mergedNodes is smaller than next in queue
#            if not self.queue_merged or mergedNodes <= self.queue_merged[-1]:
#                self.queue_merged.append(mergedNodes)
#            else:
#                tmp_queue.append(mergedNodes)
#
#        print("after: ", self.queue_merged)
#        print("mergedNodes: ", self.queue_reconstructSteps)
#        print("tmp_queue: ", tmp_queue)

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
# huffman.constructTree()
# print("max length: ", huffman.findMaximumLength())

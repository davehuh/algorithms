"""
Copyright 2020 Dave Huh
Implementation of heap
"""

import sys


class node:
    """
    Heap node contains value and pointer to two children nodes
    """
    def __init__(self, val):
        """
        initialize with value
        """
        self.val = val

    def addLeft(self, node):
        """
        add pointer to child node
        """
        self.left = node

    def addRight(self, node):
        """
        add pointer to right node
        """
        self.right = node


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 heapsort.py <array>")
        sys.exit(1)

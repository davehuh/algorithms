"""
Copyright 2020 Dave Huh
Clustering of graph with bit format
"""

import sys
import numpy as np
from difflib import SequenceMatcher

"""
Split condition: cluster need at least spacing of 3
nodes with only 2 bits or less in common are in different clusters
"""


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 cluster_bits.py <file name>")
        sys.exit(1)

    textFile = open(sys.argv[1])
    textFile = textFile.read().splitlines()
    header = textFile.pop(0)
    numNodes, bitsLength = header.split(" ")

    graph = [list(map(int, bit.strip().split(" "))) for bit in textFile]
    graph = np.array(graph)

    print(numNodes, bitsLength)
    print(graph)
    print(graph.shape)

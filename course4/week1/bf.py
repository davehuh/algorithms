"""
Copyright 2020 Dave Huh
Bellman-Ford algorithm
"""

import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 bf.py <file_name>")
        sys.exit(1)

    file = open(sys.argv[1]).read().splitlines()
    file = [row.split(' ') for row in file]
    vertices_lengths = [list(map(int, row)) for row in file]

    numVert, numEdges = vertices_lengths.pop(0)

    print(vertices_lengths)

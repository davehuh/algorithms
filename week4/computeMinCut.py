"""
Copyright 2020 Dave Huh
"""

import sys
import random


class MinCut:
    """
    Compute min cut
    """

    def computeMinCut(self, graph):
        """
        Compute min cut with adjacent list
        """

        # edge cases
        if graph is None:
            sys.exit(1)

        minCutCount = None

        while len(graph) > 2:
            graph = contractEdge(graph)

        minCutCount = len(graph[0]) - 1

        return minCutCount


def contractEdge(graph):
    """
    Randomly pick an edge to contract
    """
    chosenNodeIdx = random.choice(range(len(graph)))
    chosenEdgeIdx = random.choice(range(1, len(graph[chosenNodeIdx])))
    chosenEdge = [graph[chosenNodeIdx][0],
                  graph[chosenNodeIdx][chosenEdgeIdx]]

#    print("number of nodes before: ", len(graph))
#    print(chosenNodeIdx, " ", chosenEdgeIdx)
#    print("chosen edge: ", chosenEdge)
#
#    print("before")
#    print(graph[chosenNodeIdx])

    # add all adjacencies to chosen node
    graph[chosenNodeIdx].pop(chosenEdgeIdx)

    otherNode = None
    for otherNode in range(len(graph)):
        if graph[otherNode] == chosenEdge[1]:
            graph[chosenNodeIdx].extend(graph[otherNode][1:])
            break

    # remove self loops
    indexesToRemove = []
    for i in range(1, len(graph[chosenNodeIdx])):
        if graph[chosenNodeIdx][i] == chosenEdge[0]:
            indexesToRemove.append(i)

    for ele in indexesToRemove:
        graph[chosenNodeIdx].pop(ele)

#    print("after")
#    print(graph[chosenNodeIdx])

    # pop otherNode
    graph.pop(otherNode)

#    print("number of nodes after: ", len(graph))

    return graph


def buildList(al):
    """
    Build a list from raw adjacency list
    """
    for i in range(len(al)):
        al[i] = al[i].strip()
        al[i] = list(map(int, al[i].split('\t')))

    return al


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 computeMinCut.py <file name>")
        sys.exit(1)

    txtFile = open(sys.argv[1])
    content_list = txtFile.read().splitlines()

    numTrials = 10000000
    min_count = None

    min_cut = MinCut()

    graph = buildList(content_list)

    while numTrials > 0:
        tmp = min_cut.computeMinCut(graph)
        if min_count is None:
            min_count = tmp
        if tmp < min_count:
            min_count = tmp
        numTrials -= 1

    print("min cut count: ", min_count)

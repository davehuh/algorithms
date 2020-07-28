"""
Copyright 2020 Dave Huh
"""

import math
import sys
import csv


class dijkstra:
    """
    Computes Dijkstra's shortest path, using heap
    """

    NO_PATH = 1000000

    def __init__(self, graph, cv):
        """
        input graph which rows represent vertex
        first column represents destination vertex
        second column represents distance/weight

        outputs shortest path from vertex 1 from first row
        """
        self.graph = graph
        self.cv = cv
        self.s = graph[0][0][0]  # source
        self.vp = [None]*len(graph)  # vertices processed
        self.sd = [None]*len(graph)  # shortest distances

        self.vp[0] = self.s
        self.sd[0] = 0

        # print(self.graph[2][0][0])
        # yields vertex key

    def computeShortestPath(self):
        """
        input graph which rows represent vertex
        first column represents destination vertex
        second column represents distance/weight

        outputs shortest path from vertex 1 from first row
        """
        for row in range(len(self.graph)):
            # track row, which vertices to compute greedy Dijkstra
            v = self.graph[row][0][0]  # key to sd list

            for ele in range(1, len(self.graph[row])):
                if len(self.graph[row][ele]) == 2:
                    self.computeGreedyDijkstra(v, self.graph[row][ele])

    def computeGreedyDijkstra(self, head, ele):
        """
        Computes greedy dijkstra A with previous distance

        Input:
        source contains which source vertex (i.e. row)
        ele is a list of tail and distance

        Output:
        compares previous entry of shortest distance to tail
        and records new shortest path if needed

        greedy Dijkstra score for v, w = A[v] + l_vw
        """
        tail = ele[0] - 1  # w, used as key which is actual w - 1
        distanceFromHeadToTail = ele[1]  # l_vw

        if head == self.s:
            distanceFromSourceToHead = 0
        else:
            distanceFromSourceToHead = self.sd[head - 1]  # A[v]

        if distanceFromSourceToHead is None:  # no path from source to head
            score = dijkstra.NO_PATH
        else:
            score = distanceFromHeadToTail + distanceFromSourceToHead

        if self.sd[tail] is None or self.sd[tail] > score:
            self.sd[tail] = score


def readAdjacencyListLine(line):
    """
    Read line of adjacency list and returns delimitted line
    """
    for i in range(len(line)):
        line[i] = line[i].split(',')

    return line


def convert_to_int(lists):
    for i in range(len(lists)):
        if lists[i] == '':
            lists[i] = None
        elif not isinstance(lists[i], list):
            lists[i] = int(lists[i])
        else:
            lists[i] = convert_to_int(lists[i])

    return lists


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("invalid usage: python3 dijkstra.py <file of graph>")
        sys.exit(1)

    graphFile = open(sys.argv[1])
    content_list = list(csv.reader(graphFile, delimiter='\t'))

    for line in content_list:
        line = readAdjacencyListLine(line)

    content_list = convert_to_int(content_list)

    COMPUTED_VERTICES = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]

    shortestPaths = dijkstra(content_list, COMPUTED_VERTICES)
    shortestPaths.computeShortestPath()

    res_list = [shortestPaths.sd[i] for i in COMPUTED_VERTICES]
    print(res_list)

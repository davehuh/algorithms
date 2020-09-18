"""
Copyright 2020 Dave Huh
Clustering algorithm
"""

import sys
from functools import total_ordering
import heapq


class Node:
    def __init__(self, key):
        self.key = key


@total_ordering
class Edge:
    def __init__(self, v1, v2, cost):
        self.v1 = v1
        self.v2 = v2
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.cost == other.cost


class Graph:
    def __init__(self):
        self.edges = []
        self.nodes = set()

    def buildGraph(self, listGraph):
        for edge in listGraph:
            v1 = edge[0]
            v2 = edge[1]
            cost = edge[2]
            self.nodes.update([v1, v2])
            edge = Edge(v1, v2, cost)
            heapq.heappush(self.edges, edge)


class Cluster:
    def __init__(self, k, graph):
        self.k = k
        self.graph = graph
        self.clusters = []

    def foundMaximumSpacing(self, edge):
        v1 = edge.v1
        v2 = edge.v2
        if v1 in self.clusters and v2 in self.clusters:  # disjoint sets
            return True
        elif v1 in self.clusters:
            for key, values in self.clusters.items():
                if not values:
                    continue
                if key != v1 and v2 in values:
                    return True
        elif v2 in self.clusters:
            for key, values in self.clusters.items():
                if not values:
                    continue
                if key != v2 and v1 in values:
                    return True
        else:
            foundV1 = False
            foundV2 = False
            for key, values in self.clusters.items():
                if not values:
                    continue
                if v1 in values and v2 not in values:
                    foundV1 = True
                elif v2 in values and v1 not in values:
                    foundV2 = True
            return foundV1 and foundV2
        return False

    def checkSum(self):
        numberNodes = 0
        for key, values in self.clusters.items():
            numberNodes += 1
            if values:
                numberNodes += len(values)

        return numberNodes


    def buildCluster(self):
        edges = self.graph.edges
        self.clusters = dict.fromkeys(self.graph.nodes, None)
        while len(edges) > 0:
            edge = heapq.heappop(edges)
            v1 = edge.v1
            v2 = edge.v2

#            print(v1, v2, edge.cost)
#            print("num of clusters: ", len(self.clusters))

            # stopping condition
            if len(self.clusters) == k:
#                print("stopping cost: ", edge.cost)
                stop = self.foundMaximumSpacing(edge)
                if stop:
#                    print("final clusters: ", self.clusters)
                    return edge.cost
                else:
                    continue

            if v1 in self.clusters and v2 in self.clusters:
                if self.clusters[v1]:
                    self.clusters[v1].add(v2)
                else:
                    self.clusters[v1] = {v2}

                if self.clusters[v2]:
                    self.clusters[v1].update(list(self.clusters[v2]))
                self.clusters.pop(v2, None)
            elif v1 in self.clusters:
                if self.clusters[v1] and v2 in self.clusters[v1]:
                    continue
                for key, values in self.clusters.items():
                    if key != v1 and values and v2 in values:
                        if self.clusters[v1]:
                            self.clusters[v1].add(key)
                            self.clusters[v1].update(list(values))
                        else:
                            self.clusters[v1] = {key}
                            self.clusters[v1].update(list(values))
                        self.clusters.pop(key, None)
                        break
            elif v2 in self.clusters:
                if self.clusters[v2] and v1 in self.clusters[v2]:
                    continue
                for key, values in self.clusters.items():
                    if key != v2 and values and v1 in values:
                        if self.clusters[v2]:
                            self.clusters[v2].add(key)
                            self.clusters[v2].update(list(values))
                        else:
                            self.clusters[v2] = {key}
                            self.clusters[v2].update(list(values))
                        self.clusters.pop(key, None)
                        break
            else:
                v1Key = -1
                v2Key = -1
                for key, values in self.clusters.items():
                    if values and v1 in values:
                        v1Key = key
                    if values and v2 in values:
                        v2Key = key
                if v1Key != v2Key:
                    self.clusters[v1Key].add(v2Key)
                    self.clusters[v1Key].update(list(self.clusters[v2Key]))
                    self.clusters.pop(v2Key)

#            print("end clusters: ", self.clusters)

        return edge.cost


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 cluster.py <file name>")
        sys.exit(1)

    textFile = open(sys.argv[1])
    textFile = textFile.read().splitlines()
    numNodes = textFile.pop(0)
    list_graph = [list(map(int, ele.strip().split(" "))) for ele in textFile]
    graph = Graph()
    graph.buildGraph(list_graph)

    k = 4  # a priori number of clusters
    clusters = Cluster(k, graph)
    max_spacing = clusters.buildCluster()
    checkSum = clusters.checkSum()
    print("k: ", k)
    print("check sum: ", numNodes, "=? ", checkSum)
    print("max spacing: ", max_spacing)

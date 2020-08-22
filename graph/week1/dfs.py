"""
Copyright 2020 Dave Huh
"""

import sys


class Vertex:
    """
    Vertex in a graph
    """
    def __init__(self, value, edges=None):
        self.value = value
        self.edges = edges  # contains a list of keys
        self.explored = False
        self.ts = 0  # topological sort ranking
        self.ft = 0  # finishing time

    def addEdges(self, edges):
        if self.edges:
            self.edges = self.edges + edges
        else:
            self.edges = edges


class Graph:
    """
    A graph with vertexes and edges
    """
    def __init__(self):
        self.graph = None

    def buildGraph(self, al):
        """
        Build a graph from adjacency list
        """
        if not al:
            print("invalid input")
            sys.exit(1)

        # create vertexes
        for line in al:
            value = line[0]
            edges = line[1:]

            # check self.graph has met prerequisites for new insertions
            neededGraphLength = max(line)
            if not self.graph:
                self.graph = [None]*neededGraphLength
            elif len(self.graph) < neededGraphLength:
                self.graph = self.graph + [None] * (neededGraphLength -
                                                    len(self.graph))

            # check if vertex with value exists
            vertex = self.graph[value - 1]
            if vertex:
                vertex.addEdges(edges)
            else:
                self.graph[value - 1] = Vertex(value, edges)

            # check if vertex with edge values exist
            if edges:
                for edge in edges:
                    newEdgeVertex = self.graph[edge - 1]
                    if not newEdgeVertex:
                        self.graph[edge - 1] = Vertex(edge)

#   TODO
#        for vertex in self.graph:
#            print("vertex: ", vertex.value, " edges: ", vertex.edges)

        return self.graph


class DFS:
    """
    Depth first search algorithm
    """
    def __init__(self):
        self.currentLabel = 0
        self.numberOfNodeProcessed = 0
        self.sccMemberPopulationList = []
        self.sccCurrentLeader = None

    def search(self, graphList, start):
        """
        performs depth first search
        Input:
            graphList is a list form of a graph in adjacency form
            start is the index of a starting vertex in integer
        """
        node = graphList[start - 1]

        if self.sccCurrentLeader:
            self.sccMemberPopulationList[-1] += 1

        node.explored = True

        if node.edges:
            for edge in node.edges:
                vertex = graphList[edge - 1]
                if vertex and not vertex.explored:
                    self.search(graphList, edge)

        # for topological sorting
        node.ts = self.currentLabel
        self.currentLabel -= 1

        # for computing strongly connected components
        self.numberOfNodeProcessed += 1
        node.ft = self.numberOfNodeProcessed

    def scc(self, graphList):
        """
        find strongly connected components of directed acylic graph
        Input:
            graphList: a graph object
        Output:
            sccMemberPopulationList: a list of strongly components
            where elements represents number of
            members in a particular community
        """
        # First DFS Loop to compute finishing times
        for key in reversed(range(1, len(graphList) + 1)):
            node = graphList[key - 1]
            if node and not node.explored:
                self.search(graphList, key)

        graphReversed = reverseGraph(graphList)

#   TODO
#        for vertex in graphReversed:
#            print("rev vertex: ", vertex.value, " edges: ", vertex.edges)

        # Second DFS Loop to compute communities and their pop
        for key in reversed(range(1, len(graphReversed) + 1)):
            node = graphReversed[key - 1]
            if node and not node.explored:
                self.sccCurrentLeader = node.value
                self.sccMemberPopulationList.append(0)

                self.search(graphReversed, key)

        self.sccMemberPopulationList.sort(reverse=True)

        if len(self.sccMemberPopulationList) > 5:
            self.sccMemberPopulationList = self.sccMemberPopulationList[:5]

        return self.sccMemberPopulationList

    def topologicalSort(self, graphList):
        self.currentLabel = len(graphList)
        for vertex in graphList:
            if not vertex.explored:
                self.search(graphList, vertex.value)


def reverseGraph(graphList):
    """
    Reverses directed edges of graph. And renames node values with
    finishing times.
    This is a preprocessing step for Kasuraju's strongly connected
    component algorithm.
    Input:
        graphList is a graph in adjacency list form
    Output:
        a graph that has nodes renamed with finishing times and directed
        edges reversed
    """
    newGraph = [None]*len(graphList)

    # create copies of new vertexes to a new graph
    for node in graphList:
        newNodeValue = node.ft
        if not newGraph[newNodeValue - 1]:
            newVertex = Vertex(newNodeValue)
            newGraph[newNodeValue - 1] = newVertex
        if node.edges:
            for edge in node.edges:
                newTargetNodeValue = graphList[edge - 1].ft
                if not newGraph[newTargetNodeValue - 1]:
                    newVertex = Vertex(newTargetNodeValue)
                    newVertex.edges = [newNodeValue]
                    newGraph[newTargetNodeValue - 1] = newVertex
                else:
                    vertex = newGraph[newTargetNodeValue - 1]
                    if vertex.edges:
                        vertex.edges.append(newNodeValue)
                    else:
                        vertex.edges = [newNodeValue]

    return newGraph


def buildList(al):
    """
    Build a list from raw adjacency list format
    """
    for lineNum in range(len(al)):
        al[lineNum] = al[lineNum].strip()
        al[lineNum] = list(map(int, al[lineNum].split(' ')))

    return al


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 dfs.py <file name>")
        sys.exit(1)

    textFile = open(sys.argv[1])
    adjacencyList = textFile.read().splitlines()
    adjacencyList = buildList(adjacencyList)
    graph = Graph()
    graph = graph.buildGraph(adjacencyList)
    dfs = DFS()
    # dfs.topologicalSort(graph)
    sccCounts = dfs.scc(graph)
    print(sccCounts)

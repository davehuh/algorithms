"""
Copyright 2020 Dave Huh
Another implementation of breadth first search
"""

import sys

from collections import deque

class Directed_Edge:
    def __init__(self, head, tail):
        """
        Directed edge
        level represents which layer from vertex 1 the tail vertex lies
        """
        self.head = head
        self.tail = tail
        self.layer = None


def bfs(graph, rev_graph, source=1, target=8):
    """
    performs BFS algorithm and returns level where target was found
    reversed graph used as reference to find parent
    """
    queue = deque([source])  # only keys (tail of edge) to graph
    visited = set()  # only keys
    next_level = -1

    while len(queue) > 0:
        curr_vertex = queue.popleft()

        edges = graph[curr_vertex]

        for edge in edges:
            # initialize layer
            if curr_vertex == source:
                edge.layer = 1

            head = edge.head

            if not edge.layer:
                edge.layer = next_level

            # TODO need reversed graph
            # increment next level
            if curr_vertex != source:
                parent = rev_graph[curr_vertex][0].head
                next_level = graph[parent][0].layer + 1

            if head == target:
                return edge.layer

            if head not in visited:
                queue.append(head)

        visited.add(curr_vertex)

    return next_level


#        curr = queue.popleft()
#
#        # TODO
#        if curr == target:
#            return curr_layer
#
#        next_edges = graph[curr]
#
#        for edge in next_edges:
#            tail = edge.tail
#            head = edge.head
#            if head in visited:
#                continue
#            queue.append(head)
#
#            parent_layer = graph[tail][0].layer
#
#            if not parent_layer:
#                graph[tail][0].layer = 0
#
#            if tail == source:
#                edge.layer = 1
#
#            if not edge.layer:
#                edge.layer = parent_layer + 1
#
#            edge.layer = curr_layer
#
#        visited.add(curr)

#    return curr_layer

def build_graph(edge_list, reversed=False):
    """
    build graph dict
    reversed (default=False) build a graph with edges reversed
    """
    graph = {}
    for edge in edge_list:
        tail = edge[0]
        head = edge[1]

        if reversed:
            tail = edge[1]
            head = edge[0]

        new_edge = Directed_Edge(head, tail)

        if tail in graph:
            graph[tail].append(new_edge)
        else:
            graph[tail] = [new_edge]

    return graph

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python second_implementation_bfs.py <file name>")
        sys.exit(1)

    file = open(sys.argv[1], 'r')
    edge_list = file.readlines()
    file.close()

    edge_list = [list(map(int, row.strip().split(' '))) for row in edge_list]

    graph = {}
    graph = build_graph(edge_list)
    rev_graph = build_graph(edge_list, reversed=True)

    print('layer found vertex 8:', bfs(graph, rev_graph))

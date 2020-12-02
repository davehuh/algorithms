"""
Copyright 2020 Dave Huh
Another implementation of strongly connected components
"""

import sys
import threading

from collections import deque

def build_graph_dicts(edges):
    """
    Builds graph and reversed directed graph
    """
    num_nodes = -1
    graph = {}
    graph_rev = {}

    for edge in edges:
        tail = edge[0]
        head = edge[1]

        if tail in graph:
            graph[tail].append(head)
        else:
            graph[tail] = [head]

        if head in graph_rev:
            graph[head].append(tail)
        else:
            graph[head] = [tail]

    num_nodes = len(graph)

    return graph, graph_rev, num_nodes

def DFS1(graph, node):
    """
    Compute finishing times
    """
    global time, visited, finish
    visited.add(node)

    stack = deque([node])

    while len(stack) > 0:
        edge = stack.pop()

        for edge in graph[node]:
            if edge not in visited:
                stack.append(edge)

    finish[time] = node
    time += 1

def DFS_loop1(graph, num_nodes):
    """
    Get finishing times with reversed graph
    """
    global time, visited, finish

    for node in reversed(range(1, num_nodes + 1)):
        if node not in visited:
            DFS1(graph, node)

    return finish


def DFS_loop2(graph, num_nodes):
    """
    Get SCCs
    """
    raise NotImplementedError

def kosaraju(graph, graph_rev, num_nodes):
    """
    Perform two DFS
    """
    finish = DFS_loop1(graph_rev, num_nodes)
    scc = DFS_loop2(graph, num_nodes)

    return scc

def main():
    """
    Main function
    """
    if len(sys.argv) != 2:
        print("Usage: python3 second_implementation_scc.py <file name>")
        sys.exit(1)

    file = open(sys.argv[1], 'r')
    edge_list = file.readlines()
    file.close()

    edge_list = [list(map(int, row.strip().split(' '))) for row in edge_list]

    graph, graph_rev, num_nodes = build_graph_dicts(edge_list)

    scc = kosaraju(graph, graph_rev, num_nodes)



if __name__ == "__main__":
    STACK_SIZE = 67108864  # 64MB stack
    RECURSION_LIMIT = 2 ** 20  # approx 1 mil recursions

    visited = set()
    finish = {}
    time = 0

    threading.stack_size(STACK_SIZE)
    sys.setrecursionlimit(RECURSION_LIMIT)

    thread = threading.Thread(target = main)
    thread.start()

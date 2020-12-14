"""
Copyright 2020 Dave Huh
Find SCC
"""

import sys
import threading

from collections import defaultdict, deque

def build_graphs(file_path):
    """
    :param file_path: path to input file
    :return graph: dict graph
    :return graph_rev: reversed edges of graph
    :nodes: set of nodes
    """
    graph, graph_rev, nodes = defaultdict(list), defaultdict(list), set()

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip().split()
            tail = int(line[0])
            head = int(line[1])
            graph[tail].append(head)
            graph_rev[head].append(tail)
            nodes.add(tail)
            nodes.add(head)

    return graph, graph_rev, nodes

def set_finishing_times():
    """
    set finishing times using reversed graph
    return: mappings of nodes to finishing times
    """
    global nodes, finishing_time_mappings, finishing_time

    finishing_time = len(nodes)
    visited = set()
    finishing_time_mappings = defaultdict(list)

    for node in nodes:
        if node in visited:
            continue
        dfs_1(node, visited)

    return finishing_time_mappings

def find_scc():
    """
    find scc
    """
    global finishing_time_mappings, scc


    nodes_in_order = list(reversed(finishing_time_mappings.keys()))

    scc = defaultdict(list)
    visited = set()

    for node in nodes_in_order:
        if node in visited:
            continue
        scc[node] = set([ node ])
        dfs_2(node, visited)

    return scc

def dfs_2(leader, visited):
    """
    set scc memberships
    """
    global graph, scc

    stack = deque([leader])

    while stack:
        node = stack.pop()
        visited.add(node)

        scc[leader].add(node)

        heads = graph.get(node, [])

        for head in heads:
            if head in visited:
                continue
            stack.append(head)


def dfs_1(leader, visited):
    """
    set finishing times
    """
    global graph_rev, finishing_time, finishing_time_mappings

    stack = deque([leader])

    while stack:
        node = stack.pop()
        visited.add(node)

        heads = graph_rev.get(node, [])

        for head in heads:
            if head in visited:
                continue
            stack.append(head)

        finishing_time_mappings[node] = finishing_time
        finishing_time -= 1


def main():
    """
    main
    """
    global graph, graph_rev, nodes

    graph, graph_rev, nodes = build_graphs(sys.argv[1])

    finishing_time_mappings = set_finishing_times()
    scc = find_scc()
    scc_members_cells = scc.values()

    print("SCC descending sorted:", sorted(list(map(len, scc_members_cells)), reverse=True))


if __name__ == "__main__":

    sys.setrecursionlimit(10**6)
    threading.stack_size(68108864)

    thread = threading.Thread(target=main)
    thread.start()

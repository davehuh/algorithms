import sys
import threading

from collections import defaultdict, deque


def build_graph(file_path):
    """
    build graph
    """
    graph = defaultdict(list)
    graph_rev = defaultdict(list)
    nodes = set()

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip().split()
            head = line[0]
            tail = line[1]

            if head in graph:
                graph[head].append(tail)
            else:
                graph[head] = [tail]

            if tail in graph_rev:
                graph_rev[tail].append(head)
            else:
                graph_rev[tail] = [head]

            if head not in nodes:
                nodes.add(head)
            if tail not in nodes:
                nodes.add(tail)

    return graph, graph_rev, nodes

def set_finishing_orders(graph_rev, nodes):
    """
    From reversed graph, set finishing times
    :param graph_rev: reversed graph
    :param nodes: set of nodes
    :return mapping of finishing times of each node
    """
    global finishing_mapping  # key = vertex, value = order
    visited = set()

    finishing_time = len(nodes)

    finishing_mapping = {}

    for node in nodes:
        if node in visited:
            continue

        finishing_time = dfs_1(graph_rev, node, visited, finishing_time)

    return finishing_mapping

def find_scc(graph):
    """
    calculate scc
    """
    global finishing_mapping  # preserved decreasing finishing order during insertion
    global scc

    scc = {}
    vertices_in_order = sorted(finishing_mapping.keys(), reverse=True)

    visited = set()

    for node in vertices_in_order:
        if node in visited:
            continue

        scc[node] = set(node)
        dfs_2(graph, node, visited)

    return scc

def dfs_2(graph, leader_node, visited):
    """
    second dfs to discover SCC
    :param graph
    :param leader_node: leader of a SCC
    :param visited: a set to track visited vertices
    """
    global scc

    stack = deque([leader_node])

    while stack:
        vertex = stack.pop()
        visited.add(vertex)
        scc[leader_node].add(vertex)

        heads = graph.get(vertex, [])

        for head in heads:
            if head not in visited:
                stack.append(head)


def dfs_1(graph_rev, node, visited, finishing_time):
    """
    dfs 1 to set finishing times
    """
    global finishing_mapping

    stack = deque([node])

    while stack:
        vertex = stack.pop()
        visited.add(vertex)

        heads = graph_rev.get(vertex, [])

        for head in heads:
            if head not in visited:
                stack.append(head)

        finishing_mapping[vertex] = finishing_time
        finishing_time -= 1

    return finishing_time


def main():
    """
    main
    """
    global finishing_mapping
    graph, graph_rev, nodes = build_graph(sys.argv[1])
    finishing_mapping = set_finishing_orders(graph_rev, nodes)
    scc = find_scc(graph)

    lengths_scc = sorted([list(map(len, scc.values()))], reverse=True)
    print("lengths of SCC, in desc:", lengths_scc)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 another_implementation_scc.py <file name>")
        sys.exit(1)

    threading.stack_size(67108864)
    sys.setrecursionlimit(10**6)
    thread = threading.Thread(target=main)
    thread.start()

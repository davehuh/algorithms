"""
Copyright 2020 Dave Huh
2nd implementation of Karger's min cut algorithm
"""

import sys

from random import choice
from copy import deepcopy


def create_graph(adjacency_list):
    """
    Creates graph dict
    """
    graph_dict = {}
    for row in adjacency_list:
        key = row[0]
        edges = row[1:]

        graph_dict[key] = edges

    return graph_dict

def pick_random_edge(graph_dict):
    """
    Choose random edge
    """
    random_vertex = choice(list(graph_dict.keys()))
    random_edge = choice(graph_dict[random_vertex])

    return random_vertex, random_edge

def combine_vertices(graph_dict, v1, v2):
    """
    Combines two vertices and removes self-loops if exist
    Combines to vertex 1 and deletes v2
    Returns updated graph_dict
    """
    edges_v1 = graph_dict[v1]
    edges_v2 = graph_dict[v2]

    graph_dict[v1] = edges_v1
    graph_dict[v1].extend(edges_v2)
    graph_dict[v1] = list(filter((v1).__ne__, graph_dict[v1]))
    graph_dict[v1] = list(filter((v2).__ne__, graph_dict[v1]))

    graph_dict.pop(v2)

    # remove all traces of v2
    remove_keys = set()
    for key in graph_dict:
        if key == v1:
            continue

        if v2 in set(graph_dict[key]):
            graph_dict[key] = [v1 if ele == v2 else ele for ele in graph_dict[key]]

        if len(graph_dict[key]) < 1:
            remove_keys.add(key)

    for key in remove_keys:
        graph_dict.pop(key)

    return graph_dict

def karger(graph_dict):
    """
    Karger's min cut
    """
    while len(graph_dict) > 2:
        v1, v2 = pick_random_edge(graph_dict)
        graph_dict = combine_vertices(graph_dict, v1, v2)

    return graph_dict.values(), min(map(len, graph_dict.values()))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 second_iter_min_cut.py <file name>")
        sys.exit(1)

    file = open(sys.argv[1])
    adjacency_list = file.readlines()
    file.close()

    adjacency_list = [list(map(int, row.strip().split(' '))) for row in adjacency_list]

    graph_dict = create_graph(adjacency_list)

    num_iter = 1000
    min_cut = 10**6

    for iter in range(num_iter):
        graph = deepcopy(graph_dict)
        new_graph, new_min_cut = karger(graph)
        min_cut = min(new_min_cut, min_cut)

    print('min cut:', min_cut)

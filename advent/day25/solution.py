import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache

import numpy.linalg


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()

    connection_dict = {}
    for dline in datatable:
        from_node, other_nodes = dline.strip().split(":")
        other_nodes = other_nodes.split(" ")[1:]
        if from_node not in connection_dict.keys():
            connection_dict[from_node] = set()
        for o_node in other_nodes:
            if o_node not in connection_dict.keys():
                connection_dict[o_node] = set()
        for o_node in other_nodes:
            connection_dict[from_node].add(o_node)
            connection_dict[o_node].add(from_node)

    connection_list = []
    for from_node, val in connection_dict.items():
        for o_node in val:
            if not ((from_node, o_node) in connection_list or (o_node, from_node) in connection_list):
                connection_list.append((from_node, o_node))

    if False:
        for i in range(len(connection_list)):
            node_i = connection_list[i]
            for j in range(i+1, len(connection_list)):
                node_j = connection_list[j]
                for k in range(j+1, len(connection_list)):
                    node_k = connection_list[k]
                    res = walk_network(connection_dict, {
                        node_i[0]: node_i[1], node_i[1]: node_i[0],
                        node_j[0]: node_j[1], node_j[1]: node_j[0],
                        node_k[0]: node_k[1], node_k[1]: node_k[0]
                    })
                    if len(res) > 1:
                        return np.prod([len(resi) for resi in res])

    if False:
        apointsl = 10000
        for i in connection_dict.keys():
            # find arti_points
            visited = dict(zip(connection_dict.keys(), [False] * len(connection_dict)))
            parents = dict(zip(connection_dict.keys(), [None] * len(connection_dict)))
            lowerps = dict(zip(connection_dict.keys(), [100000] * len(connection_dict)))
            discops = dict(zip(connection_dict.keys(), [100000] * len(connection_dict)))

            import sys
            sys.setrecursionlimit(10000)
            def visit_node(nod, iterat):
                children = 0
                visited[nod] = True
                discops[nod] = lowerps[nod] = iterat[0]
                iterat[0] += 1

                for other_n in connection_dict[nod]:
                    if not visited[other_n]:
                        children += 1
                        parents[other_n] = nod
                        visit_node(other_n, iterat)
                        lowerps[nod] = min(lowerps[nod], lowerps[other_n])
            visit_node(i, [0])
            lll = np.array([[lowerps[key], discops[key]] for key in lowerps.keys()])
            apoints = np.min(lll[:, 1][lll[:, 0] > 5])
            apointsl = np.min((apointsl, apoints))
        print(apointsl)
    if False:
        for node in connection_dict.keys():
            walk_network(connection_dict, {}, {node})
    if True:
        from tqdm import tqdm
        for i in tqdm(range(len(connection_list))):
            node_i = connection_list[i]
            for node in connection_dict.keys():
                    walk_network(connection_dict, {node_i[0]: node_i[1], node_i[1]: node_i[0]}, {node})
    return 0


def walk_network(network, remove_connections={}, current_nodes=None):
    past_network = [set()]
    if current_nodes is None:
        current_nodes = {list(network.keys())[0]}
    while np.sum([len(pn) for pn in past_network]) < len(network):
        if len(current_nodes) == 0:
            for node in network.keys():
                if np.all([node not in pn for pn in past_network]):
                    current_nodes.add(node)
            past_network.append(set())
        next_nodes = set()
        for node in current_nodes:
            past_network[-1].add(node)
        for node in current_nodes:
            next_nodes_i = network[node]
            for nnii in next_nodes_i:
                if node in remove_connections.keys():
                    if remove_connections[node] == nnii:
                        continue
                if not nnii in past_network[-1]:
                    next_nodes.add(nnii)
        current_nodes = next_nodes
        if len(current_nodes) == 2 and len(current_nodes) + len(past_network[-1]) != len(network):
            print(current_nodes, len(current_nodes), len(past_network[-1]), len(network))
    return past_network


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 25")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 54
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 527790  # {'znv', 'mtq'}
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

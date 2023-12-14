import re
import numpy as np
from typing import List, Tuple


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    instruction = datatable[0].strip()
    inst_lr = []
    for inst in instruction:
        if inst == "L":
            inst_lr.append(0)
        elif inst == "R":
            inst_lr.append(1)
        else:
            assert False, f"The instruction '{inst_lr}' is not defined."

    network_dict = {}
    for dataline in datatable[2:]:
        node_name, node_connection = dataline.strip().split(" = ")
        assert len(node_name) == 3, f"The node name '{node_name}' doesn't have length 3."
        assert len(node_connection) == 10, f"The node connection '{node_connection}' doesn't have length 10."
        node_con_l, node_con_r = node_connection[1:4], node_connection[6:9]
        network_dict[node_name] = (node_con_l, node_con_r)

    current_node = "AAA"
    steps = 0
    while current_node != "ZZZ":
        current_node = network_dict[current_node][inst_lr[steps % len(inst_lr)]]
        steps += 1
    return steps


def solution2(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    instruction = datatable[0].strip()
    inst_lr = []
    for inst in instruction:
        if inst == "L":
            inst_lr.append(0)
        elif inst == "R":
            inst_lr.append(1)
        else:
            assert False, f"The instruction '{inst_lr}' is not defined."

    network_dict = {}
    for dataline in datatable[2:]:
        node_name, node_connection = dataline.strip().split(" = ")
        assert len(node_name) == 3, f"The node name '{node_name}' doesn't have length 3."
        assert len(node_connection) == 10, f"The node connection '{node_connection}' doesn't have length 10."
        node_con_l, node_con_r = node_connection[1:4], node_connection[6:9]
        network_dict[node_name] = (node_con_l, node_con_r)

    current_nodes = []
    for node_name in network_dict.keys():
        if str(node_name)[2] == "A":
            current_nodes.append(node_name)

    steps_different = []
    for cni, cn in enumerate(current_nodes):
        steps = 0
        while not cn[2] == 'Z':
            cn = network_dict[cn][inst_lr[steps % len(inst_lr)]]
            steps += 1
        steps_different.append(steps)
    lcm = 1
    steps_different = np.array(steps_different, dtype=np.int64)
    for sp in steps_different:
        lcm = np.lcm(lcm, sp)
        print(lcm)
    return np.lcm.reduce(steps_different)


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 8 ")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 6
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 17287
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase2")
    result, result_expected = solution2('test2.txt'), 6
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 18625484023687
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

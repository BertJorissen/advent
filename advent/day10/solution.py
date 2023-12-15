import re
import numpy as np
from typing import List, Tuple


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    datatable = ["." + data_i.strip() + "." for data_i in datatable]
    datatable.insert(0, "." * len(datatable[0]))
    datatable.append("." * len(datatable[0]))
    compas = {
        "north": np.array([-1, 0]),
        "east": np.array([0, 1]),
        "south": np.array([1, 0]),
        "west": np.array([0, -1]),
    }
    move_dict = {
        "|": np.array([
            compas["north"],
            compas["south"]
        ]),
        "-": np.array([
            compas["east"],
            compas["west"]
        ]),
        "L": np.array([
            compas["north"],
            compas["east"]
        ]),
        "J": np.array([
            compas["north"],
            compas["west"]
        ]),
        "7": np.array([
            compas["south"],
            compas["west"]
        ]),
        "F": np.array([
            compas["south"],
            compas["east"]
        ])
    }
    possible = [str(mv) for mv in move_dict.keys()]
    possible.append(".")
    possible.append("S")

    s_loc = np.array([])
    for yi, data_x in enumerate(datatable):
        for xi, data_y in enumerate(data_x):
            assert data_y in possible, f"The key '{data_y}' is weird."
            if data_y == "S":
                assert len(s_loc) == 0, f"There was already an 'S' at '{s_loc}', found one at '{[yi, xi]}'."
                s_loc = np.array([yi, xi])
    paths = [follow_path(datatable, s_loc, sd, move_dict) for sd in np.array([[1,0],[-1,0],[0,1],[0,-1]])]
    return int(np.max(paths) / 2)


def follow_path(datatable, start_pos, start_dir, move_dict):
    steps = 0
    print("==========", start_pos, start_dir)
    while True:
        steps += 1
        start_pos = start_pos + start_dir
        #print(start_pos)
        new_sgn = datatable[start_pos[0]][start_pos[1]]
        if new_sgn == "S":
            return steps
        if new_sgn == ".":
            return -1
        new_dir = move_dict[new_sgn]
        dir_right = np.sum(np.abs(new_dir + start_dir), axis=1) == 0
        if not np.any(dir_right):
            return -1
        start_dir = new_dir[np.logical_not(dir_right)][0]



def solution2(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    datatable = ["." + data_i.strip() + "." for data_i in datatable]
    datatable.insert(0, "." * len(datatable[0]))
    datatable.append("." * len(datatable[0]))
    compas = {
        "north": np.array([-1, 0]),
        "east": np.array([0, 1]),
        "south": np.array([1, 0]),
        "west": np.array([0, -1]),
    }
    move_dict = {
        "|": np.array([
            compas["north"],
            compas["south"]
        ]),
        "-": np.array([
            compas["east"],
            compas["west"]
        ]),
        "L": np.array([
            compas["north"],
            compas["east"]
        ]),
        "J": np.array([
            compas["north"],
            compas["west"]
        ]),
        "7": np.array([
            compas["south"],
            compas["west"]
        ]),
        "F": np.array([
            compas["south"],
            compas["east"]
        ])
    }
    possible = [str(mv) for mv in move_dict.keys()]
    possible.append(".")
    possible.append("S")

    s_loc = np.array([])
    for yi, data_x in enumerate(datatable):
        for xi, data_y in enumerate(data_x):
            assert data_y in possible, f"The key '{data_y}' is weird."
            if data_y == "S":
                assert len(s_loc) == 0, f"There was already an 'S' at '{s_loc}', found one at '{[yi, xi]}'."
                s_loc = np.array([yi, xi])
    paths = [follow_path2(datatable, s_loc, sd, move_dict) for sd in np.array([[1,0],[-1,0],[0,1],[0,-1]])]
    path_lengths = [p[0] for p in paths]
    path_idx = np.argmax(path_lengths)
    h_dir = np.array(paths[path_idx][1])
    h_pos = np.array(paths[path_idx][2])
    return int((np.abs(np.sum([np.cross(h_pos[i], h_dir[i]) for i in range(len(h_dir))])) - path_lengths[path_idx] + 2) / 2)

def follow_path2(datatable, start_pos, start_dir, move_dict):
    steps = 0
    print("==========", start_pos, start_dir)
    h_dir = []
    h_pos = []
    while True:
        steps += 1
        h_dir.append(start_dir)
        h_pos.append(start_pos)
        start_pos = start_pos + start_dir
        #print(start_pos)
        new_sgn = datatable[start_pos[0]][start_pos[1]]
        if new_sgn == "S":
            return steps, h_dir, h_pos
        if new_sgn == ".":
            return -1, h_dir, h_pos
        new_dir = move_dict[new_sgn]
        dir_right = np.sum(np.abs(new_dir + start_dir), axis=1) == 0
        if not np.any(dir_right):
            return -1, h_dir, h_pos
        start_dir = new_dir[np.logical_not(dir_right)][0]


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 10 ")
    print("================")
    print("")
    print(" - testcase A")
    result, result_expected = solution('test.txt'), 4
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase B")
    result, result_expected = solution('testB.txt'), 8
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 6714
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2A")
    result, result_expected = solution2('test2.txt'), 4
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2B")
    result, result_expected = solution2('test2B.txt'), 8
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2C")
    result, result_expected = solution2('test2C.txt'), 10
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 429
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

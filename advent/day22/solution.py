import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    assignment_table = np.zeros((len(datatable), 2, 3), dtype=np.int64)
    for li, dline in enumerate(datatable):
        for si, ss in enumerate(dline.strip().split("~")):
            for xyi, xy in enumerate(ss.split(",")):
                assignment_table[li, si, xyi] = int(xy)
        if np.any(assignment_table[li, 0, :] > assignment_table[li, 1, :]):
            assignment_table[li] = np.flip(assignment_table[li], axis=0)
        assert np.any(assignment_table[li, 0, :] <= assignment_table[li, 1, :]), "Ordering problem."

    dependency_table = {}

    def look_down(block, cti):
        ltl = len(assignment_table)
        if ltl > 0:
            x_in_area_l = np.max((assignment_table[:, 0, 0], block[0, 0] * np.ones(ltl)), axis=0)
            x_in_area_u = np.min((assignment_table[:, 1, 0], block[1, 0] * np.ones(ltl)), axis=0)
            y_in_area_l = np.max((assignment_table[:, 0, 1], block[0, 1] * np.ones(ltl)), axis=0)
            y_in_area_u = np.min((assignment_table[:, 1, 1], block[1, 1] * np.ones(ltl)), axis=0)
            xy_table = np.logical_and(x_in_area_l <= x_in_area_u, y_in_area_l <= y_in_area_u)
            zu_table = assignment_table[:, 1, 2] < block[0, 2]
            dependency_table[cti] = np.arange(ltl)[np.logical_and(xy_table, zu_table)]
        else:
            dependency_table[cti] = []

    for ati, at in enumerate(assignment_table):
        look_down(at, ati)

    z_coord = np.zeros(len(datatable), dtype=int)
    z_found = set()
    connection_dict = {}

    while not np.all(z_coord > 0):
        for key, item in dependency_table.items():
            if key not in z_found:
                if len(item) == 0:
                    z_found.add(key)
                    z_coord[key] = 1 + assignment_table[key, 1, 2] - assignment_table[key, 0, 2]
                    connection_dict[key] = []
                elif np.all([i in z_found for i in item]):
                    z_found.add(key)
                    z_max = int(np.max(z_coord[item]))
                    tmp = []
                    for ite in item:
                        if z_coord[ite] == z_max:
                            tmp.append(ite)
                    connection_dict[key] = tmp.copy()
                    z_coord[key] = z_max + 1 + assignment_table[key, 1, 2] - assignment_table[key, 0, 2]

    counter = set()
    for ati in range(len(datatable)):
        tmp = True
        tmpf = False
        tmpff = True
        for item in connection_dict.values():
            if ati in item:
                tmp = False
                if len(item) == 1:
                    tmpff = False
                    break
                else:
                    tmpf = True
        if tmp or tmpf:
            if tmpff:
                counter.add(ati)
    return len(counter)



def solution2(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    assignment_table = np.zeros((len(datatable), 2, 3), dtype=np.int64)
    for li, dline in enumerate(datatable):
        for si, ss in enumerate(dline.strip().split("~")):
            for xyi, xy in enumerate(ss.split(",")):
                assignment_table[li, si, xyi] = int(xy)
        if np.any(assignment_table[li, 0, :] > assignment_table[li, 1, :]):
            assignment_table[li] = np.flip(assignment_table[li], axis=0)
        assert np.any(assignment_table[li, 0, :] <= assignment_table[li, 1, :]), "Ordering problem."

    dependency_table = {}

    def look_down(block, cti):
        ltl = len(assignment_table)
        if ltl > 0:
            x_in_area_l = np.max((assignment_table[:, 0, 0], block[0, 0] * np.ones(ltl)), axis=0)
            x_in_area_u = np.min((assignment_table[:, 1, 0], block[1, 0] * np.ones(ltl)), axis=0)
            y_in_area_l = np.max((assignment_table[:, 0, 1], block[0, 1] * np.ones(ltl)), axis=0)
            y_in_area_u = np.min((assignment_table[:, 1, 1], block[1, 1] * np.ones(ltl)), axis=0)
            xy_table = np.logical_and(x_in_area_l <= x_in_area_u, y_in_area_l <= y_in_area_u)
            zu_table = assignment_table[:, 1, 2] < block[0, 2]
            dependency_table[cti] = np.arange(ltl)[np.logical_and(xy_table, zu_table)]
        else:
            dependency_table[cti] = []

    for ati, at in enumerate(assignment_table):
        look_down(at, ati)

    z_coord = np.zeros(len(datatable), dtype=int)
    z_found = set()
    connection_dict = {}

    while not np.all(z_coord > 0):
        for key, item in dependency_table.items():
            if key not in z_found:
                if len(item) == 0:
                    z_found.add(key)
                    z_coord[key] = 1 + assignment_table[key, 1, 2] - assignment_table[key, 0, 2]
                    connection_dict[key] = []
                elif np.all([i in z_found for i in item]):
                    z_found.add(key)
                    z_max = int(np.max(z_coord[item]))
                    tmp = []
                    for ite in item:
                        if z_coord[ite] == z_max:
                            tmp.append(ite)
                    connection_dict[key] = tmp.copy()
                    z_coord[key] = z_max + 1 + assignment_table[key, 1, 2] - assignment_table[key, 0, 2]

    counter = set()
    falling_table = {}
    for ati in range(len(datatable)):
        tmp = True
        tmpf = False
        tmpff = True
        falling_table[ati] = []
        for ii, item in connection_dict.items():
            if ati in item:
                tmp = False
                falling_table[ati].append(ii)
                if len(item) == 1:
                    tmpff = False
                else:
                    tmpf = True
        if tmp or tmpf:
            if tmpff:
                counter.add(ati)

    out_removed = []
    for bi in range(len(datatable)):
        rem_bl = set()
        def remove_blocks(ci):
            remove_now = falling_table[ci]
            call_later = set()
            rem_bl.add(ci)
            for rn in remove_now:
                if np.all([s in rem_bl for s in connection_dict[rn]]):
                    call_later.add(rn)
            for cl in call_later:
                remove_blocks(cl)
        remove_blocks(bi)
        out_removed.append(len(rem_bl)-1)
    return np.sum(out_removed)


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 22")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 5
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 434
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    result, result_expected = solution2('test.txt'), 7
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 61209
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

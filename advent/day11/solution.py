import re
import numpy as np
from typing import List, Tuple

def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    datatable = [data_i.strip() for data_i in datatable]
    allowed_keys = ".#"
    for dataline in datatable:
        for datai in dataline:
            if datai not in allowed_keys:
                assert False, f"The key '{datai}' is not an allowed key."
    data_buffer = []
    for dataline in datatable:
        if "."*len(dataline) == dataline:
            data_buffer.append(dataline)
        data_buffer.append(dataline)
    data_buffer2 = transpose_data(data_buffer)
    db2 = []
    for dataline in data_buffer2:
        if "."*len(dataline) == dataline:
            db2.append(dataline)
        db2.append(dataline)
    data_expanded = transpose_data(db2)

    star = []
    for yi, dataline in enumerate(data_expanded):
        for xi, datai in enumerate(dataline):
            if datai == "#":
                star.append(np.array([xi, yi]))
    s_len = len(star)
    total_len = 0
    for s_i, stari in enumerate(star):
        for s_j in range(s_len - s_i - 1):
            ss_j = (s_len - 1) - s_j
            starj = star[ss_j]
            total_len += np.sum(np.abs(stari-starj))
    return total_len


def transpose_data(datatable):
    databuffer = [[0 for _ in range(len(datatable))] for _ in range(len(datatable[0]))]
    for dli, dataline in enumerate(datatable):
        for ldi, datai in enumerate(dataline):
            databuffer[ldi][dli] = datai
    db = []
    for dataline in databuffer:
        db.append("".join(dataline))
    return db


def solution2(filename: str = "data.txt", expansion: int = 1000000-1) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    datatable = [data_i.strip() for data_i in datatable]
    allowed_keys = ".#"
    for dataline in datatable:
        for datai in dataline:
            if datai not in allowed_keys:
                assert False, f"The key '{datai}' is not an allowed key."
    row_addition = []
    for yi, dataline in enumerate(datatable):
        if "."*len(dataline) == dataline:
            row_addition.append(yi)
    col_addition = []
    for xi, dataline in enumerate(transpose_data(datatable)):
        if "."*len(dataline) == dataline:
            col_addition.append(xi)

    star = []
    for yi, dataline in enumerate(datatable):
        for xi, datai in enumerate(dataline):
            if datai == "#":
                star.append(np.array([xi, yi]))
    s_len = len(star)
    total_len = np.array(0, dtype=np.int64)
    for s_i, stari in enumerate(star):
        for s_j in range(s_len - s_i - 1):
            ss_j = (s_len - 1) - s_j
            starj = star[ss_j]
            total_len += np.sum(np.abs(stari-starj))
            total_len += expansion * amount_between(starj[1], stari[1], row_addition)
            total_len += expansion * amount_between(starj[0], stari[0], col_addition)
    return total_len


def amount_between(pos1, pos2, gravlist):
    gravlist = np.array(gravlist)
    pos_min, pos_max = np.min([pos1, pos2]), np.max([pos1, pos2])
    amount = np.sum(np.logical_and(gravlist < pos_max, gravlist > pos_min))
    return amount

if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 11 ")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 374
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 10289334
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    result, result_expected = solution2('test.txt', 9), 1030
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2B")
    result, result_expected = solution2('test.txt', 99), 8410
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 649862989626
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

import re
import numpy as np
from typing import List, Tuple


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    data_array = np.array([[int(d) for d in dataline.strip().split(" ")] for dataline in datatable])
    total = 0
    for dataline in data_array:
        last_digit = []
        tmp_data = dataline
        last_digit.append(tmp_data[-1])
        for _ in range(len(datatable)):
            if np.sum(np.abs(tmp_data)) == 0:
                break
            tmp_data = np.diff(tmp_data)
            last_digit.append(tmp_data[-1])
        total += np.cumsum(last_digit)[-1]
    return total


def solution2(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    data_array = np.array([[int(d) for d in dataline.strip().split(" ")] for dataline in datatable])
    total = 0
    for dataline in data_array:
        first_digit = []
        tmp_data = dataline
        first_digit.append(tmp_data[0])
        for _ in range(len(datatable)):
            if np.sum(np.abs(tmp_data)) == 0:
                break
            tmp_data = np.diff(tmp_data)
            first_digit.append(tmp_data[0])
        ti = 0
        for ts in np.flip(first_digit):
            ti = ts - ti
        total += ti
    return total


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 9 ")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 114
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 1641934234
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase2")
    result, result_expected = solution2('test.txt'), 2
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 975
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

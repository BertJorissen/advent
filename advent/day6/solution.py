import re
import numpy as np
from typing import List, Tuple


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    datatable = [dataline.strip().split(" ") for dataline in datatable]
    data_read = []
    for dataline in datatable:
        data_buffer = []
        for data_part in dataline:
            if not data_part == "":
                data_buffer.append(data_part)
        data_read.append(data_buffer)
    assert data_read[0][0] == "Time:", \
        f"The input file doesn't have the right syntax: {data_read[0][0]} != 'Time:'"
    assert data_read[1][0] == "Distance:", \
        f"The input file doesn't have the right syntax: {data_read[1][0]} != 'Distance:'"
    times = [int(data_part) for data_part in data_read[0][1:]]
    dists = [int(data_part) for data_part in data_read[1][1:]]
    return int(np.prod([find_times(time, dist, 1) for time, dist in zip(times, dists)]))

def solution2(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    datatable = [dataline.strip().split(" ") for dataline in datatable]
    data_read = []
    for dataline in datatable:
        data_buffer = []
        for data_part in dataline:
            if not data_part == "":
                data_buffer.append(data_part)
        data_read.append(data_buffer)
    assert data_read[0][0] == "Time:", \
        f"The input file doesn't have the right syntax: {data_read[0][0]} != 'Time:'"
    assert data_read[1][0] == "Distance:", \
        f"The input file doesn't have the right syntax: {data_read[1][0]} != 'Distance:'"
    time = int("".join(data_read[0][1:]))
    dist = int("".join(data_read[1][1:]))
    return int(find_times(time, dist, 1))


def find_times(time, dist, acceleration) -> int:
    eps = 10**-10
    eq_a, eq_b, eq_c = acceleration, -time * acceleration, dist
    discriminant = eq_b ** 2 - 4 * eq_a * eq_c
    if discriminant < 0:
        print("ok")
        return 0
    t_min = ((-eq_b - np.sqrt(discriminant)) / (2 * acceleration)) + eps
    t_max = ((-eq_b + np.sqrt(discriminant)) / (2 * acceleration)) - eps
    return np.floor(t_max) - np.ceil(t_min) + 1


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 6 ")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 288
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 2756160
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase2")
    result, result_expected = solution2('test.txt'), 71503
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 34788142
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
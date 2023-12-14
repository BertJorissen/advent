import re
import numpy as np
from typing import List, Tuple


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    datatable = [dataline.strip() for dataline in datatable]
    datatable.append("")
    split_table = split_in_sections(datatable)

    title_line = split_table[0][0].split(" ")
    assert title_line[0] == "seeds:", f"Input '{title_line[0]}' not expected, expected 'seeds:'"
    seeds = [int(seed) for seed in title_line[1:]]

    start_title = "seed"
    all_tables = []
    seed_list = [seeds]
    for table_one in split_table[1:]:
        all_tables.append(analyze_one_table(table_one, start_title))
        start_title = all_tables[-1][1][1]
        seed_tmp = []
        for seed in seed_list[-1]:
            seed_tmp.append(table_new_index(seed, all_tables[-1][0]))
        seed_list.append(seed_tmp)
    return np.min(seed_list[-1])


def split_in_sections(input_string: List[str]) -> List[List[str]]:
    output_data = []
    buffer = []
    for dataline in input_string:
        if dataline == "":
            output_data.append(buffer)
            buffer = []
        else:
            buffer.append(dataline)
    return output_data


def analyze_one_table(input_string: List[str], title_in: str) -> Tuple[np.ndarray, Tuple[str, str]]:
    title = input_string[0].split(" ")
    assert title[1] == "map:", f"Input '{title[1]}' not expected, expected 'map:'"
    title_name = title[0].split("-")
    assert title_name[1] == "to", f"Input '{title_name[1]}' not expected, expected 'to:'"
    assert title_name[0] == title_in, f"Input '{title_name[0]}' not expected, expected '{title_in}:'"
    data_array = np.array([[int(data_one) for data_one in dataline.split(" ")] for dataline in input_string[1:]])
    data_array = data_array[np.argsort(data_array[:, 1]), :]
    return data_array, (title_name[0], title_name[2])


def table_new_index(seed: int, table: np.ndarray) -> int:
    index_nearest = find_nearest_index(table[:, 1], seed)
    if index_nearest == -1:
        return seed
    bound_rescale = table[index_nearest, 1] + table[index_nearest, 2] - 1
    out = seed
    if seed <= bound_rescale:
        out = table[index_nearest, 0] + seed - table[index_nearest, 1]
    return out


def solution2(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    datatable = [dataline.strip() for dataline in datatable]
    datatable.append("")
    split_table = split_in_sections(datatable)

    title_line = split_table[0][0].split(" ")
    assert title_line[0] == "seeds:", f"Input '{title_line[0]}' not expected, expected 'seeds:'"
    seeds = [(int(title_line[1:][seed_i*2]), int(title_line[1:][seed_i*2+1]))
             for seed_i in range(len(title_line[1:]) // 2)]

    start_title = "seed"
    all_tables = []
    seed_list = [seeds]
    for table_one in split_table[1:]:
        all_tables.append(analyze_one_table(table_one, start_title))
        start_title = all_tables[-1][1][1]
        seed_tmp = []
        for seeds in seed_list[-1]:
            out_list = table_new_index2(seeds[0], seeds[1], all_tables[-1][0])
            for combina in out_list:
                seed_tmp.append(combina)
        seed_list.append(seed_tmp)
        seeds_in, seeds_out = np.sum(np.array(seed_list[-2])[:, 1]), np.sum(np.array(seed_list[-1])[:, 1])
        assert seeds_in == seeds_out, f"Different amount of seeds for {start_title}: {seeds_in} != {seeds_out}"
    return np.min(np.array(seed_list[-1])[:, 0])


def table_new_index2(seed: int, seed_range: int, table: np.ndarray) -> List[Tuple[int, int]]:
    # see if it is below any boundary
    index_nearest = find_nearest_index(table[:, 1], seed)
    out_list = []
    seed_range_in = seed_range

    # below any boundary
    if index_nearest == -1:
        # same values only until next range
        nearest_border = table[0, 1] - 1
        destination = seed
        certain_range, (seed, seed_range) = find_distance_to_boundary(seed, seed_range, destination, nearest_border)
        out_list.append(certain_range)

    while seed_range > 0:
        index_nearest = find_nearest_index(table[:, 1], seed)
        nearest_border = table[index_nearest, 1] + table[index_nearest, 2] - 1
        if nearest_border < seed:
            if index_nearest + 1 == len(table[:, 1]):
                out_list.append((seed, seed_range))
                return out_list
            nearest_border = table[index_nearest + 1, 1] - 1
            destination = seed
        else:
            destination = table[index_nearest, 0] + seed - table[index_nearest, 1]
        certain_range, (seed, seed_range) = find_distance_to_boundary(seed, seed_range, destination, nearest_border)
        out_list.append(certain_range)
    assert seed_range_in == np.sum(np.atleast_2d(out_list)[:, 1]), f"seed range and length are not same, {seed_range_in} != {np.sum(np.atleast_2d(out_list)[:, 1])}"
    return out_list


def find_distance_to_boundary(seed, seed_range, destination, boundary) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    distance_to_boundary = boundary - seed + 1
    certain_range = (destination, np.min((seed_range, distance_to_boundary)))
    next_range = (boundary + 1, seed_range - distance_to_boundary)
    return certain_range, next_range


def find_nearest_index(list_search: np.ndarray, number: int) -> int:
    index_nearest = np.argmin(np.abs(list_search - number))
    if not list_search[index_nearest] <= number:
        index_nearest = index_nearest - 1
    return index_nearest


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 5 ")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 35
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 551761867
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase2")
    result, result_expected = solution2('test.txt'), 46
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 57451709
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
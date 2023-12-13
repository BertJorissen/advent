import re
import numpy as np


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    return np.sum([right_game_numbers(line.strip()) for line in datatable])


def right_game_numbers(input_string: str) -> int:
    rgb_ints = dict(zip(["red", "green", "blue"], [12, 13, 14]))
    game_id = int(input_string.split(" ")[1][:-1])
    game_content = "-".join(input_string.split(" ")[2:])
    game_split = game_content.split(";")
    for game_i, game_line in enumerate(game_split):
        game_line.split(",")
        for combination in game_line.split(","):
            if combination[0] == "-":
                combination = combination[1:]
            comb_num, comb_name = combination.split("-")
            if int(comb_num) > rgb_ints[comb_name]:
                print(f"Game {game_i} is not right, {comb_num} for {comb_name}.")
                return 0
    print(f"Game {game_id} is right.")
    return game_id


def solution2(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    return np.sum([right_game_numbers2(line.strip()) for line in datatable])


def right_game_numbers2(input_string: str) -> int:
    rgb_ints = dict(zip(["red", "green", "blue"], [0, 0, 0]))
    game_id = int(input_string.split(" ")[1][:-1])
    game_content = "-".join(input_string.split(" ")[2:])
    game_split = game_content.split(";")
    for game_i, game_line in enumerate(game_split):
        game_line.split(",")
        for combination in game_line.split(","):
            if combination[0] == "-":
                combination = combination[1:]
            comb_num, comb_name = combination.split("-")
            comb_num = int(comb_num)
            if comb_num > rgb_ints[comb_name]:
                rgb_ints[comb_name] = comb_num
    product_out = np.prod(list(rgb_ints.values()))
    print(f"Game {game_id} is right, R {rgb_ints['red']}, G {rgb_ints['green']}, R {rgb_ints['red']} - {product_out}")
    return product_out


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 2 ")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 8
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 54632
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase2")
    result, result_expected = solution2('test.txt'), 2286
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 72227
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
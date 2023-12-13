import re
import numpy as np


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    return np.sum([right_game_numbers(line.strip()) for line in datatable])


def right_game_numbers(input_string: str) -> int:
    #print(input_string)
    game_id = int(input_string.split(" ", 1)[1].strip().split()[0][:-1])
    #print(game_id)
    game_content = input_string.split(" ", 2)[-1]
    winning_numbers, my_numbers = game_content.split("|")
    winning_numbers = re.sub(r'\s+', ' ', winning_numbers).strip().split(" ")
    my_numbers = re.sub(r'\s+', ' ', my_numbers).strip().split(" ")

    lucky = 0
    for my_n in my_numbers:
        if my_n in winning_numbers:
            lucky = lucky + 1
    return 2 ** (lucky-1) if lucky != 0 else 0

def solution2(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    winning = np.zeros(len(datatable))
    for line in datatable:
        input_string = line.strip()
        #print(input_string)
        game_id = int(input_string.split(" ", 1)[1].strip().split()[0][:-1])
        #print(game_id)
        game_content = input_string.split(" ", 2)[-1]
        winning_numbers, my_numbers = game_content.split("|")
        winning_numbers = re.sub(r'\s+', ' ', winning_numbers).strip().split(" ")
        my_numbers = re.sub(r'\s+', ' ', my_numbers).strip().split(" ")

        lucky = 0
        for my_n in my_numbers:
            if my_n in winning_numbers:
                lucky = lucky + 1

        previous_cards = winning[game_id - 1] + 1
        winning[game_id - 1] = previous_cards
        if lucky != 0:
            for win_i in range(lucky):
                win_k = win_i + 1 + game_id - 1
                winning[win_k] = winning[win_k] + previous_cards

    #print(winning)
    return int(np.sum(winning))


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 4 ")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 13
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 21158
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase2")
    result, result_expected = solution2('test.txt'), 30
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 6050769
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
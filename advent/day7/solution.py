import re
import numpy as np
from typing import List, Tuple


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    datatable = [dataline.strip().split(" ") for dataline in datatable]
    cards_choice = "AKQJT98765432"
    cards_value = list(map(chr, range(97, 97+len(cards_choice))))
    data_array = [[] for _ in range(7)]
    for dataline in datatable:
        card, number = dataline[:2]
        assert len(card) == 5, f"The card {card} doens't have length 5"
        for i_c, card_i in enumerate(card):
            assert card_i in cards_choice, f"The card {card} has a weird letter '{card_i}' in position {i_c}."
        number = int(number)
        card_class = find_card_class(card)
        card_value = rename_card(card, cards_choice, cards_value)
        data_array[card_class-1].append((card_value, card, number))

    data_cost_sorted = [sorted(dataline, key=lambda x: x[0]) for dataline in data_array]
    costs = np.hstack([[data_v[2] for data_v in dv] for dv in data_cost_sorted])
    return int(np.sum(costs * (len(costs) - np.arange(len(costs)))))


def rename_card(card, cards_choice, cards_value):
    card_out = []
    for card_i in card:
        for cards_c_i, cards_c in enumerate(cards_choice):
            if card_i == cards_c:
                card_out.append(cards_value[cards_c_i])
    return "".join(card_out)


def find_card_class(card) -> int:
    # 1 - five of a kind    [5]
    # 2 - four of a kind    [1, 4]
    # 3 - full house        [2, 3]
    # 4 - three of a kind   [1, 1, 3]
    # 5 - two pair          [1, 2, 2]
    # 6 - one pair          [1, 1, 1, 2]
    # 7 - high card         [1, 1, 1, 1, 1]

    card_unique = set(card)
    card_counts = np.sort([card.count(card_key) for card_key in card_unique]).tolist()
    if card_counts == [5]:
        return 1
    elif card_counts == [1, 4]:
        return 2
    elif card_counts == [2, 3]:
        return 3
    elif card_counts == [1, 1, 3]:
        return 4
    elif card_counts == [1, 2, 2]:
        return 5
    elif card_counts == [1, 1, 1, 2]:
        return 6
    elif card_counts == [1, 1, 1, 1, 1]:
        return 7
    else:
        assert False, f"This card seems to be doing weird things: {card} -> {card_counts}"


def solution2(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    datatable = [dataline.strip().split(" ") for dataline in datatable]
    cards_choice = "AKQT98765432J"
    card_joker = "J"
    cards_value = list(map(chr, range(97, 97+len(cards_choice))))
    data_array = [[] for _ in range(7)]
    for dataline in datatable:
        card, number = dataline[:2]
        assert len(card) == 5, f"The card {card} doens't have length 5"
        for i_c, card_i in enumerate(card):
            assert card_i in cards_choice, f"The card {card} has a weird letter '{card_i}' in position {i_c}."
        number = int(number)
        card_class = find_card_class2(card, cards_choice, card_joker)
        card_value = rename_card(card, cards_choice, cards_value)
        data_array[card_class-1].append((card_value, card, number))

    data_cost_sorted = [sorted(dataline, key=lambda x: x[0]) for dataline in data_array]
    costs = np.hstack([[data_v[2] for data_v in dv] for dv in data_cost_sorted])
    return int(np.sum(costs * (len(costs) - np.arange(len(costs)))))


def find_card_class2(card, cards_choice, card_joker) -> int:
    # 1 - five of a kind    [5]
    # 2 - four of a kind    [1, 4]
    # 3 - full house        [2, 3]
    # 4 - three of a kind   [1, 1, 3]
    # 5 - two pair          [1, 2, 2]
    # 6 - one pair          [1, 1, 1, 2]
    # 7 - high card         [1, 1, 1, 1, 1]

    cards_normal = []
    for card_c in cards_choice:
        if card_c not in card_joker:
            cards_normal.append(card_c)


    hand_normal, hand_joker = [], []
    for card_i in card:
        if card_i in card_joker:
            hand_joker.append(card_i)
        elif card_i in cards_normal:
            hand_normal.append(card_i)
        else:
            assert False, f"The card '{card_i}' is not in the joker nor hand cards."

    card_unique = set(hand_normal)
    card_counts = np.sort([card.count(card_key) for card_key in card_unique]).tolist()
    joker_unigue = set(hand_joker)
    joker_counts = np.sort([card.count(card_key) for card_key in joker_unigue]).tolist()
    if len(card_counts) == 0:
        card_counts = [int(np.sum(joker_counts))]
    else:
        card_counts[-1] += int(np.sum(joker_counts))
    if card_counts == [5]:
        return 1
    elif card_counts == [1, 4]:
        return 2
    elif card_counts == [2, 3]:
        return 3
    elif card_counts == [1, 1, 3]:
        return 4
    elif card_counts == [1, 2, 2]:
        return 5
    elif card_counts == [1, 1, 1, 2]:
        return 6
    elif card_counts == [1, 1, 1, 1, 1]:
        return 7
    else:
        assert False, f"This card seems to be doing weird things: {card} -> {card_counts}"


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 7 ")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 6440
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 247815719
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase2")
    result, result_expected = solution2('test.txt'), 5905
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 248747492
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
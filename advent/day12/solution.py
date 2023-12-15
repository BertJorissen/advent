import re
import numpy as np
from typing import List, Tuple, Optional


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    return np.sum([process_line(data_i.strip()) for data_i in datatable])


def process_line(dataline):
    allowed_keys = ".#?"
    springs, ledger = dataline.split(" ")

    for spring in springs:
        if spring not in allowed_keys:
            assert False, f"The key '{spring}' is not an allowed key."

    springs_broken = []
    for spring_group in springs.split("."):
        if spring_group != '':
            springs_broken.append(spring_group)

    ledger = [int(springi) for springi in ledger.split(",")]
    combinations = dist_over_groups(springs_broken, ledger)
    counts = 0
    for combination in combinations:
        counts += np.prod([amount_of_combinations(sb, cn) for (sb, cn) in zip(springs_broken, combination)])
        print(counts, '----', springs_broken, combination, [amount_of_combinations(sb, cn) for (sb, cn) in zip(springs_broken, combination)])
    return counts


def dist_over_groups(groups: List[str], ledger: List[int]) -> Optional[List[List[List[int]]]]:
    # distribute the ledger over the groups
    first_group = groups[0]
    # stopping criteria, only one group left
    if len(groups) == 1:
        if np.sum(ledger) + len(ledger) - 1 <= len(first_group):  # is the group the right size?
            return [[ledger]]
        else:
            return None
    else:
        # multiple groups, take a look at the first group
        other_groups = groups[1:]
        fgl = len(first_group)
        led_len = 0

        buffer = []
        # first ignore this group
        result_other = dist_over_groups(other_groups, ledger)
        if result_other is not None:
            for res_o in result_other:
                buf_i = [[]]
                for ri in res_o:
                    buf_i.append(ri)
                buffer.append(buf_i)
        for led_i, led in enumerate(ledger):
            if led_i > 0:
                led_len += 1
            led_len += led
            if not led_len <= fgl:
                break
            result_other = dist_over_groups(other_groups, ledger[led_i+1:])
            if result_other is not None:
                for res_o in result_other:
                    buf_i = [ledger[:led_i+1]]
                    for ri in res_o:
                        buf_i.append(ri)
                    buffer.append(buf_i)
        if buffer == []:
            return None
        return buffer


def amount_of_combinations(spring_group, counts):
    print("   ////  ", spring_group, counts)
    allowed_keys = "#?"
    for spring in spring_group:
        if spring not in allowed_keys:
            assert False, f"The key '{spring}' is not an allowed key."

    # not enough springs for ledger, i.e.: "???", [1,3]
    if len(spring_group) < np.sum(counts) + len(counts) - 1:
        return 0

    # size lines op neatly, just give it back directly, i.e.: "???", [1,1]
    if np.sum(counts) + len(counts) - 1 == len(spring_group):
        pos_count = -1
        for count in counts[:-1]:
            pos_count += count + 1
            if spring_group[pos_count] != "?":
                # there is a spring in a border, i.e. "?#?", [1,1]; can't subdivide
                return 0
        return 1

    # ledger is empty
    if len(counts) == 0:
        # There is a spring, give back zero, i.e. "??#", []
        if "#" in spring_group:
            return 0
        # They are all optional, give back one as it only has one combination, i.e. "???", []
        else:
            return 1

    # So, there is a ledger, find the position of the first spring
    fspring = first_spring(spring_group)

    # All optional, i.e. "???", [1]
    if fspring == -1:
        # Find the leftover positions, i.e. "????", [1, 1]  -> one position left over
        left_over = len(spring_group) - (np.sum(counts) + len(counts) - 1)
        n_groups = len(counts) + 1
        return n_choose_k_2(n_groups, left_over)
    elif fspring == 0:
        # The first spring is in the first location, so there is only one place to go to, i.e. "#????", [2, 1]
        if spring_group[counts[0]] == "#":
            # There is a spring on the border, so zero, i.e. "#?#??", [2, 1]
            return 0
        else:
            return 1 * amount_of_combinations(spring_group[counts[0] + 1:], counts[1:])
    else:
        # There is a padding between the first spring and the counts, i.e. "?#????", [2, 1]
        if fspring <= counts[0]:
            # The first spring is withing the edge and the counts, i.e. "?#????", [2, 1]
            counter = 0
            for ci in range(fspring + 1):
                print("rrrr", spring_group, fspring, counts, ci)
                if len(spring_group) <= ci + counts[0] + 1:
                    counter += 1
                else:
                    if spring_group[ci + counts[0]] == "#":
                        # There is a spring on the border, so zero, i.e. "#?#??", [2, 1]
                        counter += 0
                    else:
                        print("ffffffff", spring_group[ci + counts[0] + 1:])
                        if spring_group[ci + counts[0] + 1:] == "":
                            print("llllllllll")
                            counter += 1
                        else:
                            counter += 1 * amount_of_combinations(spring_group[ci + counts[0] + 1:], counts[1:])
            return counter
        else:
            # The first spring is further away from the edge, i.e. "???#????", [2, 1]
            counter = 0
            for ci in range(fspring - counts[0]):
                counter += 1 * amount_of_combinations(spring_group[ci + counts[0] + 1:], counts[1:])
            return counter


def n_choose_k(n, k):
    return int(np.math.factorial(int(n)) / (np.math.factorial(int(k)) * np.math.factorial(int(n - k))))


def n_choose_k_2(n, k):
    return n_choose_k(n + k - 1, k)


def first_spring(spring_group):
    for s, spring in enumerate(spring_group):
        if spring == "#":
            return s
    return -1


def first_spring_len(spring_group):
    for s, spring in enumerate(spring_group[first_spring(spring_group):]):
        if spring == "?":
            return s
    return len(spring_group[first_spring(spring_group):])


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 12 ")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 21
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 7613
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    #result, result_expected = solution2('test.txt', 9), 1030
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    #result, result_expected = solution2(), 649862989626
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

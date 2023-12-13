import re
import numpy as np


def solution(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    datatable = ["." + data_i.strip() + "." for data_i in datatable]
    datatable.insert(0, "." * len(datatable[0]))
    datatable.append("." * len(datatable[0]))
    #[print(f" {data_i} ") for data_i in datatable]

    digits = [str(i) for i in range(10)]
    symbols = [str(i) for i in range(10)]
    symbols.append(".")
    totalsum = 0
    for line_i in range(len(datatable) - 2):
        keep = False
        digi = 0
        lin_i = line_i + 1
        for str_i, digit in enumerate(datatable[lin_i]):
            st_i = str_i + 1
            if digit in digits:
                digi = digi * 10 + int(digit)
                if np.any([datatable[lin_i+(col_i-1)][st_i+(row_i-2)] not in symbols
                           for col_i in range(3) for row_i in range(3)]):
                    keep = True
            else:
                if digi != 0:
                    if keep:
                        totalsum = totalsum + digi
                    digi = 0
                    keep = False
    return totalsum

def solution2(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    datatable = ["." + data_i.strip() + "." for data_i in datatable]
    datatable.insert(0, "." * len(datatable[0]))
    datatable.append("." * len(datatable[0]))
    #[print(f" {data_i} ") for data_i in datatable]

    digits = [str(i) for i in range(10)]
    symbols = ["*"]
    totals = {}
    for line_i in range(len(datatable) - 2):
        keep = []
        digi = 0
        lin_i = line_i + 1
        for str_i, digit in enumerate(datatable[lin_i]):
            if digit in digits:
                digi = digi * 10 + int(digit)
                for col_i in range(3):
                    for row_i in range(3):
                        index_pos = lin_i+(col_i-1), str_i+(row_i-1)
                        gear_p = datatable[index_pos[0]][index_pos[1]]
                        if gear_p in symbols:
                            if index_pos not in keep:
                                keep.append(index_pos)
            else:
                if digi != 0:
                    for index_k in keep:
                        if str(index_k[0]) not in totals.keys():
                            totals[str(index_k[0])] = {}
                        if str(index_k[1]) not in totals[str(index_k[0])].keys():
                            totals[str(index_k[0])][str(index_k[1])] = []
                        totals[str(index_k[0])][str(index_k[1])].append(digi)
                    digi = 0
                    keep = []
    totalsum = 0
    for index_k, val_k in totals.items():
        for inkex_j, val_k in val_k.items():
            if len(val_k) == 2:
                totalsum = totalsum + np.prod(val_k)
    return totalsum

if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 3 ")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 4361
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 530495
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase2")
    result, result_expected = solution2('test.txt'), 467835
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 80253814
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
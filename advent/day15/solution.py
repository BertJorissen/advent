import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache

def solution(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    d = datatable[0].strip().split(',')
    return np.sum([ch(l) for l in d])
    

def ch(s: str) -> int:
    out = 0
    for k in s:
        out += ord(k)
        out = out * 17
        out = out % 256
    return out


def solution2(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    d = datatable[0].strip().split(',')
    steps: List[Tuple[str, int, bool, int]] = [process_one(l) for l in d]
    boxes: List[List[List[str, int]]] = [[] for _ in range(256)]
    for (label, hashstr, operation, lens) in steps:
        if operation:
            added = False
            for lci, lens_comb in enumerate(boxes[hashstr]):
                if label == lens_comb[0]:
                    boxes[hashstr][lci][1] = lens
                    added = True
                    break
            if not added:
                boxes[hashstr].append([label, lens])
        else:
            for lci, lens_comb in enumerate(boxes[hashstr]):
                if label == lens_comb[0]:
                    boxes[hashstr].pop(lci)
                    break
    counter = 0
    for boxi, box in enumerate(boxes):
        for lensi, (_, lens) in enumerate(box):
            counter += (boxi+1) * (lensi+1) * lens
    return counter


def process_one(inpt: str) -> Tuple[str, int, bool, int]:
    alphabet = list(map(chr, range(97, 97+26)))
    allowed_keys = "-="
    label = ""
    operation = False
    lens = -1
    hashstr = -1
    for si, s in enumerate(inpt):
        if s in alphabet:
            label = label + s
        elif s in allowed_keys:
            operation = s == "="
            hashstr = ch(label)
            if operation:
                lens = int(inpt[si+1:])
            break
        else:
            assert False, f"The key '{s}' in position {si} in '{inpt}' seems to behave weirdly."
    return label, hashstr, operation, lens


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 15")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 1320
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 495972
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    result, result_expected = solution2('test.txt'), 145
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 245223
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

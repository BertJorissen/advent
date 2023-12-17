import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache

def solution(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    data_all = []
    buffer = []
    for dataline in datatable:
        dataline = dataline.strip()
        if dataline is not "":
            buffer.append(dataline)
        else:
            data_all.append(buffer)
            buffer = []
    if buffer is not []:
        data_all.append(buffer)
    if not smudge:
        return np.sum([process_mirror(mirror) for mirror in data_all])
    else:
        return np.sum([pre_process_horizontal(mirror) for mirror in data_all])


def transform(mirror) -> np.ndarray:
    allowed_keys = ".#"
    mmatrix = []
    for mline in mirror:
        matmlin = []
        for mkey in mline:
            assert mkey in allowed_keys, f"The key '{mkey} is not allowed."
            matmlin.append(mkey == ".")
        mmatrix.append(matmlin)
    mmatrix = np.array(mmatrix)
    m_x_len = mmatrix.shape[1]
    assert np.all(m_x_len == np.array([len(mline) for mline in mirror])), "Not all mirrors have the same length."
    return mmatrix


def process_mirror(mmatrix) -> int:
    mmatrix = transform(mmatrix)
    return process_horizontal(mmatrix)[0] * 100 + process_horizontal(mmatrix.T)[0]


def process_horizontal(mirror: np.ndarray) -> Tuple[int, List[int], List[List[int]]]:
    already_mirror = 0
    mirror_list = []
    mrznge_lidt = []
    for mirror_line in range(1, mirror.shape[0]):
        mrange = np.min((mirror_line, mirror.shape[0]-mirror_line))
        if np.all(mirror[mirror_line-mrange:mirror_line] == np.flip(mirror[mirror_line:mirror_line+mrange], axis=0)):
            mirror_list.append(mirror_line)
            already_mirror += mirror_line
            mrznge_lidt.append(np.arange(mirror_line-mrange+1, mirror_line+mrange+1).tolist())
    return already_mirror, mirror_list, mrznge_lidt


def pre_process_horizontal(mirror: np.ndarray) -> int:
    mirror = transform(mirror)
    couter = 0
    mirror = mirror.T
    for multply in [1, 100]:
        idxll = process_horizontal(mirror)[0]
        ccs = set([])
        for idx in range(mirror.shape[0]):
            for idy in range(mirror.shape[1]):
                mirror[idx, idy] = not mirror[idx, idy]
                _, gg1, gg2 = process_horizontal(mirror*1)
                for g1, g2 in zip(gg1, gg2):
                    if idx+1 in g2:
                        print(idx+1, g1, g2)
                        ccs.add(g1)
                mirror[idx, idy] = not mirror[idx, idy]
        couter += np.sum(list(ccs)) * multply
        mirror = mirror.T
        print(ccs, idxll)
    return couter

if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 13 ")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 405
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 34993
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    result, result_expected = solution('test.txt', smudge=True), 400
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution(smudge=True), 29341
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

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
    if smudge:
        return np.sum([process_mirror(mirror) for mirror in data_all])
    else:
        return np.sum([pre_process_mirror(mirror) for mirror in data_all])

def process_mirror(mirror) -> int:
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

    return process_horizontal(mmatrix) * 100 + process_horizontal(mmatrix.T)

def process_horizontal(mirror: np.ndarray) -> int:
    already_mirror = 0
    for mirror_line in range(1, mirror.shape[0]):
        mrange = np.min((mirror_line, mirror.shape[0]-mirror_line))
        if np.all(mirror[mirror_line-mrange:mirror_line] == np.flip(mirror[mirror_line:mirror_line+mrange], axis=0)):
            if already_mirror != 0:
                print(f"there already was a mirror, {mirror}")
            already_mirror += mirror_line
    return already_mirror


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
    #result, result_expected = solution('test.txt', smudge=True), 400
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    #result, result_expected = solution2(smudge=True), 649862989626
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

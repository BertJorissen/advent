import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache

def solution(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    ddt = dict(zip("UDRL",np.array([[1,0],[-1,0],[0,1],[0,-1]])))
    omt, opp, pos = 0, 0, np.array([0,0])
    pozl = []
    for dl in datatable:
        dtn, dit, hxd = dl.strip().split(" ")
        dtn, dit = ddt[dtn], int(dit)
        omt += dit
        opp += np.cross(pos,dit*dtn)
        #for dtni in range(dit):
        #    nnn = pos+dtn*(1+dtni)
        #    for pp in pozl:
        #        if np.all(pp==nnn):
        #            print(nnn)
        #    pozl.append(nnn)
        pos += dit*dtn
    print(omt, pos, opp)
    return int(np.abs(opp)/2 + omt/2 +1)


def solution2(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    ddt = np.array([[1,0],[0,-1],[-1,0],[0,1]])
    omt, opp, pos = 0, 0, np.array([0,0])
    pozl = []
    for dl in datatable:
        _, _, hxd = dl.strip().split(" ")
        
        dtn, dit = ddt[int(hxd[7])], int(hxd[2:7], 16)
        omt += dit
        opp += np.cross(pos,dit*dtn)
        #for dtni in range(dit):
        #    nnn = pos+dtn*(1+dtni)
        #    for pp in pozl:
        #        if np.all(pp==nnn):
        #            print(nnn)
        #    pozl.append(nnn)
        pos += dit*dtn
    print(omt, pos, opp)
    return int(np.abs(opp)/2 + omt/2 +1)


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 18")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 62
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 70026
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    result, result_expected = solution2('test.txt'), 952408144115
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 68548301037382
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

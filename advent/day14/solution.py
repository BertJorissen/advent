import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache

def solution(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    lookup_dict = dict(zip(['.','#','O'],[1,2,3]))

    matrix = []
    for dataline in datatable:
        dataline = dataline.strip()
        buffer = []
        for data in dataline:
            buffer.append(lookup_dict[data])
        matrix.append(buffer)
    matrix = np.array(matrix)
    return np.sum([count_column(process_column(tuple(lined))) for lined in matrix.T])
    

def solution2(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    lookup_dict = dict(zip(['.','#','O'],[1,2,3]))

    matrix = []
    for dataline in datatable:
        dataline = dataline.strip()
        buffer = []
        for data in dataline:
            buffer.append(lookup_dict[data])
        matrix.append(buffer)
    matrix = np.array(matrix)

    for i in range(2000): #range(1000000000):
        # north
        #printm(matrix)
        matrix = np.array([process_column(tuple(lined)) for lined in matrix.T], dtype=int).T
        # west
        #printm(matrix)
        matrix = np.array([process_column(tuple(lined)) for lined in matrix], dtype=int)
        # south
        #printm(matrix)
        matrix = np.flip(np.array([process_column(tuple(lined)) for lined in np.flip(matrix).T], dtype=int)).T
        # east
        #printm(matrix)    
        matrix = np.flip(np.array([process_column(tuple(lined)) for lined in np.flip(matrix)], dtype=int))
         
        out = np.sum([count_column(l) for l in matrix.T])
        #print('n: ', out)
        #print('e: ', np.sum([count_column(l) for l in np.flip(matrix)]))
        #print('s: ', np.sum([count_column(l) for l in np.flip(matrix).T]))
        #print('w: ', np.sum([count_column(l) for l in matrix]))
        #print('-: ', np.sum(matrix==3))
        #printm(matrix) 
        print('======', i, out)
    #print(matrix)
    return out

def printm(matrix):
    out = np.sum([count_column(l) for l in matrix.T])
    print('n: ', out)
    print('e: ', np.sum([count_column(l) for l in np.flip(matrix)]))
    print('s: ', np.sum([count_column(l) for l in np.flip(matrix).T]))
    print('w: ', np.sum([count_column(l) for l in matrix]))
    print('-: ', np.sum(matrix==3))
    
    
@cache
def process_column(column):
    col_place = 0
    out = np.ones(len(column))
    for di, dd in enumerate(column):
        if dd == 3:
            assert out[col_place] == 1, "Wrong symbol on line"
            out[col_place] = 3
            col_place += 1
        elif dd == 2:
            col_place = di + 1
            out[di] = 2
        elif dd == 1:
            gg = 1
        else:
            assert False, "This shouldn't happen"
    #print(column, out)
    return out


def count_column(column):
    return np.sum(np.flip(np.arange(1, len(column)+1))[column==3])


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 14")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 136
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 111339
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    result, result_expected = solution2('test.txt'), 64
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 93736
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache

def solution(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    data = np.array([[int(d) for d in l.strip()] for l in datatable], dtype=int)
    dy, dx = data.shape
    steps = np.zeros((dy, dx), dtype=int)
    
    idics = np.zeros((dy, dx, 4, 3), dtype=int)
    moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    perps = [[2, 3], [ 2, 3], [0, 1], [0,  1]]
    def one_step(xi, yi):
        for mi in range(4):
            sx, sy = moves[mi]
            for mj in range(3):
                rx,ry = xi+sx,yi+sy
                if rx<0 or ry<0 or rx>=dx or ry>=dy:
                    break
                mk = idics[yi, xi, mi, mj]
                if mk > 0:
                    ml = mk + data[ry,rx]
                    for pi in perps[mi]:
                        for i in range(3):
                            ppp = idics[ry,rx,pi,i]
                            if ppp== 0 or ppp > ml:
                                idics[ry,rx,pi,i] = ml
                    for i in range(mj):
                        ppp = idics[ry,rx,mi,i]
                        if ppp == 0 or ppp > ml:
                            idics[ry,rx,mi,i] = ml
    idics[0,0,0,:] = data[0,0]
    ddd = data[0,0]
    cc, dc, mi = 0, -1, 0
    while mi<39 or dc!=0:
        for _ in range(3):
            for yi in range(dy):
                for xi in range(dx):
                    one_step(xi, yi)
            costi = np.min(idics[-1,-1])-ddd
            dc = cc-costi
            cc = costi
            mi += 1
            print(mi, cc, dc)
    return cc

def solution2(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    data = np.array([[int(d) for d in l.strip()] for l in datatable], dtype=int)
    dy, dx = data.shape
    steps = np.zeros((dy, dx), dtype=int)
    
    idics = np.zeros((dy, dx, 4, 10), dtype=int)
    moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    perps = [[2, 3], [ 2, 3], [0, 1], [0,  1]]
    def one_step(xi, yi):
        for mi in range(4):
            sx, sy = moves[mi]
            for mj in range(10):
                rx,ry = xi+sx,yi+sy
                if rx<0 or ry<0 or rx>=dx or ry>=dy:
                    break
                mk = idics[yi, xi, mi, mj]
                if mk > 0:
                    ml = mk + data[ry,rx]
                    if mj == 0:
                        for pi in perps[mi]:
                            for i in range(7):
                                ppp = idics[ry,rx,pi,3+i]
                                if ppp== 0 or ppp > ml:
                                    idics[ry,rx,pi,3+i] = ml
                    else:
                        ppp = idics[ry,rx,mi,mj-1]
                        if ppp==0 or ppp > ml:
                            idics[ry,rx,mi,mj-1] = ml
    idics[0,0,0,4:] = data[0,0]
    ddd = data[0,0]
    cc, dc, mi = 0, -1, 0
    while mi<40  or dc!=0:
        for _ in range(3):
            for yi in range(dy):
                for xi in range(dx):
                    one_step(xi, yi)
            costi = idics[-1,-1,:,0]-ddd
            costi[costi==-ddd] = 1000000
            costi = np.min(costi)
            dc = cc-costi
            cc = costi
            mi += 1
            print(mi, cc, dc)
    idics[idics==0]=100000000
    print(idics[-1,-1])
    print(np.min(np.min(idics[:,:,:],axis=2),axis=2))
    return cc


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 17")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 102
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 1256
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    result, result_expected = solution2('test.txt'), 94
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2b")
    result, result_expected = solution2('test2.txt'), 71
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 1382
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

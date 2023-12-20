import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache

def solution(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    allowed_keys = r".-|\/"
    ad = dict(zip(allowed_keys, list(range(len(allowed_keys)))))
    mirror = np.zeros((len(datatable), len(datatable[0].strip())), dtype=int)
    for di, dataline in enumerate(datatable):
        tmpline = []
        for dj, datai in enumerate(dataline.strip()):
            assert datai in allowed_keys, f"The key {datai} is unexpected."
            mirror[di, dj] = ad[datai]
    ms = mirror.shape
    lt = np.array([[0, 1, 2], [3, 0, 0], [4, 0, 0]],dtype=int)
    tl = np.array([[0, 0], [0, 1], [0, -1], [1, 0], [-1, 0]],dtype=int)
    tt = (
        ([],[2],[1],[4],[3]),
        ([],[2],[1],[1,2],[1,2]),
        ([],[3,4],[3,4],[4],[3]),
        ([],[4],[3],[2],[1]),
        ([],[3],[4],[1],[2])
    )
    ml = np.zeros((5, *ms), dtype=bool)
    print(ms)
    import sys
    sys.setrecursionlimit(10000)
    def cm(point, pdir, mlist):
        nep, pen = point + pdir, lt[pdir[0],pdir[1]]
        print(nep, pen)
        if not (np.any(nep<0) or np.any(nep>=ms)):
            if not mlist[pen,nep[0],nep[1]]:
                mlist[pen,nep[0],nep[1]] = True
                mtt = tt[mirror[nep[0],nep[1]]][pen]
                for nnp in mtt:
                    mlist[nnp,nep[0],nep[1]] = True
                for nnp in mtt:
                    mlist = np.logical_or(mlist, cm(nep, -tl[nnp], mlist)) 
        return mlist
    gg = cm(np.array([0,-1],dtype=int),np.array([0,1],dtype=int),ml) 
    #print(gg*1)
    #print(np.sum(gg,axis=0))
    return np.sum(np.sum(gg,axis=0)>0)


def solution2(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    allowed_keys = r".-|\/"
    ad = dict(zip(allowed_keys, list(range(len(allowed_keys)))))
    mirror = np.zeros((len(datatable), len(datatable[0].strip())), dtype=int)
    for di, dataline in enumerate(datatable):
        tmpline = []
        for dj, datai in enumerate(dataline.strip()):
            assert datai in allowed_keys, f"The key {datai} is unexpected."
            mirror[di, dj] = ad[datai]
    ms = mirror.shape
    lt = np.array([[0, 1, 2], [3, 0, 0], [4, 0, 0]],dtype=int)
    tl = np.array([[0, 0], [0, 1], [0, -1], [1, 0], [-1, 0]],dtype=int)
    tt = (
        ([],[2],[1],[4],[3]),
        ([],[2],[1],[1,2],[1,2]),
        ([],[3,4],[3,4],[4],[3]),
        ([],[4],[3],[2],[1]),
        ([],[3],[4],[1],[2])
    )
    ml = np.zeros((5, *ms), dtype=bool)
    print(ms)
    import sys
    sys.setrecursionlimit(10000)
    def cm(point, pdir, mlist):
        nep, pen = point + pdir, lt[pdir[0],pdir[1]]
        #print(nep, pen)
        if not (np.any(nep<0) or np.any(nep>=ms)):
            if not mlist[pen,nep[0],nep[1]]:
                mlist[pen,nep[0],nep[1]] = True
                mtt = tt[mirror[nep[0],nep[1]]][pen]
                for nnp in mtt:
                    mlist[nnp,nep[0],nep[1]] = True
                for nnp in mtt:
                    mlist = np.logical_or(mlist, cm(nep, -tl[nnp], mlist)) 
        return mlist
    out = [
            [0 for _ in range(ms[0])],
            [0 for _ in range(ms[0])],
            [0 for _ in range(ms[1])],
            [0 for _ in range(ms[1])]
    ]

    for itl in range(4):
        for ik in range(ms[itl//2]):
            if True:#out[itl][ik] == 0:
                if itl == 0:
                    posn=np.array([ik,-1],dtype=int)
                elif itl == 1:
                    posn=np.array([ik,ms[1]],dtype=int)
                elif itl == 2:
                    posn=np.array([-1,ik],dtype=int)
                elif itl == 3:
                    posn=np.array([ms[0],ik],dtype=int)
                gg = cm(posn,tl[itl+1],np.zeros((5, *ms), dtype=bool))
                count = np.sum(np.sum(gg,axis=0)>0)
                for ki, kk in enumerate([gg[1][:,0],gg[2][:,-1],gg[3][0,:],gg[4][-1,:]]):
                    
                    for li, ll in enumerate(kk):
                        if ll:
                            print(ki,li)
                            out[ki][li] = np.max((count, out[ki][li]))

    #print(gg*1)
    #print(np.sum(gg,axis=0))
    print([np.argmax(oo) for oo in out])
    print(out)
    return np.max([np.max(oo) for oo in out])


def solution(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    allowed_keys = r".-|\/"
    ad = dict(zip(allowed_keys, list(range(len(allowed_keys)))))
    mirror = np.zeros((len(datatable), len(datatable[0].strip())), dtype=int)
    for di, dataline in enumerate(datatable):
        tmpline = []
        for dj, datai in enumerate(dataline.strip()):
            assert datai in allowed_keys, f"The key {datai} is unexpected."
            mirror[di, dj] = ad[datai]
    ms = mirror.shape
    lt = np.array([[0, 1, 2], [3, 0, 0], [4, 0, 0]],dtype=int)
    tl = np.array([[0, 0], [0, 1], [0, -1], [1, 0], [-1, 0]],dtype=int)
    tt = (
        ([],[2],[1],[4],[3]),
        ([],[2],[1],[1,2],[1,2]),
        ([],[3,4],[3,4],[4],[3]),
        ([],[4],[3],[2],[1]),
        ([],[3],[4],[1],[2])
    )
    ml = np.zeros((5, *ms), dtype=bool)
    print(ms)
    import sys
    sys.setrecursionlimit(10000)
    def cm(point, pdir, mlist):
        nep, pen = point + pdir, lt[pdir[0],pdir[1]]
        print(nep, pen)
        if not (np.any(nep<0) or np.any(nep>=ms)):
            if not mlist[pen,nep[0],nep[1]]:
                mlist[pen,nep[0],nep[1]] = True
                mtt = tt[mirror[nep[0],nep[1]]][pen]
                for nnp in mtt:
                    mlist[nnp,nep[0],nep[1]] = True
                for nnp in mtt:
                    mlist = np.logical_or(mlist, cm(nep, -tl[nnp], mlist)) 
        return mlist
    gg = cm(np.array([0,-1],dtype=int),np.array([0,1],dtype=int),ml) 
    #print(gg*1)
    #print(np.sum(gg,axis=0))
    return np.sum(np.sum(gg,axis=0)>0)



if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 16")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 46
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 6994
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    result, result_expected = solution2('test.txt'), 51
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 7488
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

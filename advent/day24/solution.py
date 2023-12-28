import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache

import numpy.linalg


def solution(filename: str = "data.txt", short=None) -> int:
    if short is None:
        short = (np.array(200000000000000, np.int64), np.array(400000000000000, np.int64))
    with open(filename, "r") as data:
        datatable = data.readlines()
    dll = len(datatable)
    pos = np.zeros((dll, 3), np.int64)
    vel = np.zeros((dll, 3), np.int64)

    for dli, dline in enumerate(datatable):
        dline = dline.strip()
        posi, veli = dline.split("@")
        for ii, (pii, vii) in enumerate(zip(posi.split(","), veli.split(","))):
            pos[dli, ii] = int(pii)
            vel[dli, ii] = int(vii)

    # p = r + v * t

    # p1 = r1 + v1 * t1
    # p2 = r2 + v2 * t2

    # v1 * a - v2 * b = r2 - r1

    def find_one(posa, posb, vela, velb):
        dv = np.array(vela[1] * velb[0] - vela[0] * velb[1], dtype=np.float64)
        if dv == 0:
            return None
        t1 = ((posa[1] - posb[1]) * velb[0] - (posa[0] - posb[0]) * velb[1]) / dv
        t2 = ((posa[1] - posb[1]) * vela[0] - (posa[0] - posb[0]) * vela[1]) / dv
        return np.array([-t1, -t2], dtype=np.float64)

    counter = 0
    for pf, (pos_f, vel_f) in enumerate(zip(pos, vel)):
        for ps, (pos_s, vel_s) in enumerate(zip(pos[pf+1:], vel[pf+1:])):
            timefs = find_one(pos_f[:2], pos_s[:2], vel_f[:2], vel_s[:2])
            if timefs is None:
                continue
            if np.all(timefs >= 0):
                posxy0 = pos_f + vel_f * timefs[0]
                posxy = pos_s + vel_s * timefs[1]
                assert np.any(np.abs((posxy[:2] - posxy0[:2])/ posxy[:2]) < 1e-10), f"The positions are not the same, {posxy} != {posxy0}"
                if np.all(np.logical_and(short[0] <= posxy[:2], posxy[:2] <= short[1])):
                    counter += 1
    return counter


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def pfac(n):
    pn = prime_factors(n)
    out = dict(zip(pn, [0 for _ in range(len(pn))]))
    for pp in pn:
        m = n * 1
        while m % pp == 0:
            m = m // pp
            out[pp] += 1
    return out


def other_lcm(n):
    nf = [pfac(int(abs(ni))) for ni in n]
    k = set(nf[0].keys())
    k = k.intersection(*[set(nf[ki].keys()) for ki in range(1, len(n))])
    d = dict(zip(k, [0 for _ in range(len(k))]))
    for ki in k:
        d[ki] = np.min([nfi[ki] for nfi in nf])
    o = 1
    for item, val in d.items():
        o *= int(item) ** int(val)
    return o


def solution2(filename: str = "data.txt") -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    dll = len(datatable)
    pos = np.zeros((dll, 3), np.int64)
    vel = np.zeros((dll, 3), np.int64)

    for dli, dline in enumerate(datatable):
        dline = dline.strip()
        posi, veli = dline.split("@")
        for ii, (pii, vii) in enumerate(zip(posi.split(","), veli.split(","))):
            pos[dli, ii] = int(pii)
            vel[dli, ii] = int(vii)

    dictt = [{}, {}, {}]
    for ixyz in range(3):
        for p_i, v in enumerate(vel[:, ixyz]):
            if v not in dictt[ixyz].keys():
                dictt[ixyz][v] = [p_i]
            else:
                dictt[ixyz][v].append(p_i)
    vp = []
    vpp = []
    for ixyz in range(3):
        vals = set()
        for key, val in dictt[ixyz].items():
            if len(val) > 2:
                v = vel[dictt[ixyz][key][0], ixyz]
                assert np.all(np.array(vel[dictt[ixyz][key]][:, ixyz]) == v), "Wrong v's."
                p = [int(pp) for pp in pos[dictt[ixyz][key]][:,ixyz]]
                r = [p[i]-p[(i+1)%len(p)] for i in range(len(p))]
                co = other_lcm(r)
                s = [ri % co for ri in r]
                if np.all(np.array(s) == 0):
                    t = [ri // co for ri in r]
                    vv = [ri // ti + v for ri, ti in zip(r, t)]
                    if np.all(np.array(vv) == vv[0]):
                        vp.append(vv[0])
                        if ixyz == 2:
                            a = []
                            for jxyz in range(2):
                                vj = vel[dictt[ixyz][key]][:, jxyz]
                                pj = [int(pp) for pp in pos[dictt[ixyz][key]][:, jxyz]]
                                rj = [pj[i] - pj[(i + 1) % len(pj)] for i in range(len(pj))]
                                vvjj = [vj[i] - vj[(i + 1) % len(pj)] for i in range(len(pj))]
                                tj = [-(rjj+(vjj-vp[jxyz])*tjj) // (vvjjj) for rjj, tjj, vjj, vvjjj in zip(rj, t, vj, vvjj)]
                                sj = [-(rjj+(vjj-vp[jxyz])*tjj) % (vvjjj) for rjj, tjj, vjj, vvjjj in zip(rj, t, vj, vvjj)]
                                assert np.all(np.array(sj) == 0), "Not zero"
                                a.append(tj)
                            assert np.all(np.array(a[0]) == np.array(a[1]))
                            for jxyz in range(3):
                                vj = vel[dictt[ixyz][key]][:, jxyz]
                                pj = [int(pp) for pp in pos[dictt[ixyz][key]][:, jxyz]]
                                ppp = [pjj+(int(vjj)-int(vp[jxyz]))*int(tjj) for pjj, tjj, vjj in zip(pj[1:], tj, vj[1:])]
                                assert np.all(np.array(ppp) == ppp[0])
                                vpp.append(ppp[0])

                        # p = r1 + v1 * t1 = r + v * t1
                        # y1-y2 + v1*(t1-t2+t2)-v2*t2 = v * (t1-t2)
                        # t2 = -(y1-y2 - v*(t1-t2)) / (v1-v2)
                        break
    print(vp, vpp)
    return vpp[0] + vpp[1] + vpp[2]

if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 24")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt', (7, 27)), 2
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 18651
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    #result, result_expected = solution2('test.txt'), 47
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 658018404718110
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache


def solution(filename: str = "data.txt", short=True) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    sy, sx = len(datatable), len(datatable[0].strip())
    at = np.zeros((sy, sx), dtype=int)
    translate_dict = dict(zip("#.><v^", [1, 2, 3, 4, 5, 6]))
    for dli, dline in enumerate(datatable):
        for di, dl in enumerate(dline.strip()):
            at[dli, di] = translate_dict[dl]
    start_pos, end_pos = (0, 1), (sy - 1, sx - 2)
    cd = {start_pos: [], end_pos: []}

    # find crossing
    for iy in range(1, sy-1):
        for ix in range(1, sx-1):
            if at[iy, ix] > 1:
                if np.sum([at[iy+yy, ix+xx] > 1 for yy, xx in ((-1, 0), (1, 0), (0, -1), (0, 1))]) > 2:
                    cd[(iy, ix)] = []

    choose_dict = dict(zip([2,3,4,5,6],(
        {(-1,0): True, (1, 0): True, (0,-1): True, (0,1): True},
        {(0,1): True, (0,-1): False},
        {(0,1): False, (0,-1): True},
        {(1,0): True, (-1,0): False},
        {(1,0): False, (-1,0): True}
    ))) if short else dict(zip([2,3,4,5,6],(
        {(-1,0): True, (1, 0): True, (0,-1): True, (0,1): True},
        {(0,1): True, (0,-1): True},
        {(0,1): True, (0,-1): True},
        {(1,0): True, (-1,0): True},
        {(1,0): True, (-1,0): True}
    )))

    def follow_path(first_pos, start_dir):
        # find lengths in network
        counts = 1
        current_pos, current_dir = first_pos, start_dir
        while counts < 1000:
            counts += 1
            for sdi in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if sdi[0] == -current_dir[0] and sdi[1] == -current_dir[1]:
                    continue
                cpos = current_pos[0] + sdi[0], current_pos[1] + sdi[1]
                cat = at[cpos]
                if cpos in cd.keys():
                    return cpos, counts
                if cat == 1:
                    continue
                if choose_dict[cat][sdi]:
                    current_pos, current_dir = cpos, sdi
                    break
                else:
                    return None
        return -1
    for path_i in cd.keys():
        if path_i == start_pos or path_i == end_pos:
            sd = (1, 0) if path_i == start_pos else (-1, 0)
            sp = start_pos if path_i == start_pos else end_pos
            fp = follow_path((sp[0]+sd[0], sp[1]+sd[1]), sd)
            if fp is not None:
                cd[path_i].append(fp)
            continue

        iy, ix = path_i
        for sd in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if at[iy+sd[0], ix+sd[1]] > 1:  # path is passable
                fp = follow_path((iy+sd[0], ix+sd[1]), sd)
                if fp is not None:
                    cd[path_i].append(fp)

    out_list = []
    def follow_network(start_point, passed_points, counts=0):
        options = cd[start_point]
        if len(options) == 0:
            return False
        else:
            for option, cts in options:
                if option not in passed_points:
                    if option == end_pos:
                        out_list.append(counts + cts)
                    pp_local = passed_points.copy()
                    pp_local.add(option)
                    follow_network(option, pp_local, counts+cts)

    follow_network(start_pos, {start_pos})
    return np.max(out_list)

if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 23")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 94
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 2106
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    result, result_expected = solution('test.txt', False), 154
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution(short=False), 6350
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

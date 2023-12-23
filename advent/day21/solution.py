import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache


def solution(filename: str = "data.txt", smudge=64) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()

    garden = np.zeros((len(datatable), len(datatable[0])), dtype=bool)
    allowed_keys = ".#S"
    start_point = np.array([-1, -1])
    for dli, dataline in enumerate(datatable):
        for gpi, garden_part in enumerate(dataline.strip()):
            assert garden_part in allowed_keys, f"The patch {garden_part} is unexpected."
            point = np.array([dli, gpi])
            if garden_part == "S":
                assert np.all(start_point == np.array([-1, -1])), f"There are multple starting points, {start_point} and {point}."
                start_point = point
            if garden_part != "#":
                garden[point[0], point[1]] = True
    previous_points = set()
    previous_points.add(tuple(start_point.tolist()))
    sy, sx = garden.shape
    from copy import deepcopy
    for istep in range(smudge):
        points_reached = set()
        for p_point in previous_points:
            for dy, dx in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                i_point = (p_point[0] + dy, p_point[1] + dx)
                if 0 <= i_point[0] < sy and 0 <= i_point[1] < sx:
                    if garden[i_point[0], i_point[1]]:
                        points_reached.add(i_point)
        previous_points = deepcopy(points_reached)
    return len(previous_points)


def solution2(filename: str = "data.txt", smudge=26501365) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()

    garden = np.zeros((len(datatable), len(datatable[0].strip())), dtype=bool)
    allowed_keys = ".#S"
    start_point = np.array([-1, -1])
    for dli, dataline in enumerate(datatable):
        for gpi, garden_part in enumerate(dataline.strip()):
            assert garden_part in allowed_keys, f"The patch {garden_part} is unexpected."
            point = np.array([dli, gpi])
            if garden_part == "S":
                assert np.all(start_point == np.array([-1, -1])), f"Multiple start points, {start_point} and {point}."
                start_point = point
            if garden_part != "#":
                garden[point[0], point[1]] = True
    previous_points = set()
    previous_points.add(tuple(start_point.tolist()))
    sy, sx = garden.shape
    if False:
        already_sites = set()
        find_points = [(0, 0), (sy, 0), (0, sx), (sy, sx)]
        istep = 0
        keep_running = True
        fp_res = {}
        fb_res = {}
        while keep_running:
            istep += 1
            points_reached = set()
            for p_point in previous_points:
                for dy, dx in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                    i_point = (p_point[0] + dy, p_point[1] + dx)
                    if garden[i_point[0] % sy, i_point[1] % sx]:
                        points_reached.add(i_point)
            for ip in points_reached:
                if ip in find_points and ip not in fp_res.keys():
                    fp_res[ip] = istep
                if ip[0] == 0 and "-y" not in fb_res.keys():
                    fb_res["-y"] = istep
                if ip[0] == sy-1 and "+y" not in fb_res.keys():
                    fb_res["+y"] = istep
                if ip[1] == 0 and "-x" not in fb_res.keys():
                    fb_res["-x"] = istep
                if ip[1] == sx-1 and "+x" not in fb_res.keys():
                    fb_res["+x"] = istep
            if len(fp_res) == 4 and len(fb_res) == 4:
                keep_running = False
            previous_points = points_reached

        previous_points = set()
        previous_points.add((0, 0))
        fd_res = {}
        find_points = [(sy, 0), (0, sx), (sy, sx)]
        keep_running = True
        istep = 0
        while keep_running:
            istep += 1
            points_reached = set()
            for p_point in previous_points:
                for dy, dx in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                    i_point = (p_point[0] + dy, p_point[1] + dx)
                    if garden[i_point[0] % sy, i_point[1] % sx]:
                        points_reached.add(i_point)
            for ip in points_reached:
                if ip in find_points and ip not in fd_res.keys():
                    fd_res[ip] = istep
            if len(fd_res) == 3:
                keep_running = False
            previous_points = points_reached

        previous_points = set()
        previous_points.add((sy-1, sx-1))
        find_points = [(-1, -1), (-1, sx-1), (sy-1, -1)]
        keep_running = True
        istep = 0
        while keep_running:
            istep += 1
            points_reached = set()
            for p_point in previous_points:
                for dy, dx in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                    i_point = (p_point[0] + dy, p_point[1] + dx)
                    if garden[i_point[0] % sy, i_point[1] % sx]:
                        points_reached.add(i_point)
            for ip in points_reached:
                if ip in find_points and ip not in fd_res.keys():
                    fd_res[ip] = istep
            if len(fd_res) == 6:
                keep_running = False
            previous_points = points_reached
        print(fb_res)
        print(fp_res)
        print(fd_res)

    previous_points = set()
    previous_points.add(tuple(start_point.tolist()))
    prev_count, pv, pvv, pvv_2 = 0, 0, 0, 0
    prev_sets = []
    assert sx == sy, f"This method only works for square gardens, {sx} != {sy}."

    remainder_s = smudge % sx
    loopbool = True
    istep = 0
    while loopbool:
        istep += 1
        points_reached = set()
        for p_point in previous_points:
            for dy, dx in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                i_point = (p_point[0] + dy, p_point[1] + dx)
                if garden[i_point[0] % sy, i_point[1] % sx]:
                    points_reached.add(i_point)
        if (istep - remainder_s) % sx == 0:
            now_count = len(points_reached)
            pv_now = now_count - prev_count
            pvv_now = pv_now - pv
            if pvv_now == pvv:  # and pvv == pvv_2:
                loopbool = False
            #print(istep, now_count, pv_now, pvv_now)
            prev_count = now_count
            pv = pv_now
            pvv_2 = pvv
            pvv = pvv_now
        previous_points = points_reached

    return now_count + np.sum([pv + pvv * (i+1) for i in range((smudge - istep) // sx)])


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 21")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt', 6), 16
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 3724
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2a")
    #result, result_expected = solution2('test.txt', 6), 16
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2b")
    #result, result_expected = solution2('test.txt', 10), 50
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2c")
    #result, result_expected = solution2('test.txt', 50), 1594
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2d")
    result, result_expected = solution2('test.txt', 100), 6536
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2e")
    result, result_expected = solution2('test.txt', 500), 167004
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2f")
    result, result_expected = solution2('test.txt', 1000), 668697
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2g")
    result, result_expected = solution2('test.txt', 5000), 16733044
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 620348631910321
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

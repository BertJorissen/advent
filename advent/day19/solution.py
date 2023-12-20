import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache

def solution(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    rules = {}
    assignments = []

    import_rules = True

    for line in datatable:
        l = line.strip()
        if import_rules:
            if l == "":
                import_rules = False
            else:
                k_name, k_content = l.split("{")
                k_content = k_content.split("}")[0].split(",")
                buffer = []
                for k_r_i, k_rule in enumerate(k_content):
                    if "<" in k_rule:
                        k_r, k_m = k_rule.split(":")
                        key_i, int_i = k_r.split("<")
                        buffer.append((key_i, k_m, -int(int_i)))
                    elif ">" in k_rule:
                        k_r, k_m = k_rule.split(":")
                        key_i, int_i = k_r.split(">")
                        buffer.append((key_i, k_m, int(int_i)))
                    else:
                        assert k_r_i == len(k_content) - 1, f"The line {k_rule} at {k_r_i}/{len(k_content-1)} is abnormal."
                        buffer.append(("", k_rule, 0))
                rules[k_name] = buffer
        else:
            l = l[1:-1]
            ld = {}
            for ll in l.split(","):
                lll = ll.split("=")
                ld[lll[0]] = int(lll[1])
            assignments.append(ld)

    def process_line(am, ky):
        if ky == "A":
            return True
        elif ky == "R":
            return False
        rule = rules[ky]
        for ri, rul in enumerate(rule):
            if rul[2] == 0:
                assert ri == len(rule) - 1, f"The rule {rule} with {ky} at {ri}-{rul} seem to be weird."
                return process_line(am, rul[1])
            elif rul[2] > 0:
                if am[rul[0]] > rul[2]:
                    return process_line(am, rul[1])
            elif rul[2] < 0:
                if am[rul[0]] < -rul[2]:
                    return process_line(am, rul[1])
            else:
                assert False, f"This line with {am} and {ky} seems to be wrong."
        assert False, f"This line with {am} and {ky} seems to be wrong."

    count = 0
    for amt in assignments:
        if process_line(amt, "in"):
            count += np.sum(list(amt.values()))
    return count


def solution2(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()
    rules = {}
    assignments = []

    import_rules = True
    d_min, d_max = 1, 4000
    for line in datatable:
        l = line.strip()
        if import_rules:
            if l == "":
                import_rules = False
            else:
                k_name, k_content = l.split("{")
                k_content = k_content.split("}")[0].split(",")
                buffer = []
                for k_r_i, k_rule in enumerate(k_content):
                    if "<" in k_rule:
                        k_r, k_m = k_rule.split(":")
                        key_i, int_i = k_r.split("<")
                        int_i = int(int_i)
                        assert d_min <= int_i <= d_max, f"The integer {int_i} is not between {d_min} and {d_max}."
                        buffer.append((key_i, k_m, -int_i))
                    elif ">" in k_rule:
                        k_r, k_m = k_rule.split(":")
                        key_i, int_i = k_r.split(">")
                        int_i = int(int_i)
                        assert d_min <= int_i <= d_max, f"The integer {int_i} is not between {d_min} and {d_max}."
                        buffer.append((key_i, k_m, int_i))
                    else:
                        assert k_r_i == len(k_content) - 1, f"The line {k_rule} at {k_r_i}/{len(k_content-1)} is abnormal."
                        buffer.append(("", k_rule, 0))
                rules[k_name] = buffer
        else:
            l = l[1:-1]
            ld = {}
            for ll in l.split(","):
                lll = ll.split("=")
                ld[lll[0]] = int(lll[1])
            assignments.append(ld)

    def process_line(am, ky):
        #print(am, ky)
        if ky == "A":
            #print(am)
            #print([krr[1]-krr[0]+1 for krr in list(am.values())])
            return np.prod([krr[1]-krr[0]+1 for krr in list(am.values())], dtype=np.int64)
        elif ky == "R":
            return 0
        rule = rules[ky]
        counts = np.array(0, dtype=np.int64)
        for ri, rul in enumerate(rule):
            if rul[2] == 0:
                assert ri == len(rule) - 1, f"The rule {rule} with {ky} at {ri}-{rul} seem to be weird."
                counts += process_line(am, rul[1])
            elif rul[2] > 0:
                if am[rul[0]][0] > rul[2]:
                    return process_line(am, rul[1])
                elif am[rul[0]][1] > rul[2]:
                    ml = am.copy()
                    ml[rul[0]] = [rul[2]+1, am[rul[0]][1]]
                    counts += process_line(ml, rul[1])
                    am = am.copy()
                    am[rul[0]] = [am[rul[0]][0], rul[2]]
            elif rul[2] < 0:
                if am[rul[0]][1] < -rul[2]:
                    return process_line(am, rul[1])
                elif am[rul[0]][0] < -rul[2]:
                    ml = am.copy()
                    ml[rul[0]] = [am[rul[0]][0], -rul[2]-1]
                    counts += process_line(ml, rul[1])
                    am = am.copy()
                    am[rul[0]] = [-rul[2], am[rul[0]][1]]
            else:
                assert False, f"This line with {am} and {ky} seems to be wrong."
        #print(counts)
        return counts
    amt = {"x": [d_min, d_max], "m": [d_min, d_max], "a": [d_min, d_max], "s": [d_min, d_max]}
    return process_line(amt, "in")


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 19")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 19114
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 476889
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    result, result_expected = solution2('test.txt'), 167409079868000
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 132380153677887
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

import re
import numpy as np
from typing import List, Tuple, Optional
from functools import cache


def solution(filename: str = "data.txt", smudge=False) -> int:
    with open(filename, "r") as data:
        datatable = data.readlines()

    n_connections = {}
    n_states = {}
    for dataline in datatable:
        m_in, m_out = dataline.strip().split(" -> ")
        m_out = m_out.split(", ")
        if m_in == "broadcaster":
            m_type, m_name = 0, m_in
        else:
            m_type, m_name = m_in[0], m_in[1:]
            if m_type == "%":
                m_type = 1
            elif m_type == "&":
                m_type = 2
            else:
                assert False, f"The key {m_type} seems to be unexpected"
        n_connections[m_name] = m_out
        n_states[m_name] = (m_type, m_out, {}, False)

    for nname, nval in n_connections.items():
        for m_oi in nval:
            if m_oi in n_states.keys():
                n_states[m_oi][2][nname] = False
            else:
                n_states[m_oi] = (3, [], {}, False)
    assert n_states["broadcaster"][2] == {}, f"The broadcaster shoedn't get inputs, {n_states['breadcaster'][2]}."

    print(n_states)
    print(n_connections)


    def call_node(nodename, fromstate, powerstate):
        m_type = n_states[nodename][0]
        counter = 0
        if m_type == 0:  # broadcaster
            for m_i in m_out:
                counter += 1
                counter += call_node(m_i, nodename, powerstate)
            return counter
        elif m_type == 1:  # flip-flop
            for m_i in m_out:
                if powerstate:
                    counter += 1
                    counter += call_node(m_i, nodename, powerstate)
                else:
                    counter += 1
                    counter += call_node(m_i, nodename, not n_states[nodename])
                    n_states[nodename] = not n_states[nodename]
            return counter
        elif m_type == 2:  # conjunction
            ee
        elif m_type == 3:  # endpoint
            return 0
        else:
            assert False, f"The combination {m_type} is unknown."
        n_connections[nodename]


if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 20")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test.txt'), 32000000
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    result, result_expected = solution('test2.txt'), 11687500
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    #result, result_expected = solution(), 476889
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    #result, result_expected = solution2('test.txt'), 167409079868000
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    #result, result_expected = solution2(), 132380153677887
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

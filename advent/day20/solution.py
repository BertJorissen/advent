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
        n_states[m_name] = [m_type, m_out, {}, False]

    for nname, nval in n_connections.items():
        for m_oi in nval:
            if m_oi in n_states.keys():
                n_states[m_oi][2][nname] = False
            else:
                n_states[m_oi] = [3, [], {}, False]
    assert n_states["broadcaster"][2] == {}, f"The broadcaster shoedn't get inputs, {n_states['breadcaster'][2]}."

    #print(n_states)
    #print(n_connections)

    slow, shigh = np.array([1,0]), np.array([0,1])
    counter = np.array([0,0])
    v = False
    for i in range(1000):
        if v:
            print("_----------_", i)
        call_list = [("button", "", False)]
        while len(call_list) > 0:
            tmp = []
            for nodename, fromstate, powerstate in call_list:
            #def call_node(nodename="button", fromstate="", powerstate=False):
                m_type = 0 if nodename == "button" else n_states[nodename][0]
                #counter = np.array([0,0])
                if nodename == "button":
                    counter += slow
                    if v:
                        print("broadcaster", nodename, powerstate)
                    #counter += call_node("broadcaster", nodename, powerstate)
                    tmp.append(("broadcaster", nodename, powerstate))
                    #return counter
                elif m_type == 0:  # broadcaster
                    for m_i in n_connections[nodename]:
                        counter += shigh if powerstate else slow
                        if v:
                            print(m_type, nodename, m_i, powerstate)
                        #counter += call_node(m_i, nodename, powerstate)
                        tmp.append((m_i, nodename, powerstate))
                    #return counter
                elif m_type == 1:  # flip-flop
                    if powerstate:
                        #for m_i in n_connections[nodename]:
                        #    counter += shigh
                        #    if v:
                        #        print(m_type, 'h', nodename, m_i, powerstate)
                        #    #counter += call_node(m_i, nodename, True)
                        #    tmp.append((m_i, nodename, True))
                        ppppp = 1
                    else:
                        out_state = not n_states[nodename][3]
                        n_states[nodename][3] = out_state
                        for m_i in n_connections[nodename]:
                            if v:
                                print(m_type, nodename, m_i, out_state)
                            counter += shigh if out_state else slow
                            #counter += call_node(m_i, nodename, out_state)
                            tmp.append((m_i, nodename, out_state))
                    #return counter
                elif m_type == 2:  # conjunction
                    n_states[nodename][2][fromstate] = powerstate
                    out_state = not np.sum(list(n_states[nodename][2].values())) == len(n_states[nodename][2])
                    for m_i in n_connections[nodename]:
                        counter += shigh if out_state else slow
                        if v:
                            print(m_type, nodename, m_i, out_state)
                        #counter += call_node(m_i, nodename, out_state)
                        tmp.append((m_i, nodename, out_state))
                    #return counter
                elif m_type == 3:  # endpoint
                    #return counter
                    pppppp =1
                else:
                    assert False, f"The combination {m_type} is unknown."
            call_list = tmp.copy()
    return np.prod(counter)


def solution2(filename: str = "data.txt", fn="rx") -> int:
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
        n_states[m_name] = [m_type, m_out, {}, False]

    for nname, nval in n_connections.items():
        for m_oi in nval:
            if m_oi in n_states.keys():
                n_states[m_oi][2][nname] = False
            else:
                n_states[m_oi] = [3, [], {nname: False}, False]
    assert n_states["broadcaster"][2] == {}, f"The broadcaster shoedn't get inputs, {n_states['breadcaster'][2]}."

    v = False

    from copy import deepcopy
    def find_iters(node_name: str, ooo: bool = True) -> int:
        n_s = deepcopy(n_states)
        for i in range(100000):
            if (i+1) % 10000 == 0:
                print(i)
            if v:
                print("_----------_", i)
            call_list = [("button", "", False)]
            while len(call_list) > 0:
                tmp = []
                for nodename, fromstate, powerstate in call_list:
                    if fromstate == node_name and powerstate == ooo:
                        return i + 1
                    m_type = 0 if nodename == "button" else n_s[nodename][0]
                    if nodename == "button":
                        if v:
                            print("broadcaster", nodename, powerstate)
                        tmp.append(("broadcaster", nodename, powerstate))
                    elif m_type == 0:  # broadcaster
                        for m_i in n_connections[nodename]:
                            if v:
                                print(m_type, nodename, m_i, powerstate)
                            tmp.append((m_i, nodename, powerstate))
                    elif m_type == 1:  # flip-flop
                        if not powerstate:
                            out_state = not n_s[nodename][3]
                            n_s[nodename][3] = out_state
                            for m_i in n_connections[nodename]:
                                if v:
                                    print(m_type, nodename, m_i, out_state)
                                tmp.append((m_i, nodename, out_state))
                    elif m_type == 2:  # conjunction
                        n_s[nodename][2][fromstate] = powerstate
                        out_state = not np.sum(list(n_s[nodename][2].values())) == len(n_s[nodename][2])
                        for m_i in n_connections[nodename]:
                            if v:
                                print(m_type, nodename, m_i, out_state)
                            tmp.append((m_i, nodename, out_state))
                    elif m_type != 3:  # not an endpoint
                        assert False, f"The combination {m_type} is unknown."
                call_list = tmp.copy()

    def find_sources(find_name: str) -> List[str]:
        sources = list(n_states[find_name][2].keys())
        if len(sources) == 1:
            return find_sources(sources[0])
        elif len(sources) > 1:
            for source in sources:
                assert n_states[source][0] == 2, f"This is an unexpected type: {source} - {n_states[source][0]}."
            return sources
        else:
            assert False, f"The sources of {find_name} are unexpected."
    periods = [find_iters(source, True) for source in find_sources(fn)]
    return np.lcm.reduce(periods, dtype=np.int64)




if __name__ == "__main__":
    print("================")
    print(" ADVENT - DAY 20")
    print("================")
    print("")
    print(" - testcase")
    result, result_expected = solution('test2.txt'), 32000000
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - testcase 2")
    result, result_expected = solution('test.txt'), 11687500
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment")
    result, result_expected = solution(), 861743850
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")
    print("")
    print(" - assignment 2")
    result, result_expected = solution2(), 247023644760071
    print(f"  + result: {result}")
    if result != result_expected:
        print(f" ERROR: this should be {result_expected}")

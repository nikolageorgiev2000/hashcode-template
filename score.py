from dataparser import *
from collections import *

# inp: the input file as a single string
# out: the answer file produced by your solver, as a single string
# return the score of the output as an integer


def score(inp, out):
    ns = parse(inp)
    itr = (line for line in out.split('\n'))
    # TODO: implement
    sout = argparse.Namespace()
    sout.A = nl(itr)[0] # number of intersections
    sout.schedules = {} # dict of schedules per intersection
    for _ in range(sout.A):
        id = nl(itr)[0]
        sout.schedules[id] = argparse.Namespace()
        sout.schedules[id].I = id  # intersection id
        sout.schedules[id].E = nl(itr)[0]  # num of incoming streets
        sout.schedules[id].intimes = []  # list (street_name, green_duration)
        for _ in range(sout.schedules[id].E):
            street_info = next(itr).split()
            sout.schedules[id].intimes.append((street_info[0], int(street_info[1])))
    print(sout.schedules)

    # total = 0
    # cpos = {}
    # for c in ns.cars:
    #     cpos[c[0]] = 0
    #     while 
    # for T in range(ns.D+1):



    return 0

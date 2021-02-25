import argparse
import random
import sys
import math
sys.path.extend(['..', '.'])
from collections import *
from dataparser import parse
from util import get_in_file_content

# inp is an input file as a single string
# return your output as a string
def solve(inp, args):
    # TODO: Solve the problem
    random.seed(args['seed'])
    ns = parse(inp)

    schedule = []

    ############## Calculates street usage
    ############## For future use
    streetUsage = {}
    carsAtStart = {}
    for street in ns.streets:
        streetUsage[street] = 0
        carsAtStart[street] = 0

    for path in ns.cars:
        carsAtStart[path[0]]+=1
        for street in path:
            streetUsage[street]+=1

    streetThroughput = {}
    for name in ns.streets:
        streetThroughput[name] = streetUsage[name]/ns.streets[name].l
    ###############
    ###############

    # Creates round robin scheduling
    for intersection in range(0,ns.I):
        node = ns.nodes[intersection]
        streetTimings = []
        tTotal = 0
        for street in sorted(node.i, key=lambda k: ns.streets[k].l):
            if carsAtStart[street]>0:
                t = max(ns.streets[street].l-tTotal,0)+carsAtStart[street]
                tTotal += t

                if tTotal<ns.D:
                    streetTimings.append({"name": street, "time": t, "length": ns.streets[street].l})
                else:
                    if t-(tTotal-ns.D)>0:
                        streetTimings.append({"name": street, "time": t-(tTotal-ns.D), "length": ns.streets[k].l})


        schedule.append({"id": intersection, "streets": streetTimings})

    # Creates output string
    output = str(len(schedule)) + "\n"
    for intersection in schedule:
        if len(intersection["streets"])>0:
            output += str(intersection["id"]) + "\n"
            output += str(len(intersection["streets"])) + "\n"
            for street in sorted(intersection["streets"], key=lambda k: k['length']):
                output += street["name"] + " " + str(street["time"]) + "\n"

    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    args = parser.parse_args()
    inp = get_in_file_content(args.in_file)
    out = solve(inp, {'seed': 0})
    print('\n'.join(['OUT:', '=========', out]))

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
    for street in ns.streets:
        streetUsage[street] = 0

    for path in ns.cars:
        for street in path:
            streetUsage[street]+=1

    streetThroughput = {}
    for name in ns.streets:
        streetThroughput[name] = streetUsage[name]/ns.streets[name].l
    ###############
    ###############

    # Creates round robin scheduling
    n = max(math.floor(ns.D / 150),2)

    for intersection in range(0,ns.I):
        node = ns.nodes[intersection]
        streetTimings = []
        streetDist = 0
        for street in node.i:
            streetDist += streetThroughput[street]

        for street in node.i:
            usage = streetThroughput[street]

            if streetDist == 0:
                t = 1
            else:
                t = math.ceil(usage*1.0/streetDist * min(n, ns.D))
            t = max(t, 1)
            streetTimings.append({"name": street, "time": t, "length": ns.streets[street].l})

        schedule.append({"id": intersection, "streets": streetTimings})

    # Creates output string
    output = str(len(schedule)) + "\n"
    for intersection in schedule:
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

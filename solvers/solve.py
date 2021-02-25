import argparse
import random
import sys
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
    street_usage = {}
    for street in ns.streets:
        street_usage[street] = 0

    for path in ns.cars:
        for street in path:
            street_usage[street]+=1
    ###############
    ###############

    # Creates round robin scheduling
    for intersection in range(0,ns.I):
        node = ns.nodes[intersection]
        streetTimings = []
        for street in node.i:
            streetTimings.append({"name": street, "time": 1})

        schedule.append({"id": intersection, "streets": streetTimings})

    # Creates output string
    output = str(len(schedule)) + "\n"
    for intersection in schedule:
        output += str(intersection["id"]) + "\n"
        output += str(len(intersection["streets"])) + "\n"
        for street in intersection["streets"]:
            output += street["name"] + " " + str(street["time"]) + "\n"

    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    args = parser.parse_args()
    inp = get_in_file_content(args.in_file)
    out = solve(inp, {'seed': 0})
    print('\n'.join(['OUT:', '=========', out]))

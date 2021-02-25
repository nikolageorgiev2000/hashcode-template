import argparse
import numpy as np
import random
import sys
import math
sys.path.extend(['..', '.'])
from collections import *
from dataparser import parse
from util import get_in_file_content

# Python implementation of Binary Indexed Tree 

def getrangesum(BITTree,i,j):
    if i > 1:
        return getsum(BITTree,j) - getsum(BITTree,i - 1)
    else:
        return getsum(BITTree,j)

# Returns sum of arr[0..index]. This function assumes 
# that the array is preprocessed and partial sums of 
# array elements are stored in BITree[]. 
def getsum(BITTree,i): 
    s = 0 #initialize result 

    # index in BITree[] is 1 more than the index in arr[] 
    i = i+1

    # Traverse ancestors of BITree[index] 
    while i > 0: 

        # Add current element of BITree to sum 
        s += BITTree[i] 

        # Move index to parent node in getSum View 
        i -= i & (-i) 
    return s 

# Updates a node in Binary Index Tree (BITree) at given index 
# in BITree. The given value 'val' is added to BITree[i] and 
# all of its ancestors in tree. 
def updatebit(BITTree , n , i ,v): 

    # index in BITree[] is 1 more than the index in arr[] 
    i += 1

    # Traverse all ancestors and add 'val' 
    while i <= n: 

        # Add 'val' to current node of BI Tree 
        BITTree[i] += v 

        # Update index to that of parent in update View 
        i += i & (-i) 


# Constructs and returns a Binary Indexed Tree for given 
# array of size n. 
def construct(arr, n): 

    # Create and initialize BITree[] as 0 
    BITTree = [0]*(n+1) 

    # Store the actual values in BITree[] using update() 
    for i in range(n): 
        updatebit(BITTree, n, i, arr[i]) 

    # Uncomment below lines to see contents of BITree[] 
    #for i in range(1,n+1): 
    #     print BITTree[i], 
    return BITTree 

# inp is an input file as a single string
# return your output as a string
def solve(inp, args):
    # TODO: Solve the problem
    random.seed(args['seed'])
    ns = parse(inp)

    schedule = []

    ############## Calculates street usage
    ############## For future use
    busy = {}
    for path in ns.cars:
        t = 0
        for street in path:
            # add to heightmap
            for i in range(t, t + ns.streets[street].l):
                if street not in busy:
                    busy[street] = [0] * ns.D
                if i < ns.D:
                    busy[street][i] += 1
            t += ns.streets[street].l

    avgs = {}
    for s in ns.streets:
        if s in busy:
            avgs[s] = np.mean(busy[s])
        else:
            avgs[s] = 0

    # make fenwick tree
    # timestepsFT = construct(timeSteps, len(timeSteps))
                
    ###############
    ###############

    # Creates round robin scheduling
    t=min(20, ns.D)

    for intersection in range(0,ns.I):
        node = ns.nodes[intersection]
        streetTimings = []
        streetDist = 1
        for street in node.i:
            streetDist += avgs[street]

        for street in node.i:
            usage = avgs[street]

            if streetDist > 0 and usage > 0:
                t2 = math.ceil(usage*1.0/streetDist * 8.0)
                streetTimings.append({"name": street, "time": t2})

        if len(streetTimings) > 0:
            schedule.append({"id": intersection, "streets": streetTimings})

    # #Creates round robin scheduling
    # for intersection in range(0,ns.I):
    #     node = ns.nodes[intersection]
    #     streetTimings = []
    #     maxStreet = ""
    #     maxStreetUsage = -1
    #     for street in node.i:
    #         if streetUsage[street] > maxStreetUsage:
    #             maxStreetUsage = streetUsage[street]
    #             maxStreet = street
    #
    #     # for street in node.i:
    #     #     if street != maxStreet:
    #     #         streetTimings.append({"name": street, "time": 1})
    #
    #     streetTimings.append({"name": maxStreet, "time": 1})
    #
    #     schedule.append({"id": intersection, "streets": streetTimings})

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

from dataparser import *
from collections import *
import queue

# inp: the input file as a single string
# out: the answer file produced by your solver, as a single string
# return the score of the output as an integer


def score(inp, out):
    ns = parse(inp)
    itr = (line for line in out.split('\n'))
    # TODO: implement
    sout = argparse.Namespace()
    sout.A = nl(itr)[0]  # number of intersections
    sout.schd = {}  # dict of schedules per intersection
    for _ in range(sout.A):
        id = nl(itr)[0]
        sout.schd[id] = argparse.Namespace()
        sout.schd[id].I = id  # intersection id
        sout.schd[id].E = nl(itr)[0]  # num of incoming streets
        # list [street_name, green_duration, end_time]
        sout.schd[id].intimes = []
        total = 0
        for _ in range(sout.schd[id].E):
            street_info = next(itr).split()
            total += int(street_info[1])
            sout.schd[id].intimes.append(
                [street_info[0], int(street_info[1]), total])
        sout.schd[id].totlen = total

    print("PARSING")

    # track current max position in queue on street
    qmax = {sname: 0 for sname in ns.streets.keys()}

    # track car [street_index, queue_index, dist left on street]
    cpos = []
    for i in range(len(ns.cars)):
        street = ns.cars[i][0]
        cpos.append([0, qmax[street]+1, 0])
        qmax[street] = qmax[street]+1

    # keep track of green light at intersection [street_ind, time]
    for id in sout.schd.keys():
        sout.schd[id].lights = [0, 0]

    score = 0

    for T in range(1, ns.D+1):
        if(T % 10000 == 0):
            print(score)
        # update green light for each intersection
        for id in sout.schd.keys():
            node = sout.schd[id]
            street_ind = node.lights[0]
            node.lights[1] += 1  # update time
            if(node.lights[1] > node.intimes[street_ind][2]):  # if over street end time
                node.lights[0] += 1  # update street
                node.lights[0] = node.lights[0] % node.E  # fix overflow
            node.lights[1] = node.lights[1] % node.totlen  # fix overflow


        for c, pos in enumerate(cpos):
            curr_street = ns.cars[c][pos[0]]
            if(pos[1] != -1):  # if in queue
                node = ns.streets[curr_street].e
                if(sout.schd[node].lights[0] == pos[0]):  # if street light green
                    if(pos[1] == 1):  # if in position 1, move to next street
                        pos[0] += 1
                        pos[1] = -1
                        new_street = ns.cars[c][pos[0]]
                        pos[2] = ns.streets[new_street].l
                    else:  # update queue pos
                        pos[1] -= 1
            else:  # else update distance on street, if dist becomes 0 add to queue
                pos[2] -= 1
                if(pos[2] == 0):
                    if(pos[0] != len(ns.cars[c])-1):
                        score += 1000 + ns.D-T
                        pos[1] = -1
                    else:
                        pos[1] = qmax[curr_street] + 1
                        qmax[curr_street] = qmax[curr_street] + 1

    return score

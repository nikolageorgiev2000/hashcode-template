import argparse
import json
from collections import *
from pathlib import Path

def ni(itr):
    return int(next(itr))

# parses the next string of itr as a list of integers
def nl(itr):
    return [int(v) for v in next(itr).split()]


def parse(inp):
    itr = (line for line in inp.split('\n'))
    ns = argparse.Namespace()

    first_line = nl(itr)
    # Simduration
    ns.D  = first_line[0]
    # num. intersections
    ns.I  = first_line[1]
    # num. streets
    ns.S = first_line[2]
    # num. cars
    ns.V = first_line[3]
    # bonus points
    ns.F = first_line[4]

    # Access with:
    #   ns.sreets[<street-name>].property
    ns.streets = {}

    for _ in range(ns.S):
        line = next(itr).split(' ')
        b, e = int(line[0]), int(line[1])
        sname = line[2]
        l = int(line[3])

        # add it to dic
        ns.streets[sname] = argparse.Namespace()
        ns.streets[sname].name = sname  # street name
        ns.streets[sname].b = b         # start intersec ID
        ns.streets[sname].e = e         # end   intersec ID
        ns.streets[sname].l = l         # time to cross

    # Access with:
    #   ns.cars[<car ID>][i] -> name of ith street car <card ID. passes through
    ns.cars = []
    for _ in range(ns.V):
        car_path = []

        line = next(itr).split(' ')
        p = int(line[0])
        # add all street names to a list
        for i in range(p):
            car_path.append(line[1 + i])

        # add the path to the cars list
        ns.cars.append(car_path)

    # Access with:
    #   ns.nodes[<node-ID>].i -> array of incomming street names
    #   ns.nodes[<node-ID>].o -> array of outgoing street names
    ns.nodes = []
    for _ in range(ns.I):
        ns.nodes.append(argparse.Namespace())
    # init
    for inter in ns.nodes:
        inter.i = []
        inter.o = []
    # assign
    for street in ns.streets.values():
        # start inter -> outgoing
        ns.nodes[street.b].o.append(street.name)
        # end inter -> ingoing street
        ns.nodes[street.e].i.append(street.name)

    return ns

class FlexibleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, argparse.Namespace):
            return vars(obj)
        return json.JSONEncoder.default(self, obj)

def parse2json(inp):
    ns = parse(inp)
    return json.dumps(ns, cls=FlexibleEncoder)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('inp', nargs='?')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    if args.inp:
        file_list = [Path(args.inp)]
    else:
        file_list = Path('in').glob('*.in')

    for inp in file_list:
        data = parse2json(inp.read_text())
        with inp.with_suffix('.json').open('w') as f:
            f.write(data)

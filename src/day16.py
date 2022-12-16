import matplotlib.pyplot as plt
from itertools import product, permutations
import networkx as nx
from tqdm import tqdm
import re


def get_graph(filename):
    # Create networkx graph to calc shortest distances
    G = nx.Graph()
    valves = {}
    regex = r"Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)"
    with open(filename, 'r') as f:
        for line in f.readlines():
            groups = re.findall(regex, line, re.MULTILINE)
            for group in groups:
                print(group)
                valves[group[0]] = int(group[1])
                G.add_edges_from(list(product([group[0]], group[2].split(", "))))

    # nx.draw(G, with_labels=True)
    # plt.show()
    return G, valves


def calc_flow_rate(G, route, valves):
    time_left = 30
    total_flow_rate = 0
    # opened_valves = []
    # Start with the distance between AA starting point and the first valve
    time_left -= len(nx.shortest_path(G, source=route[0], target='AA')) - 1
    # For each combination of 2 valves in the route
    for valve1, valve2 in zip(route, route[1:]):
        # Subtract 1 from remaining time for opening the valve
        time_left -= 1
        # print(sum([valves[o] for o in opened_valves]))
        # opened_valves.append(valve1)
        # Add time_left * valve flow rate to total flow rate
        total_flow_rate += time_left * valves[valve1]
        # for _ in range(len(nx.shortest_path(G, source=valve1, target=valve2)) - 1):
        #     print(sum([valves[o] for o in opened_valves]))
        # Add distance between valves as time cost
        time_left -= len(nx.shortest_path(G, source=valve1, target=valve2)) - 1

        if time_left <= 0:
            return total_flow_rate
    # Open the last valve
    time_left -= 1
    total_flow_rate += time_left * valves[route[-1]]

    return total_flow_rate


def calc_possible_paths(G, useful_valves):
    good_paths = []
    for valve in useful_valves:
        for path in nx.all_simple_paths(G, source='AA', target=valve):
            if set(path).issuperset(set(useful_valves)):
                good_paths.append(path)
    return good_paths


def part1_slow(filename):
    G, valves = get_graph(filename)
    useful_valves = [k for k, v in valves.items() if v > 0]
    print(f"Useful_valves: {useful_valves}")

    # possible_paths = calc_possible_paths(G, useful_valves)

    # Permutate the list of valves that have a flow rate > 0
    max_flow_rate = 0
    for possible_combination in tqdm(permutations(useful_valves)):
        # For each permutation, calc the total flow rate until time runs out
        # test_flow_rate = calc_flow_rate(G, ('DD', 'BB', 'JJ', 'HH', 'EE', 'CC'), valves)
        # print(test_flow_rate)
        # break
        flow_rate = calc_flow_rate(G, possible_combination, valves)
        if flow_rate > max_flow_rate:
            # Keep track of max
            max_flow_rate = flow_rate
            print(possible_combination, flow_rate)

    print(f"Day 16 Part 1: {max_flow_rate}")


def part1(filename):
    G, valves = get_graph(filename)
    useful_valves = [k for k, v in valves.items() if v > 0]
    print(f"Useful_valves: {useful_valves}")

    current_valve = 'AA'
    total_score = 0
    while len(useful_valves) > 1:
        best_valve, best_score = get_valve_score(G, valves, useful_valves, current_valve)
        print(best_valve)
        useful_valves.remove(best_valve)
        current_valve = best_valve
        total_score += best_score


    print(f"Day 16 Part 1: {total_score}")

def get_valve_score(G, valves, useful_valves, current_valve):
    best_score = 0
    best_valve = 'AA'
    time_left = 30
    for valve in useful_valves:
        distance_to_current_valve = len(nx.shortest_path(G, source=current_valve, target=valve)) - 1
        # time_left - distance - time_to_open * flow rate of valve
        # This is the "score" of a valve given a starting position
        valve_score = (time_left - 2*distance_to_current_valve - 1) * valves[valve]
        if valve_score > best_score:
            best_score = valve_score
            best_valve = valve
    
    return best_valve, best_score



if __name__ == '__main__':
    part1('data/test16_1.txt')
    # part1('data/input16_1.txt')
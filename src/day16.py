import math
import matplotlib.pyplot as plt
from itertools import product, permutations
import networkx as nx
from tqdm import tqdm
import re
import random
import array
import numpy as np
import multiprocessing

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


def get_graph(filename):
    # Create networkx graph to calc shortest distances
    G = nx.Graph()
    valves = {}
    regex = r"Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)"
    with open(filename, 'r') as f:
        for line in f.readlines():
            groups = re.findall(regex, line, re.MULTILINE)
            for group in groups:
                # print(group)
                valves[group[0]] = int(group[1])
                G.add_edges_from(list(product([group[0]], group[2].split(", "))))

    # nx.draw(G, with_labels=True)
    # plt.show()
    return G, valves


def calc_shortest_paths(G, nodes):
    shortest_paths = {}
    for node1, node2 in permutations(nodes, 2):
        shortest_paths[(node1, node2)] = len(nx.shortest_path(G, source=node1, target=node2))
    return shortest_paths


# # @profile
# def calc_flow_rate(shortest_paths, route, valves, route_len):
#     time_left = 30
#     total_flow_rate = 0
#     # Start with the distance between AA starting point and the first valve
#     time_left -= shortest_paths[(route[0], 'AA')] - 1
#     # For each combination of 2 valves in the route
#     # for valve1, valve2 in zip(route, route[1:]):
#     for i in range(route_len - 1):
#         valve1 = route[i]
#         valve2 = route[i+1]
#         # Subtract 1 from remaining time for opening the valve
#         time_left -= 1
#         total_flow_rate += time_left * valves[valve1]
#         time_left -= shortest_paths[(valve1, valve2)] - 1

#         if time_left <= 0:
#             return total_flow_rate
#     # Open the last valve
#     time_left -= 1
#     total_flow_rate += time_left * valves[route[-1]]

#     return total_flow_rate


# def calc_possible_paths(G, useful_valves):
#     good_paths = []
#     for valve in useful_valves:
#         for path in nx.all_simple_paths(G, source='AA', target=valve):
#             if set(path).issuperset(set(useful_valves)):
#                 good_paths.append(path)
#     return good_paths


# # @profile
# def part1_slow(filename):
#     G, valves = get_graph(filename)
#     useful_valves = [k for k, v in valves.items() if v > 0]
#     print(f"Useful_valves: {useful_valves}")

#     route_len = len(useful_valves)

#     shortest_paths = calc_shortest_paths(G, useful_valves + ['AA'])
#     # possible_paths = calc_possible_paths(G, useful_valves)

#     # Permutate the list of valves that have a flow rate > 0
#     max_flow_rate = 0
#     for possible_combination in tqdm(permutations(useful_valves)):
#         # For each permutation, calc the total flow rate until time runs out
#         # test_flow_rate = calc_flow_rate(G, ('DD', 'BB', 'JJ', 'HH', 'EE', 'CC'), valves)
#         # print(test_flow_rate)
#         # break
#         flow_rate = calc_flow_rate(shortest_paths, possible_combination, valves, route_len)
#         if flow_rate > max_flow_rate:
#             # Keep track of max
#             max_flow_rate = flow_rate
#             print(possible_combination, flow_rate)

#     print(f"Day 16 Part 1: {max_flow_rate}")


# def part1(filename):
#     G, valves = get_graph(filename)
#     useful_valves = [k for k, v in valves.items() if v > 0]
#     print(f"Useful_valves: {useful_valves}")

#     current_valve = 'AA'
#     total_score = 0
#     while len(useful_valves) > 1:
#         best_valve, best_score = get_valve_score(G, valves, useful_valves, current_valve)
#         print(best_valve)
#         useful_valves.remove(best_valve)
#         current_valve = best_valve
#         total_score += best_score

#     print(f"Day 16 Part 1: {total_score}")


# def bfs_test(filename):
#     G, valves = get_graph(filename)
#     bfs_tree = nx.bfs_tree(G, source='AA', depth_limit=30)
#     nx.draw_networkx(bfs_tree, with_labels=True)
#     plt.show()


# def get_valve_score(G, valves, useful_valves, current_valve):
#     best_score = 0
#     best_valve = 'AA'
#     time_left = 30
#     for valve in useful_valves:
#         distance_to_current_valve = len(nx.shortest_path(G, source=current_valve, target=valve)) - 1
#         # time_left - distance - time_to_open * flow rate of valve
#         # This is the "score" of a valve given a starting position
#         valve_score = (time_left - distance_to_current_valve - 1) * valves[valve]
#         if valve_score > best_score:
#             best_score = valve_score
#             best_valve = valve

#     return best_valve, best_score


def evalGA_part1(route, shortest_paths, useful_valves, valves):
    time_left = 30
    total_flow_rate = 0
    # Start with the distance between AA starting point and the first valve
    time_left -= shortest_paths[(useful_valves[route[0]], 'AA')] - 1
    # For each combination of 2 valves in the route
    # for valve1, valve2 in zip(route, route[1:]):
    for i in range(len(route) - 1):
        valve1 = useful_valves[route[i]]
        valve2 = useful_valves[route[i+1]]
        # Subtract 1 from remaining time for opening the valve
        time_left -= 1
        total_flow_rate += time_left * valves[valve1]
        time_left -= shortest_paths[(valve1, valve2)] - 1

        if time_left <= 0:
            return (total_flow_rate,)
    # Open the last valve
    time_left -= 1
    total_flow_rate += time_left * valves[useful_valves[route[-1]]]

    return (total_flow_rate,)


def day16_1_evolutionary(filename):
    G, valves = get_graph(filename)
    useful_valves = [k for k, v in valves.items() if v > 0]
    # print(f"Useful_valves: {useful_valves}")

    route_len = len(useful_valves)
    shortest_paths = calc_shortest_paths(G, useful_valves + ['AA'])

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    # Attribute generator
    toolbox.register("indices", random.sample, range(route_len), route_len)

    # Structure initializers
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxPartialyMatched)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evalGA_part1, shortest_paths=shortest_paths, useful_valves=useful_valves, valves=valves)

    random.seed(169)

    pop = toolbox.population(n=300)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 20, stats=stats, halloffame=hof)

    return pop, stats, hof


def evalGA_part2(routes, shortest_paths, useful_valves, valves):
    # Split routes with highest nr as the cutoff point
    # List 1 is me, List 2 is the elephant
    cutoff = routes.index(len(routes) - 1)
    my_list = routes[:cutoff]
    elephant_list = routes[cutoff + 1:]
    to_process = []
    if my_list:
        to_process.append(my_list)
    if elephant_list: 
        to_process.append(elephant_list)
    # Keep track of total flow rate (combined me and elephant)
    total_flow_rate = 0

    for route in to_process:
        # After teaching the elephant, the time left is 26
        # Reset this for me and the elephant
        time_left = 26
        # Start with the distance between AA starting point and the first valve
        time_left -= shortest_paths[(useful_valves[route[0]], 'AA')] - 1
        # For each combination of 2 valves in the route
        # for valve1, valve2 in zip(route, route[1:]):
        for i in range(len(route) - 1):
            valve1 = useful_valves[route[i]]
            valve2 = useful_valves[route[i+1]]
            # Subtract 1 from remaining time for opening the valve
            time_left -= 1
            total_flow_rate += time_left * valves[valve1]
            time_left -= shortest_paths[(valve1, valve2)] - 1

            if time_left <= 0:
                return (total_flow_rate,)
        # Open the last valve
        time_left -= 1
        total_flow_rate += time_left * valves[useful_valves[route[-1]]]

    return (total_flow_rate,)


def day16_2_evolutionary(filename, generations, seed):
    G, valves = get_graph(filename)
    useful_valves = [k for k, v in valves.items() if v > 0]
    # print(f"Useful_valves: {useful_valves}")

    route_len = len(useful_valves)
    shortest_paths = calc_shortest_paths(G, useful_valves + ['AA'])

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    # Enable multiprocessing
    # I'm dumb, but I have a fast PC...
    # pool = multiprocessing.Pool()
    # toolbox.register("map", pool.map)

    # Attribute generator
    toolbox.register("indices", random.sample, range(route_len + 1), route_len + 1)

    # Structure initializers
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxPartialyMatched)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.03)
    toolbox.register("select", tools.selTournament, tournsize=5)
    # toolbox.register("select", tools.selBest)
    toolbox.register("evaluate", evalGA_part2, shortest_paths=shortest_paths, useful_valves=useful_valves, valves=valves)

    random.seed(seed)

    pop = toolbox.population(n=10000)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, 0.7, 0.3, generations, stats=stats, halloffame=hof, verbose=False)

    routes = hof.items[0]
    cutoff = routes.index(len(routes) - 1)
    my_list = routes[:cutoff]
    elephant_list = routes[cutoff + 1:]
    # print([useful_valves[i] for i in my_list])
    # print([useful_valves[i] for i in elephant_list])

    return my_list, elephant_list, hof.keys[0].values[0]



if __name__ == '__main__':
    print(math.factorial(15) / 800000 / 3600)
    # day16_1_evolutionary('data/test16_1.txt')
    # day16_1_evolutionary('data/input16_1.txt')
    # day16_2_evolutionary('data/test16_1.txt', 20, 42)
    # 2268 too low
    # 2516 too low
    # 2631 wrong?
    # 2706 wrong?
    results = []
    for seed in range(100):
        my_list, elephant_list, maxi = day16_2_evolutionary('data/input16_1.txt', 100, seed)
        print(my_list, elephant_list, maxi)
        results.append(maxi)
    
    print(f"max: {max(results)}")
    # part1_slow('data/test16_1.txt')
    # bfs_test('data/test16_1.txt')
    # part1('data/test16_1.txt')
    # part1_slow('data/input16_1.txt')
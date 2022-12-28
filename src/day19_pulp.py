import re
import numpy as np
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, LpInteger, GLPK

# ore_bot_ore = 4
# clay_bot_ore = 2
# obs_bot_ore = 3
# obs_bot_clay = 14
# geo_bot_ore = 2
# geo_bot_obs = 7

# ore_bot_ore = 2
# clay_bot_ore = 3
# obs_bot_ore = 3
# obs_bot_clay = 8
# geo_bot_ore = 3
# geo_bot_obs = 12

def parse_input(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        input_str = f.read()
    # First, split the input string into a list of strings, one for each blueprint
    blueprints = re.split(r'Blueprint \d+: ', input_str)

    # Iterate over each blueprint
    costs = []
    for blueprint in blueprints[1:]:
        # Split the blueprint into a list of strings, one for each robot
        robots = re.split(r'\. ', blueprint)
        # Initialize a list to store the costs for this blueprint
        blueprint_costs = []
        # Iterate over each robot
        for robot in robots:
            # Extract the costs for this robot using a regular expression
            costs_match = re.findall(r'\d+', robot)
            if costs_match:
                # Convert the extracted costs to integers and add them to the blueprint costs
                blueprint_costs.append(tuple(map(int, costs_match)))
        # Add the blueprint costs to the overall list of costs
        costs.append(blueprint_costs)

    return costs


def optimize(
    ore_bot_ore,
    clay_bot_ore,
    obs_bot_ore,
    obs_bot_clay,
    geo_bot_ore,
    geo_bot_obs,
    minutes=25,
    debug=False
):
    # Create the model
    model = LpProblem("day19", LpMaximize)

    # Initialize the decision variables, it is a binary decision of whether or not to get the specific resource at time t
    ore = LpVariable.dicts('ore', list(range(minutes)), cat='Binary')
    clay = LpVariable.dicts('clay', list(range(minutes)), cat='Binary')
    obsidian = LpVariable.dicts('obsidian', list(range(minutes)), cat='Binary')
    geode = LpVariable.dicts('geode', list(range(minutes)), cat='Binary')

    print(geode)
    print(type(geode[0]))

    # Add the constraints to the model

    model += (ore[0] <= 0, 'InitialOre')
    model += (clay[0] <= 0, 'InitialClay')
    model += (obsidian[0] <= 0, 'InitialObs')
    model += (geode[0] <= 0, 'InitialGeode')

    # Account for the cost of buying a bot
    # For every minute
    for t in range(1, minutes):

        # At any minute we can only build 1 bot at a time
        model += (ore[t] + clay[t] + obsidian[t] + geode[t] <= 1, f"OneBotAtATime_{t}")

        # If we decide to buy an ore bot at t, we should have enough resources for it
        # Each line below basically translates to:
        # ore[t] * ore_bot_ore -> if we buy a bot at time t, it is the cost of the bot, if we don't its zero
        # (t-i) * ore[i] -> ore production up until then
        # ore_bot_ore * ore[i] -> the cost of a potential ore bot we bought at time i

        model += lpSum(
            [t-1] +  # Production of the 1 orebot you already have
            [(t-i-1) * ore[i] for i in range(1, t)] +  # Production for each ore bot bought at any time before t
            [- ore_bot_ore * ore[i] - clay_bot_ore * clay[i] - obs_bot_ore * obsidian[i] - geo_bot_ore * geode[i] for i in range(t+1)]  # The cost of each bot bought at time t or before
        ) >= 0
        model += lpSum(
            [(t-i-1) * clay[i] for i in range(1, t)] +
            [- obs_bot_clay * obsidian[i] for i in range(t+1)]
        ) >= 0
        model += lpSum(
            [(t-i-1) * obsidian[i] for i in range(1, t)] +
            [- geo_bot_obs * geode[i] for i in range(t+1)]
        ) >= 0

        # Ore cost of Ore bot
        # model += (ore[t] * ore_bot_ore <= lpSum([
        #     (t-i) * ore[i] - ore_bot_ore * ore[i] - clay_bot_ore * clay[i] - obs_bot_ore * obsidian[i] - geo_bot_ore * geode[i]
        #     for i in range(t+1)
        # ]), f"OreBot_OreCost_{t}")
        # # Ore cost of Clay bot
        # model += (clay[t] * clay_bot_ore <= lpSum([
        #     (t-i) * ore[i] - ore_bot_ore * ore[i] - clay_bot_ore * clay[i] - obs_bot_ore * obsidian[i] - geo_bot_ore * geode[i]
        #     for i in range(t+1)
        # ]), f"ClayBot_OreCost_{t}")
        # # Ore cost of Obsidian bot
        # model += (obsidian[t] * obs_bot_ore <= lpSum([
        #     (t-i) * ore[i] - ore_bot_ore * ore[i] - clay_bot_ore * clay[i] - obs_bot_ore * obsidian[i] - geo_bot_ore * geode[i]
        #     for i in range(t+1)
        # ]), f"ObsidianBot_OreCost_{t}")
        # # Ore cost of Geode bot
        # model += (geode[t] * geo_bot_ore <= lpSum([
        #     (t-i) * ore[i] - ore_bot_ore * ore[i] - clay_bot_ore * clay[i] - obs_bot_ore * obsidian[i] - geo_bot_ore * geode[i]
        #     for i in range(t+1)
        # ]), f"GeodeBot_OreCost_{t}")

        # # # Clay cost for Obsidian bot
        # model += (obsidian[t] * obs_bot_clay <= lpSum([
        #     (t-i) * clay[i] - obs_bot_clay * obsidian[i]
        #     for i in range(t)
        # ]), f"ObsidianBot_ClayCost_{t}")

        # # Obsidian cost for Geode bot
        # model += (geode[t] * geo_bot_obs <= lpSum([
        #     (t-i) * obsidian[i] - geo_bot_obs * geode[i]
        #     for i in range(t)
        # ]), f"GeodeBot_ObsidianCost_{t}")


    # Add the objective function to the model: The amount of geodes
    # model += x + 2 * y
    model += lpSum([(minutes-1 - t) * geode[t] for t in range(1, minutes-1)])

    # print(model)

    # Solve the problem
    # status = model.solve(GLPK(msg=1))
    status = model.solve()

    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"objective: {model.objective.value()}")

    if debug:
        for t in range(1, minutes):
            print(f"[MINUTE {t}]")
            # print(clay[t].value(), [(t-i) * clay[i].value() for i in range(t)], sum([(t-i) * clay[i].value() - obs_bot_clay * obsidian[i].value() for i in range(t)]))
            # print("RESOURCES BEGIN OF MINUTE:")
            # print(f"ORE: {sum([t-1] + [(t-i-1) * ore[i].value() for i in range(1, t)] + [- ore_bot_ore * ore[i].value() - clay_bot_ore * clay[i].value() - obs_bot_ore * obsidian[i].value() - geo_bot_ore * geode[i].value() for i in range(t+1)])}")
            # print(f"CLAY: {sum([(t-i-1) * clay[i].value() for i in range(1, t)] + [- obs_bot_clay * obsidian[i].value() for i in range(t+1)])}")
            # print(f"OBS: {sum([(t-i-1) * obsidian[i].value() for i in range(1, t)] + [- geo_bot_obs * geode[i].value() for i in range(t+1)])}")
            # print(f"GEODE: {sum([(t-i-1) * geode[i].value() for i in range(1, t)])}")
            print("BUY")
            print(f"ORE: {ore[t].value()}  CLAY: {clay[t].value()}  OBSIDIAN: {obsidian[t].value()} GEODE: {geode[t].value()}")
            print("RESOURCES END OF MINUTE:")
            print(f"ORE: {sum([t] + [(t-i) * ore[i].value() for i in range(1, t)] + [- ore_bot_ore * ore[i].value() - clay_bot_ore * clay[i].value() - obs_bot_ore * obsidian[i].value() - geo_bot_ore * geode[i].value() for i in range(t+1)])}")
            print(f"CLAY: {sum([(t-i) * clay[i].value() for i in range(1, t)] + [- obs_bot_clay * obsidian[i].value() for i in range(t+1)])}")
            print(f"OBS: {sum([(t-i) * obsidian[i].value() for i in range(1, t)] + [- geo_bot_obs * geode[i].value() for i in range(t+1)])}")
            print(f"GEODE: {sum([(t-i) * geode[i].value() for i in range(1, t)])}")
            print("====")
    
    return model.objective.value()

def part1():
    blueprints = parse_input('data/test19_1.txt')
    quality_levels = []
    for i, blueprint in enumerate(blueprints):
        amount_of_geodes = optimize(
            ore_bot_ore=blueprint[0][0],
            clay_bot_ore=blueprint[1][0],
            obs_bot_ore=blueprint[2][0],
            obs_bot_clay=blueprint[2][1],
            geo_bot_ore=blueprint[3][0],
            geo_bot_obs=blueprint[3][1]
        )
        quality_levels.append(amount_of_geodes * (i+1))
    print(sum(quality_levels))


def part2():
    blueprints = parse_input('data/input19_1.txt')
    most_geodes = []
    for i, blueprint in enumerate(blueprints[:3]):
        amount_of_geodes = optimize(
            ore_bot_ore=blueprint[0][0],
            clay_bot_ore=blueprint[1][0],
            obs_bot_ore=blueprint[2][0],
            obs_bot_clay=blueprint[2][1],
            geo_bot_ore=blueprint[3][0],
            geo_bot_obs=blueprint[3][1],
            minutes=33
        )
        most_geodes.append(amount_of_geodes)
    print(most_geodes)
    print(np.prod(most_geodes))


if __name__ == '__main__':
    # part1()
    part2()
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, LpInteger, GLPK

ore_bot_ore = 4
clay_bot_ore = 2
obs_bot_ore = 3
obs_bot_clay = 14
geo_bot_ore = 2
geo_bot_obs = 7

minutes = 4

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
# Account for the cost of buying a bot
# For every minute
for t in range(minutes):

    # At any minute we can only build 1 bot at a time
    model += (ore[t] + clay[t] + obsidian[t] + geode[t] <= 1, f"OneBotAtATime_{t}")

    # If we decide to buy an ore bot at t, we should have enough resources for it
    # Each line below basically translates to:
    # ore[t] * ore_bot_ore -> if we buy a bot at time t, it is the cost of the bot, if we don't its zero
    # (t-i) * ore[i] -> ore production up until then
    # ore_bot_ore * ore[i] -> the cost of a potential ore bot we bought at time i

    model += lpSum(
        [t] +  # Production of the 1 orebot you already have
        [(t-i) * ore[i] for i in range(t)] +  # Production for each ore bot bought at any time before t
        [- ore_bot_ore * ore[i] - clay_bot_ore * clay[i] - obs_bot_ore * obsidian[i] - geo_bot_ore * geode[i] for i in range(t+1)]  # The cost of each bot bought at time t or before
    ) >= 0
    model += lpSum(
        [(t-i) * clay[i] for i in range(t)] +
        [- obs_bot_clay * obsidian[i] for i in range(t+1)]
    ) >= 0
    model += lpSum(
        [(t-i) * obsidian[i] for i in range(t)] +
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
model += lpSum([(minutes - t) * clay[t] for t in range(minutes)])

# print(model)

# Solve the problem
# status = model.solve(GLPK(msg=1))
status = model.solve()

print(f"status: {model.status}, {LpStatus[model.status]}")
print(f"objective: {model.objective.value()}")

for t in range(minutes):
    print(t)
    # print(clay[t].value(), [(t-i) * clay[i].value() for i in range(t)], sum([(t-i) * clay[i].value() - obs_bot_clay * obsidian[i].value() for i in range(t)]))
    print(f"ORE: {ore[t].value()} {sum([t] + [(t-i) * ore[i].value() for i in range(t)] + [- ore_bot_ore * ore[i].value() - clay_bot_ore * clay[i].value() - obs_bot_ore * obsidian[i].value() - geo_bot_ore * geode[i].value() for i in range(t+1)])}")
    print(f"CLAY: {clay[t].value()} {sum([(t-i) * clay[i].value() for i in range(t)] + [- obs_bot_clay * obsidian[i].value() for i in range(t+1)])}")
    print(f"OBS: {obsidian[t].value()} {sum([(t-i) * obsidian[i].value() for i in range(t)] + [- geo_bot_obs * geode[i].value() for i in range(t+1)])}")
    print(f"GEODE: {geode[t].value()} {sum([(t-i) * geode[i].value() for i in range(t)])}")
    print("====")
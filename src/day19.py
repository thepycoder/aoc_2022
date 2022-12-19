from dataclasses import dataclass, replace, fields
from queue import Queue
import re


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


@dataclass
class Blueprint:
    ore: dict
    clay: dict
    obsidian: dict
    geode: dict


@dataclass
class BotNet:
    ore: int
    clay: int
    obsidian: int
    geode: int

    @property
    def total(self):
        return self.ore + self.clay*100 + self.obsidian*1000 + self.geode*10000


@dataclass
class State:
    time: int
    ore: int
    clay: int
    obsidian: int
    geode: int

    def update_resources(self, botnet: BotNet):
        self.ore += botnet.ore
        self.clay += botnet.clay
        self.obsidian += botnet.obsidian
        self.geode += botnet.geode

    @property
    def total(self):
        return self.ore + self.clay*100 + self.obsidian*1000 + self.geode*10000


# @profile
def buy_bot(current_state, blueprint, current_bots, bot_type):
    # Or if we can buy a new ore bot
    if all([getattr(current_state, ore_type) >= ore_needed
            for ore_type, ore_needed in getattr(blueprint, bot_type).items()]):
        # Add buying a new one to possible options to explore
        new_state = replace(current_state)
        new_bots = replace(current_bots)
        # Current bots still go and fetch resources, using the old botnet
        new_state.update_resources(current_bots)
        # Now actually "pay" for the bot
        for ore_type, ore_needed in getattr(blueprint, bot_type).items():
            amount_of_resource = getattr(new_state, ore_type)
            amount_of_resource -= ore_needed
            setattr(new_state, ore_type, amount_of_resource)
        amount_of_bots = getattr(new_bots, bot_type)
        amount_of_bots += 1
        setattr(new_bots, bot_type, amount_of_bots)
        new_state.time += 1

        return new_state, new_bots
    return None, None


# @profile
def day19_1(blueprint, maxdepth=25):
    # Keep a queue of states at each time interval. Basically we're doing BFS again
    to_process = Queue()
    starting_state = (State(0, 0, 0, 0, 0), BotNet(1, 0, 0, 0))
    to_process.put(starting_state)

    # Most expensive items
    most_ore = 0
    most_clay = 0
    for costs in blueprint.__dict__.values():
        if costs.get('ore') and costs.get('ore') > most_ore:
            most_ore = costs.get('ore')
        if costs.get('clay') and costs.get('clay') > most_clay:
            most_clay = costs.get('clay')

    time_tracker = 2
    final_states = []
    while not to_process.empty():
        # What state are we in?
        current_state, current_bots = to_process.get()

        # We've arrived at the end of the tree! Skip this one, so the queue will go empty 
        # and break the loop
        if current_state.time == maxdepth:
            final_states.append((current_state, current_bots))
            continue
        if current_state.time == time_tracker:
            print(f"Now at time {time_tracker} with Q size {to_process.qsize()}")
            time_tracker += 1
            # Sort the possible solutions with some heuristics to keep dimension down
            new_queue = Queue()
            current_elements = list(to_process.queue) + [(current_state, current_bots)]
            if len(current_elements) > 2:
                # Sort the current elements (total bots first then total resources)
                current_elements.sort(key=lambda x: (-x[1].total, -x[0].total))
                pass
                for element1, element2 in zip(current_elements, current_elements[1:]):
                    if element1[0].ore < 2*most_ore or element1[0].clay < 2*most_clay:
                        new_queue.put(element1)
                    # elif element1[0].total >= element2[0].total and element1[1].total >= element2[1].total:
                    #     # If the lower sorted element is lower in both resources and bots
                    #     # No use in keeping any of the lower ones around
                    #     new_queue.put(element1)
                    #     break
                to_process = new_queue
                continue

        # Doing nothing is always an option, replace function just copies the dataclass obj
        new_state_nothing = replace(current_state)
        new_bots_nothing = replace(current_bots)
        new_state_nothing.update_resources(new_bots_nothing)
        new_state_nothing.time += 1
        to_process.put((new_state_nothing, new_bots_nothing))

        for bot_type in ['ore', 'clay', 'obsidian', 'geode']:
            new_bot_state, new_bot_bots = buy_bot(current_state, blueprint, current_bots, bot_type)
            if new_bot_state:
                to_process.put((new_bot_state, new_bot_bots))

    i, maxi = max(enumerate([f[0].geode for f in final_states]), key=lambda x: x[1])
    for final_state in final_states:
        state = final_state[0]
        if state.geode == maxi and state.ore == 6 and state.clay == 41 and state.obsidian == 8:
            print(final_state)
            print('\n')
    return maxi, final_states[i]


if __name__ == '__main__':
    blueprints = parse_input('data/test19_1.txt')
    all_blueprints = []
    for b in blueprints:
        blueprint = Blueprint(
            ore={'ore': b[0][0]},
            clay={'ore': b[1][0]},
            obsidian={'ore': b[2][0], 'clay': b[2][1]},
            geode={'ore': b[3][0], 'obsidian': b[3][1]},
        )
        all_blueprints.append(day19_1(blueprint))
        break
    print(all_blueprints)

import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class Monkey:
    name: str
    operation: str
    number: int


def parse_input(input_line, G):
    name, details = input_line.split(": ")
    split_details = details.split()

    if len(split_details) == 1:
        G.add_node(name, operation=None, number=int(split_details[0]))
    else:
        G.add_node(name, operation=split_details[1], number=None)
        G.add_edge(name, split_details[0])
        G.add_edge(name, split_details[2])


# Part 1
with open('data/input21_1.txt', 'r', encoding='utf-8') as f:
    G = nx.DiGraph()
    input_list = [parse_input(monkey, G) for monkey in f.readlines()]

# Show the pretty graph
# nx.draw(G, with_labels=True)
# plt.show()

# Sanity check
# outs = []
# for node in G:
#     outs.append(G.in_degree(node))
# print(max(outs))

while len(G.nodes) != 1:
    leaf_nodes = sorted([(node, nx.shortest_path_length(G, 'root', node)) for node in G.nodes if G.out_degree[node] == 0], key=lambda x: -x[1])
    # print(leaf_nodes)

    for leaf_node, depth in leaf_nodes:
        # Skip the siblings of which we already saw the other sibling
        if leaf_node not in G.nodes:
            continue
        # Get node parent
        parent = list(G.predecessors(leaf_node))[0]

        # Get the other child of the parent
        children = [n for n in G.successors(parent)]
        degrees = [G.out_degree[n] for n in children]
        if max(degrees) > 0:
            continue

        # Perform operation
        operation_result = eval(str(G.nodes[children[0]]['number']) + G.nodes[parent]['operation'] + str(G.nodes[children[1]]['number']))

        # Store result as number
        G.nodes[parent]['number'] = operation_result

        if depth == 2:
            print(f"{leaf_node}: {operation_result}")

        # Remove both children from the graph
        G.remove_node(children[0])
        G.remove_node(children[1])
        # G.remove_edge(parent, children[0])
        # G.remove_edge(parent, children[1])

        # print(G.nodes)
        # print(G.edges)

    # Show the pretty graph
    # nx.draw(G, with_labels=True)
    # plt.show()
print(G.nodes['root'])


def parse_input_2(input_line, G):
    name, details = input_line.split(": ")
    split_details = details.split()

    if name == 'humn':
        G.add_node(name, operation=None, number=None)
        return
    # if name == 'root':
    #     G.add_node(name, operation='==', number=None)
    #     G.add_edge(name, split_details[0])
    #     G.add_edge(name, split_details[2])
    #     return

    if len(split_details) == 1:
        G.add_node(name, operation=None, number=int(split_details[0]))
    else:
        G.add_node(name, operation=split_details[1], number=None)
        G.add_edge(name, split_details[0])
        G.add_edge(name, split_details[2])


# Part 2
with open('data/input21_1.txt', 'r', encoding='utf-8') as f:
    G = nx.DiGraph()
    [parse_input_2(monkey, G) for monkey in f.readlines()]

# Show the pretty graph
# nx.draw_networkx(G, with_labels=True)
# plt.show()

# Sanity check
# outs = []
# for node in G:
#     outs.append(G.in_degree(node))
# print(max(outs))

# Set the human node with my testinput
# G.nodes['humn']['number'] = 301
# G.nodes['humn']['number'] = 7500329760671.045
while len(G.nodes) != 1:
    leaf_nodes = sorted([(node, nx.shortest_path_length(G, 'root', node)) for node in G.nodes if G.out_degree[node] == 0], key=lambda x: -x[1])
    print(leaf_nodes)

    for leaf_node, depth in leaf_nodes:
        # Skip the siblings of which we already saw the other sibling
        if leaf_node not in G.nodes:
            continue

        # Get node parent
        parent = list(G.predecessors(leaf_node))[0]

        # Get the other child of the parent
        children = [n for n in G.successors(parent)]
        degrees = [G.out_degree[n] for n in children]
        if parent == 'root':
            print(leaf_node)
            root_child_sibling_nr = G.nodes[leaf_node]['number']
            print(root_child_sibling_nr)
            break
        if max(degrees) > 0:
            continue
        if 'humn' in children:
            continue

        # Perform operation
        operation_result = eval(str(G.nodes[children[0]]['number']) + G.nodes[parent]['operation'] + str(G.nodes[children[1]]['number']))

        # Store result as number
        G.nodes[parent]['number'] = operation_result

        # Remove both children from the graph
        G.remove_node(children[0])
        G.remove_node(children[1])
        # G.remove_edge(parent, children[0])
        # G.remove_edge(parent, children[1])

        # print(G.nodes)
        # print(G.edges)

    if parent == 'root':
        print(root_child_sibling_nr)
        break

print(f"Result partial tree: {root_child_sibling_nr}")

inverse_mapping = {
    '+': '-',
    '-': '+',
    '*': '/',
    '/': '*'
}

# Skip root
nodes_to_check = nx.shortest_path(G, 'root', 'humn')[1:-1]
# Set the value of the root sibling that still has None
assert G.nodes[nodes_to_check[0]]['number'] is None
G.nodes[nodes_to_check[0]]['number'] = root_child_sibling_nr

# Then for each of the nodes in our tree towards humn
for parent in nodes_to_check:
    # Get both children
    children = [n for n in G.successors(parent)]

    child0, child0_value = children[0], G.nodes[children[0]]['number']
    child1, child1_value = children[1], G.nodes[children[1]]['number']
    parent_value = G.nodes[parent]['number']
    print(f"Node {parent} has value {parent_value} and children: {children}")
    parent_operation = G.nodes[parent]['operation']
    inv_parent_operation = inverse_mapping[parent_operation]
    child_value = child0_value if child0_value is not None else child1_value

    if parent_operation == '/' or parent_operation == '-':
        if child0_value is None:
            child_result = eval(str(child1_value) + inv_parent_operation + str(parent_value))
        elif child1_value is None:
            child_result = eval(str(child0_value) + parent_operation + str(parent_value))
        else:
            raise ValueError("Bad")
    if parent_operation == '+' or parent_operation == '*':
        if child0_value is None:
            child_result = eval(str(parent_value) + inv_parent_operation + str(child1_value))
        elif child1_value is None:
            child_result = eval(str(parent_value) + inv_parent_operation + str(child0_value))
        else:
            raise ValueError("Bad")

    print(child_result)
    # Set the value of child0
    G.nodes[child0 if child0_value is None else child1]['number'] = child_result

print(child_result)

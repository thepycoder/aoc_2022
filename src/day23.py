from collections import deque


# @profile
def generate_proposal(elf, elves, directions):
    no_one = True
    directions_valid = []
    proposals = []
    for direction in directions:
        for coord in direction:
            proposal = (elf[0] + coord[0], elf[1] + coord[1])
            if proposal in elves:
                directions_valid.append(False)
                no_one = False
                proposals.append(False)
                break
        else:
            directions_valid.append(True)
            proposals.append((elf[0] + direction[1][0], elf[1] + direction[1][1]))
    if no_one or True not in directions_valid:
        return False
    else:
        return proposals[directions_valid.index(True)]
    

def display_elves(elves):
    leftmost, rightmost, upmost, downmost = get_bounds(elves)
    for row in range(upmost, downmost + 1):
        rowline = "."*leftmost
        for col in range(leftmost, rightmost + 1):
            if (row, col) in elves:
                rowline += '#'
            else:
                rowline += '.'
        print(rowline)
    print("\n\n")


# @profile
def day23_1(filename):
    # Keep a set of coordinates as the elves, faster lookup in set, but we need to keep order
    elves = []
    previous_elves = [0]

    with open(filename, "r") as f:
        for row, line in enumerate(f.readlines()):
            for col, char in enumerate(line):
                if char == '#':
                    elves.append((row, col))
    
    # Coord system = (row, col) in case we need numpy later
    north = [(-1, -1), (-1, 0), (-1, 1)]
    south = [(1, -1), (1, 0), (1, 1)]
    west = [(-1, -1), (0, -1), (1, -1)]
    east = [(-1, 1), (0, 1), (1, 1)]
    
    # Keep deque because we can easily rotate it
    directions = deque([north, south, west, east])
    
    round_nr = 0
    # for _ in range(10):
    while sorted(previous_elves) != sorted(elves):
        print(f"Round: {round_nr}")
        previous_elves = elves.copy()
        proposal_elves = []
        proposals = []
        stationary_elves = []
        
        # First half round
        # Get all neighbors using lookup in elves
        # If no neighbors, do nothing
        # Test each of the deque directions in turn
        
        # For each elf, add proposal
        # Challenge: keep track of each elf's proposal, while duplicate checking so we can remove both duplicates
        # Solution: every iteration, pop an elf out of the elves list
        # Generate their proposal and check if the proposal is already in the proposal list
        # If not: add proposal to proposals list and (in the same index) add the elf to the proposal elves list
        # If dupl: add current elf in the duplicate elf list, remove the other duplicate proposal from the proposals list and 
        # in turn the corresponding elf from the proposal_elves list. Add the elf into duplicate elves list, no use for the proposal
        while elves:
            elf = elves.pop()
            proposal = generate_proposal(elf, set(elves+proposal_elves+stationary_elves), directions)
            if not proposal:
                stationary_elves.append(elf)
                continue
            if proposal in proposals:
                stationary_elves.append(elf)
                index = proposals.index(proposal)
                proposals.remove(proposal)
                stationary_elves.append(proposal_elves.pop(index))
                continue
            proposals.append(proposal)
            proposal_elves.append(elf)
        
        # End of round now is simple: execute the proposals of all elves in proposal_elves by adding their corresponding proposal from proposals
        elves = stationary_elves + proposals
        
        # Rotate the directions deque
        directions.rotate(-1)
        
        # Show the board as it is now
        if round_nr % 100 == 0:
            display_elves(elves)
        round_nr += 1
    
    leftmost, rightmost, upmost, downmost = get_bounds(elves)
    
    answer = ((rightmost - leftmost + 1) * (downmost - upmost + 1)) - len(elves)
    print(answer)

    print(round_nr)

def get_bounds(elves):
    leftmost = min([e[1] for e in elves])
    rightmost = max([e[1] for e in elves])
    upmost = min([e[0] for e in elves])
    downmost = max([e[0] for e in elves])
    return leftmost,rightmost,upmost,downmost



if __name__ == '__main__':
    # day23_1("data/test23_1.txt")
    day23_1("data/input23_1.txt")
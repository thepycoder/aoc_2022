from dataclasses import dataclass
from queue import Queue
import numpy as np


def show_map(grid, blizzards, points=[]):
    mapping = {0: '.', 1: '#', 2: 'E', 90: '>', 180: 'v', 270: '<', 360: '^'}
    grid_viz = grid.copy()
    for point in points:
        grid_viz[point[0]][point[1]] = 2
    for blizzard in blizzards:
        grid_viz[blizzard.row][blizzard.col] = blizzard.heading
    for row in grid_viz:
        rowline = "".join([str(mapping[int(e)]) for e in row])
        print(rowline)
    print("\n\n")


def get_neighbors(coord):
    x, y = coord
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    return neighbors


@dataclass
class Blizzard:
    row: int
    col: int
    heading: int

    def move(self, grid):
        if self.heading == 360:
            potential_position = (self.row-1, self.col)
            if grid[potential_position[0], potential_position[1]] == 1:
                potential_position = (grid.shape[0]-2, self.col)
        elif self.heading == 90:
            potential_position = (self.row, self.col+1)
            if grid[potential_position[0], potential_position[1]] == 1:
                potential_position = (self.row, 1)
        elif self.heading == 180:
            potential_position = (self.row+1, self.col)
            if grid[potential_position[0], potential_position[1]] == 1:
                potential_position = (1, self.col)
        elif self.heading == 270:
            potential_position = (self.row, self.col-1)
            if grid[potential_position[0], potential_position[1]] == 1:
                potential_position = (self.row, grid.shape[1]-2)

        self.row, self.col = potential_position


def parse_input_map(input_map):
    lines = input_map.split("\n")
    blizzards = []

    rows = len(lines)
    cols = max([len(l) for l in lines])

    grid = np.zeros((rows, cols))
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '.':
                grid[row][col] = 0
            elif char == '#':
                grid[row][col] = 1
            elif char == '^':
                blizzards.append(Blizzard(row, col, 360))
                # grid[row][col] = 0
            elif char == '>':
                blizzards.append(Blizzard(row, col, 90))
                # grid[row][col] = 90
            elif char == 'v':
                blizzards.append(Blizzard(row, col, 180))
                # grid[row][col] = 180
            elif char == '<':
                blizzards.append(Blizzard(row, col, 270))
                # grid[row][col] = 270

    print(grid)
    return grid, blizzards


def print_path(paths, starting_position, current_point, step_nr):
    current_point = (step_nr-1, current_point)
    previous_point = current_point
    steps_back = 1
    while previous_point != (0, starting_position):
        print(current_point)
        current_point = previous_point
        previous_point = paths[current_point]
        steps_back += 1


def day24_1(filename):
    with open(filename, 'r') as f:
        input_map = f.read()

    grid, blizzards = parse_input_map(input_map)

    q = set()
    next_q = set()
    starting_position = (0, 1)
    target_position = (grid.shape[0] - 1, grid.shape[1] - 2)
    q.add(starting_position)
    paths = {}

    # visited = set()
    step_nr = 1
    while True:
        [b.move(grid) for b in blizzards]
        blizzard_positions = set([(b.row, b.col) for b in blizzards])
        for coord in q:
            neighbors = get_neighbors(coord)
            for neighbor in neighbors + [coord]:  # One can also wait, so that's the same location as before
                # if neighbor in visited:
                #     continue
                if neighbor in blizzard_positions:
                    continue
                row, col = neighbor
                if row < 0:
                    continue
                if grid[row][col] == 1:
                    continue
                # visited.add(neighbor)
                paths[(step_nr, neighbor)] = (step_nr-1, coord)
                next_q.add(neighbor)
                if neighbor == target_position:
                    # Jackpot! Follow the trail back down
                    # print(paths)
                    print_path(paths, starting_position, coord, step_nr)
                    return step_nr
        q = next_q
        next_q = set()
        step_nr += 1


def day24_2(filename, swap=False, init_blizzards=None):
    with open(filename, 'r') as f:
        input_map = f.read()

    grid, blizzards = parse_input_map(input_map)
    if init_blizzards:
        blizzards = init_blizzards

    q = set()
    next_q = set()
    starting_position = (0, 1)
    target_position = (grid.shape[0] - 1, grid.shape[1] - 2)
    if swap:
        starting_position, target_position = target_position, starting_position
    q.add(starting_position)
    paths = {}

    # visited = set()
    step_nr = 1
    while True:
        [b.move(grid) for b in blizzards]
        blizzard_positions = set([(b.row, b.col) for b in blizzards])
        for coord in q:
            neighbors = get_neighbors(coord)
            for neighbor in neighbors + [coord]:  # One can also wait, so that's the same location as before
                # if neighbor in visited:
                #     continue
                if neighbor in blizzard_positions:
                    continue
                row, col = neighbor
                if row < 0 or row >= grid.shape[0]:
                    continue
                if grid[row][col] == 1:
                    continue
                # visited.add(neighbor)
                paths[(step_nr, neighbor)] = (step_nr-1, coord)
                next_q.add(neighbor)
                if neighbor == target_position:
                    # Jackpot! Follow the trail back down
                    # print(paths)
                    print_path(paths, starting_position, coord, step_nr)
                    return step_nr, blizzards
        q = next_q
        next_q = set()
        step_nr += 1


if __name__ == '__main__':
    # print(day24_1('data/test24_2.txt'))
    # 309 too high
    # Should be 308??
    # print(day24_1('data/input24_1.txt'))
    # Part 2
    out, out_blizzards = day24_2('data/input24_1.txt')
    back, back_blizzards = day24_2('data/input24_1.txt', swap=True, init_blizzards=out_blizzards)
    out_again, _ = day24_2('data/input24_1.txt', init_blizzards=back_blizzards)
    print(out, back, out_again, out+back+out_again)

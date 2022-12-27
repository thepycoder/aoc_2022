import numpy as np
from queue import Queue
import sys
np.set_printoptions(threshold=sys.maxsize)



def get_neighbors(coord):
    x, y, z = coord
    neighbors = [(x+1, y, z), (x-1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z-1)]
    return neighbors


def amount_adjacent_sides(coordinates, grid):
    adjacent = 0
    for coord in coordinates:
        possible_neighbors = get_neighbors(coord)
        for possible_neighbor in possible_neighbors:
            x, y, z = possible_neighbor
            try:
                adjacent += grid[x][y][z]
            except IndexError:
                continue
    return adjacent


def day18(filename):
    with open(filename) as f:
        coordinates = [np.array(list(map(int, x.split(",")))) for x in f.readlines()]

    xmax = max([x[0] for x in coordinates])
    ymax = max([x[1] for x in coordinates])
    zmax = max([x[2] for x in coordinates])

    # Make a grid in which we will keep our blocks
    grid = np.zeros((xmax+1, ymax+1, zmax+1))

    # Fill the grid
    for coordinate in coordinates:
        grid[coordinate[0]][coordinate[1]][coordinate[2]] = 1

    # Part 1
    adjacent = amount_adjacent_sides(coordinates, grid)

    answer = len(coordinates)*6 - adjacent
    print(int(answer))

    # Part 2
    # Fill up the outside, count what's left
    starting_coord = (0, 0, 0)
    q = Queue()
    q.put(starting_coord)

    visited = set()
    while not q.empty():
        coord = q.get()
        neighbors = get_neighbors(coord)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            x, y, z = neighbor
            if x < 0 or y < 0 or z < 0:
                continue
            try:
                if grid[x][y][z] == 1:
                    # Its an existing "rock", skip
                    continue
                grid[x][y][z] = 2
                visited.add(neighbor)
                q.put(neighbor)
            except IndexError:
                continue

    # Now we have the same problem as in part 1, but in reverse:
    # for each pocket of air we need to count its outside surface area. Meaning 6*blocks - adjacent_sides
    coordinates = np.where(grid == 0)
    # Make a new grid in which we will keep our blocks
    new_grid = np.zeros((xmax+1, ymax+1, zmax+1))
    # Fill it up with only the air pockets
    correct_format_coords = []
    for x, y, z in zip(*coordinates):
        new_grid[x][y][z] = 1
        correct_format_coords.append((x, y, z))
    adjacent = amount_adjacent_sides(correct_format_coords, new_grid)
    air_pockets_surface_area = len(correct_format_coords)*6 - adjacent

    print(grid)
    print(int(answer - air_pockets_surface_area))

    # 4136 too high
    # print(int(answer))


if __name__ == '__main__':
    day18("data/test18_1.txt")
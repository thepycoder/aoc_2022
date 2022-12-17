import numpy as np
from tqdm import tqdm


class Rock:
    def __init__(self, y, x, shape):
        self.corridor_width = 7
        self.y = y
        self.x = x
        self.stationary = False
        self.coordinates = []
        if shape == '-':
            for i in range(4):
                self.coordinates.append((self.y, self.x + i))
        if shape == '+':
            for i in range(3):
                self.coordinates.append((self.y + 1, self.x + i))
            self.coordinates.append((self.y + 2, self.x + 1))
            self.coordinates.append((self.y, self.x + 1))
        if shape == 'L':
            for i in range(3):
                self.coordinates.append((self.y, self.x + i))
            for i in range(1, 3):
                self.coordinates.append((self.y + i, self.x + 2))
        if shape == '|':
            for i in range(4):
                self.coordinates.append((self.y + i, self.x))
        if shape == '#':
            for i in range(2):
                self.coordinates.append((self.y + i, self.x))
                self.coordinates.append((self.y + i, self.x + 1))

    @property
    def ysize(self):
        return max([c[0] for c in self.coordinates]) - min([c[0] for c in self.coordinates])

    def get_block(self):
        return np.zeros((3 + self.ysize + 1, 7))

    def move_right(self, grid):
        moved_coordinates = [(y, x+1) for y, x in self.coordinates]
        if max([c[1] for c in moved_coordinates]) < self.corridor_width and not check_collision(moved_coordinates, grid):
            self.coordinates = moved_coordinates

    def move_left(self, grid):
        moved_coordinates = [(y, x-1) for y, x in self.coordinates]
        if min([c[1] for c in moved_coordinates]) >= 0 and not check_collision(moved_coordinates, grid):
            self.coordinates = moved_coordinates

    def gravity(self, grid):
        dropped_coordinates = [(y-1, x) for y, x in self.coordinates]
        if check_collision(dropped_coordinates, grid):
            self.stationary = True
        else:
            self.coordinates = dropped_coordinates

    def put(self, grid):
        for coord in self.coordinates:
            grid[coord[0]][coord[1]] = 5


def check_collision(coordinates, grid):
    for y, x in coordinates:
        if grid[y][x] != 0:
            return True
    return False


def display_grid(grid, iteration, rock):
    grid_to_display = grid.copy()
    for coord in rock.coordinates:
        grid_to_display[coord[0]][coord[1]] = 5 if rock.stationary else 6
    print(f"===== Iteration {iteration} ======")
    for row in np.flip(np.flip(grid_to_display), axis=1):
        print(''.join([str(int(i)) for i in row]).replace('0', '.').replace('5', '#').replace('6', '@') + '\n')


def part1(filename, end_iteration):

    def rock_generator():
        i = 0
        shapes = ['-', '+', 'L', '|', '#']
        while True:
            yield Rock(height + 3, 2, shapes[i % len(shapes)])
            i += 1

    grid = np.ones((1, 7))
    with open(filename, 'r', encoding='utf-8') as f:
        gasjets = f.read()
    # Numpy indexing is y, x
    # test = np.zeros((5, 5))
    # test[1][4] = 1
    # print(test)

    iteration = 0
    stationary_rocks = []
    height = 1

    for rock_nr, rock in tqdm(enumerate(rock_generator())):
        grid = np.vstack([grid, rock.get_block()])

        # display_grid(grid, iteration, rock)
        pass

        while not rock.stationary:
            # Move with the wind
            jet = gasjets[iteration % len(gasjets)]
            if jet == '>':
                rock.move_right(grid)
            if jet == '<':
                rock.move_left(grid)
            
            # display_grid(grid, iteration, rock)

            # Move by gravity
            rock.gravity(grid)
            # display_grid(grid, iteration, rock)

            # display_grid(grid, iteration, rock)
            iteration += 1

        rock.put(grid)
        stationary_rocks.append(rock)
        # Clean out empty rows
        grid = grid[~np.all(grid == 0, axis=1)]
        # Keep track of tower height
        height = grid.shape[0]

        if rock_nr == end_iteration - 1:
            return height


# print(grid)
print(f"Test part 1: {part1('data/test17_1.txt', 2022) - 1}")
print(f"Part 1: {part1('data/input17_1.txt', 2022) - 1}")


# print(f"Test part 2: {part1('data/test17_1.txt', 1000000000000) - 1}")
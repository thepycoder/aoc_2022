from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm
from sklearn import svm


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
    plot_data = []
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
        # Clean out empty rows
        grid = grid[~np.all(grid == 0, axis=1)]
        # Keep track of tower height
        height = grid.shape[0]

        plot_data.append((rock_nr, height))

        if rock_nr == end_iteration - 1:
            return height - 1, plot_data  # account for bottom row


height_test1, plot_data_test1 = part1('data/test17_1.txt', 2022)
print(f"Test part 1: {height_test1}")
height_part1, _ = part1('data/input17_1.txt', 2022)
print(f"Part 1: {height_part1}")

part2_iterations = 30000
height_part1, plot_data_part1 = part1('data/input17_1.txt', part2_iterations)


def part2(plot_data, previous_answer):
    x_data = [x[0] for x in plot_data]
    y_data = [y[1] for y in plot_data]

    # import plotly.express as px
    # fig = px.scatter(x=x_data, y=y_data)
    # fig.show()

    len_pattern = 1
    while True:
        diffs_this_cycle = []
        diffs_next_cycle = []
        for i in range(len(x_data) - 1 - 2*len_pattern, len(x_data) - 1 - len_pattern):
            diffs_this_cycle.append(y_data[i+1] - y_data[i])
            diffs_next_cycle.append(y_data[i+len_pattern+1] - y_data[i+len_pattern])
        if diffs_this_cycle == diffs_next_cycle:
            break
        else:
            len_pattern += 1
    print(len_pattern)
    rocks = (1000000000000 - part2_iterations)
    return (rocks // len_pattern) * sum(diffs_this_cycle) + sum(diffs_this_cycle[:(rocks % len_pattern)]) + previous_answer

# 30724685831 too low
# 1541449275380 too high
# 1541449275379 too high
# 1541449275365
print(f"Test part 2: {part2(plot_data_test1, height_test1)}")
print(f"Part 2: {part2(plot_data_part1, height_part1)}")

##########
# height_part1, plot_data = part1('data/input17_1.txt', 2022)
# print(f"Part 1: {height_part1}")

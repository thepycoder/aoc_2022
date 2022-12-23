import numpy as np


class Me:
    def __init__(self, row, col, heading, grid):
        self.row = row
        self.col = col
        self.heading = heading
        self.grid = grid

    def move(self):
        if self.heading == 0:
            return self.move_up()
        elif self.heading == 90:
            return self.move_right()
        elif self.heading == 180:
            return self.move_down()
        elif self.heading == 270:
            return self.move_left()
    
    def show_map(self, console=False):
        with open('world_map.txt', 'w') as wm:
            mapping = {1: ' ', 2: '.', 3: '#', 90: '>', 180: 'v', 270: '<', 0: '^'}
            grid_viz = self.grid.copy()
            grid_viz[self.row][self.col] = self.heading
            header = f"Row: {self.row}, Col: {self.col}, heading: {self.heading}"
            if console: print(header)
            wm.write(header + '\n')
            for row in grid_viz:
                rowline = "".join([str(mapping[int(e)]) for e in row])
                if console: print(rowline)
                wm.write(rowline + '\n')
            if console: print("\n\n")
    
    def change_heading(self, ccw):
        if ccw:
            self.heading = (self.heading - 90) % 360
        else:
            self.heading = (self.heading + 90) % 360
    
    def move_left(self):
        potential_position = [self.row, self.col - 1]
        # Wrap around
        if potential_position[1] < 0 or self.grid[potential_position[0]][potential_position[1]] == 1:
            potential_position[1] = np.where(self.grid[potential_position[0], :] != 1)[0][-1]
        return self.apply_move(potential_position)

    def move_right(self):
        potential_position = [self.row, self.col + 1]
        # Wrap around
        if potential_position[1] >= self.grid.shape[1] or self.grid[potential_position[0]][potential_position[1]] == 1:
            potential_position[1] = np.where(self.grid[potential_position[0], :] != 1)[0][0]
        return self.apply_move(potential_position)

    def move_up(self):
        potential_position = [self.row - 1, self.col]
        # Wrap around
        if potential_position[0] < 0 or self.grid[potential_position[0]][potential_position[1]] == 1:
            potential_position[0] = np.where(self.grid[:, potential_position[1]] != 1)[0][-1]
        return self.apply_move(potential_position)

    def move_down(self):
        potential_position = [self.row + 1, self.col]
        # Wrap around
        if potential_position[0] >= self.grid.shape[0] or self.grid[potential_position[0]][potential_position[1]] == 1:
            potential_position[0] = np.where(self.grid[:, potential_position[1]] != 1)[0][0]
        return self.apply_move(potential_position)

    def apply_move(self, potential_position):
        if self.check_collision(potential_position):
            return False
        self.row, self.col = potential_position
        return True
    
    def check_collision(self, position):
        if self.grid[position[0], position[1]] == 3:
            return True
        return False

class Me2:
    def __init__(self, row, col, heading, grid):
        self.row = row
        self.col = col
        self.heading = heading
        self.grid = grid
        
        self.row_section = self.grid.shape[0] / 3
        self.col_section = self.grid.shape[1] / 4

    def move(self):
        if self.heading == 0:
            return self.move_up()
        elif self.heading == 90:
            return self.move_right()
        elif self.heading == 180:
            return self.move_down()
        elif self.heading == 270:
            return self.move_left()
    
    def show_map(self, console=False):
        with open('world_map.txt', 'w') as wm:
            mapping = {1: ' ', 2: '.', 3: '#', 90: '>', 180: 'v', 270: '<', 0: '^'}
            grid_viz = self.grid.copy()
            grid_viz[self.row][self.col] = self.heading
            header = f"Row: {self.row}, Col: {self.col}, heading: {self.heading}"
            if console: print(header)
            wm.write(header + '\n')
            for row in grid_viz:
                rowline = "".join([str(mapping[int(e)]) for e in row])
                if console: print(rowline)
                wm.write(rowline + '\n')
            if console: print("\n\n")
    
    def change_heading(self, ccw):
        if ccw:
            self.heading = (self.heading - 90) % 360
        else:
            self.heading = (self.heading + 90) % 360
    
    def move_left(self):
        potential_position = [self.row, self.col - 1]
        potential_heading = self.heading
        # Wrap around
        if potential_position[1] < 0 or self.grid[potential_position[0]][potential_position[1]] == 1:
            # We're corssing the top left edge, check which side of the cube we are on by looking at the row nr
            if 0 <= potential_position[0] < self.row_section:
                # We're in section 1 and crossing boundary 1 -> 3
                potential_position = [self.row_section, self.col_section + potential_position[0]]
                # Leaving 1 going left = entering 3 going down
                potential_heading = 180
            # We're corssing the middle left edge (also side of grid)
            elif self.row_section <= potential_position[0] < 2 * self.row_section:
                # We're in section 2 and crossing boundary 2 -> 6
                potential_position = [3 * self.row_section - 1, 4 * self.col_section - (potential_position[0] - self.row_section) - 1]
                # Leaving 2 going left = entering 6 going up 
                potential_heading = 0
            # We're corssing the lower left edge
            elif 2 * self.row_section <= potential_position[0] < 3 * self.row_section:
                # We're in section 5 and crossing boundary left 5 -> 3
                potential_position = [2 * self.row_section - 1, 2 * self.col_section - (potential_position[0] - 2 * self.row_section) - 1]
                # Leaving 5 going left = entering 3 going up
                potential_heading = 0
        return self.apply_move(potential_position, potential_heading)

    def move_right(self):
        potential_position = [self.row, self.col + 1]
        potential_heading = self.heading
        # Wrap around
        if potential_position[1] >= self.grid.shape[1] or self.grid[potential_position[0]][potential_position[1]] == 1:
            # We're corssing the top right edge
            if 0 <= potential_position[0] < self.row_section:
                # We're in section 1 and crossing boundary 1 -> 6
                potential_position = [3 * self.row_section - potential_position[0] - 1, self.col_section * 4 - 1]
                # Leaving 1 going right = entering 6 going left
                potential_heading = 270
            # We're corssing the middle right edge
            elif self.row_section <= potential_position[0] < 2 * self.row_section:
                # We're in section 4 and crossing boundary 4 -> 6
                potential_position = [2 * self.row_section, 4 * self.col_section - (potential_position[0] - self.row_section) - 1]
                # Leaving 4 going right = entering 6 going down 
                potential_heading = 180
            # We're corssing the lower left edge
            elif 2 * self.row_section <= potential_position[0] < 3 * self.row_section:
                # We're in section 6 and crossing boundary 6 -> 1
                potential_position = [self.row_section - (potential_position[0] - 2 * self.row_section), 3 * self.col_section - 1]
                # Leaving 5 going left = entering 3 going up
                potential_heading = 270
        return self.apply_move(potential_position, potential_heading)

    def move_up(self):
        potential_position = [self.row - 1, self.col]
        potential_heading = self.heading
        # Wrap around
        if potential_position[0] < 0 or self.grid[potential_position[0]][potential_position[1]] == 1:
            # We're corssing the left top edge
            if 0 <= potential_position[1] < self.col_section:
                potential_position = [0, 3 * self.col_section - potential_position[1] - 1]
                potential_heading = 180
            # We're corssing the leftmiddle top edge
            elif self.col_section <= potential_position[1] < 2 * self.col_section:
                potential_position = [potential_position[1] - self.col_section , 2 * self.col_section]
                potential_heading = 90
            # We're corssing the rightmiddle top edge
            elif 2 * self.col_section <= potential_position[1] < 3 * self.col_section:
                potential_position = [self.row_section, self.col_section - (potential_position[1] - 2 * self.col_section) - 1]
                potential_heading = 180
            # We're corssing the right top edge
            elif 3 * self.col_section <= potential_position[1] < 4 * self.col_section:
                potential_position = [2 * self.row_section - (potential_position[1] - 3 * self.col_section) - 1, 3 * self.col_section - 1]
                potential_heading = 270
        return self.apply_move(potential_position, potential_heading)

    def move_down(self):
        potential_position = [self.row + 1, self.col]
        potential_heading = self.heading
        # Wrap around
        if potential_position[0] >= self.grid.shape[0] or self.grid[potential_position[0]][potential_position[1]] == 1:
            # We're corssing the left top edge
            if 0 <= potential_position[1] < self.col_section:
                potential_position = [3 * self.row_section - 1, 3 * self.col_section - potential_position[1] - 1]
                potential_heading = 0
            # We're corssing the leftmiddle top edge
            elif self.col_section <= potential_position[1] < 2 * self.col_section:
                potential_position = [3 * self.row_section - (potential_position[1] - self.col_section) - 1, 2 * self.col_section]
                potential_heading = 90
            # We're corssing the rightmiddle top edge
            elif 2 * self.col_section <= potential_position[1] < 3 * self.col_section:
                potential_position = [2 * self.row_section - 1, self.col_section - (potential_position[1] - 2 * self.col_section) - 1]
                potential_heading = 0
            # We're corssing the right top edge
            elif 3 * self.col_section <= potential_position[1] < 4 * self.col_section:
                potential_position = [2 * self.row_section - (potential_position[1] - 3 * self.col_section) - 1, 0]
                potential_heading = 90
        return self.apply_move(potential_position, potential_heading)

    def apply_move(self, potential_position, potential_heading):
        potential_position = list(map(int, potential_position))
        if self.check_collision(potential_position):
            return False
        self.row, self.col = potential_position
        self.heading = potential_heading
        return True
    
    def check_collision(self, position):
        if self.grid[position[0], position[1]] == 3:
            return True
        return False


class Me3:
    def __init__(self, row, col, heading, grid):
        self.row = row
        self.col = col
        self.heading = heading
        self.grid = grid
        
        self.row_section = self.grid.shape[0] / 4
        self.col_section = self.grid.shape[1] / 3

    def move(self):
        if self.heading == 0:
            return self.move_up()
        elif self.heading == 90:
            return self.move_right()
        elif self.heading == 180:
            return self.move_down()
        elif self.heading == 270:
            return self.move_left()
    
    def show_map(self, console=False):
        with open('world_map.txt', 'w') as wm:
            mapping = {1: ' ', 2: '.', 3: '#', 90: '>', 180: 'v', 270: '<', 0: '^'}
            grid_viz = self.grid.copy()
            grid_viz[self.row][self.col] = self.heading
            header = f"Row: {self.row}, Col: {self.col}, heading: {self.heading}"
            if console: print(header)
            # wm.write(header + '\n')
            for row in grid_viz:
                rowline = "".join([str(mapping[int(e)]) for e in row])
                if console: print(rowline)
                wm.write(rowline + '\n')
            if console: print("\n\n")
    
    def change_heading(self, ccw):
        if ccw:
            self.heading = (self.heading - 90) % 360
        else:
            self.heading = (self.heading + 90) % 360
    
    def move_left(self):
        potential_position = [self.row, self.col - 1]
        potential_heading = self.heading
        # Wrap around
        if potential_position[1] < 0 or self.grid[potential_position[0]][potential_position[1]] == 1:
            if 0 <= potential_position[0] < self.row_section:
                potential_position = [3*self.row_section - potential_position[0] - 1, 0]
                potential_heading = 90
            elif self.row_section <= potential_position[0] < 2 * self.row_section:
                potential_position = [2*self.row_section, potential_position[0] - self.row_section]
                potential_heading = 180
            elif 2 * self.row_section <= potential_position[0] < 3 * self.row_section:
                potential_position = [self.row_section - (potential_position[0] - 2*self.row_section) - 1, self.col_section]
                potential_heading = 90
            elif 3 * self.row_section <= potential_position[0] < 4 * self.row_section:
                potential_position = [0, self.col_section + (potential_position[0] - 3*self.row_section)]
                potential_heading = 180
        return self.apply_move(potential_position, potential_heading)

    def move_right(self):
        potential_position = [self.row, self.col + 1]
        potential_heading = self.heading
        # Wrap around
        if potential_position[1] >= self.grid.shape[1] or self.grid[potential_position[0]][potential_position[1]] == 1:
            if 0 <= potential_position[0] < self.row_section:
                potential_position = [3*self.row_section - potential_position[0] - 1, 2*self.col_section-1]
                potential_heading = 270
            elif self.row_section <= potential_position[0] < 2 * self.row_section:
                potential_position = [self.row_section - 1, 2*self.col_section + (potential_position[0] - self.row_section)]
                potential_heading = 0
            elif 2 * self.row_section <= potential_position[0] < 3 * self.row_section:
                potential_position = [self.row_section - (potential_position[0] - 2*self.row_section) - 1, 3*self.col_section-1]
                potential_heading = 270
            elif 3 * self.row_section <= potential_position[0] < 4 * self.row_section:
                potential_position = [3*self.row_section - 1, self.col_section + (potential_position[0] - 3*self.row_section)]
                potential_heading = 0
        return self.apply_move(potential_position, potential_heading)

    def move_up(self):
        potential_position = [self.row - 1, self.col]
        potential_heading = self.heading
        # Wrap around
        if potential_position[0] < 0 or self.grid[potential_position[0]][potential_position[1]] == 1:
            if 0 <= potential_position[1] < self.col_section:
                potential_position = [potential_position[1] + self.row_section, self.col_section]
                potential_heading = 90
            elif self.col_section <= potential_position[1] < 2 * self.col_section:
                potential_position = [3*self.row_section + (potential_position[1] - self.col_section), 0]
                potential_heading = 90
            elif 2 * self.col_section <= potential_position[1] < 3 * self.col_section:
                potential_position = [4*self.row_section-1, potential_position[1] - 2*self.col_section]
                potential_heading = 0
        return self.apply_move(potential_position, potential_heading)

    def move_down(self):
        potential_position = [self.row + 1, self.col]
        potential_heading = self.heading
        # Wrap around
        if potential_position[0] >= self.grid.shape[0] or self.grid[potential_position[0]][potential_position[1]] == 1:
            if 0 <= potential_position[1] < self.col_section:
                potential_position = [0, 2*self.col_section + potential_position[1]]
                potential_heading = 180
            elif self.col_section <= potential_position[1] < 2 * self.col_section:
                potential_position = [3*self.row_section + (potential_position[1] - self.col_section), self.col_section-1]
                potential_heading = 270
            elif 2 * self.col_section <= potential_position[1] < 3 * self.col_section:
                potential_position = [self.row_section + (potential_position[1] - 2*self.col_section), 2*self.col_section-1]
                potential_heading = 270
        return self.apply_move(potential_position, potential_heading)

    def apply_move(self, potential_position, potential_heading):
        potential_position = list(map(int, potential_position))
        if self.check_collision(potential_position):
            return False
        self.row, self.col = potential_position
        self.heading = potential_heading
        return True
    
    def check_collision(self, position):
        if self.grid[position[0], position[1]] == 3:
            return True
        return False
     

def parse_input_map(input_map):
    lines = input_map.split("\n")
    
    rows = len(lines)
    cols = max([len(l) for l in lines])
    
    grid = np.ones((rows, cols))
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '.':
                grid[row][col] = 2
            elif char == '#':
                grid[row][col] = 3
    
    print(grid)
    return grid


def parse_instructions(input_instructions):
    instructions = []
    buffer = ""
    for char in input_instructions.strip():
        if not char.isdigit():
            instructions.append((int(buffer), char))
            buffer = ""
            continue
        buffer += char
    if buffer:
        instructions.append((int(buffer), None))
    return instructions
    

def day22_1(player_obj, instructions):    
    for move_amount, rotation in instructions:
        for _ in range(move_amount):
            success = player_obj.move()
            if not success:
                break
            # player_obj.show_map()
        if rotation:
            player_obj.change_heading(rotation == 'L')
        # player_obj.show_map()
    
    heading_score_mapping = {90: 0, 180: 1, 270: 2, 0: 3}
    print(1000*(player_obj.row+1) + 4*(player_obj.col+1) + heading_score_mapping[player_obj.heading])


def parse_input(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        input_map, input_instructions = f.read().split("\n\n")
    
    grid = parse_input_map(input_map)
    instructions = parse_instructions(input_instructions)
    return grid, instructions

if __name__ == '__main__':
    grid, instructions = parse_input("data/input22_1.txt")

    # Part 1
    # me = Me(
    #     row=0,
    #     col=np.where(grid[0, :] == 2)[0][0],
    #     heading=90,
    #     grid=grid.copy()
    # )
    # day22_1(me, instructions)
    
    ## Part 2 example
    # me2 = Me2(
    #     row=0,
    #     col=np.where(grid[0, :] == 2)[0][0],
    #     heading=90,
    #     grid=grid.copy()
    # )
    # day22_1(me2, instructions)
    
    ## Part 2 Input
    me3 = Me3(
        row=0,
        col=np.where(grid[0, :] == 2)[0][0],
        heading=90,
        grid=grid.copy()
    )
    day22_1(me3, instructions)
    
    # 80393 too high
    # 48416 too high p2
    # 16535 too low p2
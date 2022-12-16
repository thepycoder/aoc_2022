"""Day 14"""


SOURCE = (500, 0)


def read_input(filestring):
    with open(filestring, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        coords = {}
        for line in lines:
            coordinates = line.replace(' -> ', ',').split(",")
            for i in range(0, len(coordinates) - 3, 2):
                x1, y1, x2, y2 = map(int, (coordinates[i], coordinates[i+1], coordinates[i+2], coordinates[i+3]))
                if x1 != x2:
                    line = list(zip(range(*sorted([x1, x2])), [y1] * abs(x1 - x2)))
                elif y1 != y2:
                    line = list(zip([x1] * abs(y1 - y2), range(*sorted([y1, y2]))))
                for element in line + [(x1, y1), (x2, y2)]:
                    coords[element] = "#"
        depth = max(x[1] for x in coords)

    return coords, depth


def step(coords, sand):
    # Fall down
    if (new_sand := (sand[0], sand[1] + 1)) not in coords:
        return new_sand

    # Down and left
    if (new_sand := (sand[0] - 1, sand[1] + 1)) not in coords:
        return new_sand

    # Down and right
    if (new_sand := (sand[0] + 1, sand[1] + 1)) not in coords:
        return new_sand

    # Steady
    return sand


def part1(filestring):
    coords, bottom_rock = read_input(filestring)

    sand_heap = []
    falling_sand = SOURCE
    while falling_sand[1] < bottom_rock:
        new_coordinate = step(coords, falling_sand)
        if new_coordinate == falling_sand:
            # Sand is stuck, start new drop
            sand_heap.append(falling_sand)
            coords[falling_sand] = "o"
            falling_sand = SOURCE
        else:
            falling_sand = new_coordinate

    print(f"Day 14 Part 1: {len(sand_heap)}")


def part2(filestring):
    coords, bottom_rock = read_input(filestring)
    floor = bottom_rock + 2

    sand_heap = [(0, 0)]
    falling_sand = SOURCE
    while sand_heap[-1] != SOURCE:
        new_coordinate = step(coords, falling_sand)
        if new_coordinate == falling_sand or new_coordinate[1] == floor:
            # Sand is stuck, start new drop
            sand_heap.append(falling_sand)
            coords[falling_sand] = "o"
            falling_sand = SOURCE
        else:
            falling_sand = new_coordinate
    print(sorted(sand_heap))
    print(f"Day 14 Part 2: {len(sand_heap) - 1}")




if __name__ == "__main__":
    part1("data/test14_1.txt")
    part1("data/input14_1.txt")

    part2("data/test14_1.txt")
    part2("data/input14_1.txt")

import math
import re

from tqdm import tqdm


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def read_input(filename):
    regex = r"Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)"
    sensors = []
    beacons = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            groups = re.findall(regex, line, flags=re.MULTILINE)[0]
            sensor = Coord(int(groups[0]), int(groups[1]))
            beacon = Coord(int(groups[2]), int(groups[3]))
            sensors.append(sensor)
            beacons.append(beacon)

    return sensors, beacons


def combine_ranges(ranges):
    combined_ranges = []

    for irange in ranges:
        flag = True
        for erange in combined_ranges:
            # if overlapping left
            if irange[0] < erange[0] and erange[0] - 1 <= irange[1] <= erange[1]:
                erange[0] = irange[0]
                flag = False
                continue
            # if overlapping right
            if irange[1] >= erange[1] and erange[0] <= irange[0] <= erange[1] + 1:
                erange[1] = irange[1]
                flag = False
                continue
            # completely outside
            if irange[0] <= erange[0] and irange[1] >= erange[1]:
                erange[0] = irange[0]
                erange[1] = irange[1]
                flag = False
                break
            # completely inside
            if irange[0] >= erange[0] and irange[1] <= erange[1]:
                flag = False
                break
        # 2 existing ranges could now have become overlapping
        combined_ranges = combine_ranges(combined_ranges)
        # In this case, the range is not (partly) overlapping with any of the existing ranges, so we add it
        if flag:
            combined_ranges.append(irange)

    return combined_ranges


# @profile
def day15_1(sensors, beacons, rownr):
    row = []
    for sensor, beacon in zip(sensors, beacons):
        sensor_range = sensor - beacon
        if sensor.y + sensor_range >= rownr >= sensor.y - sensor_range:
            x_distance_sensor_left_intersection = sensor_range - abs(sensor.y - rownr)
            row.append([sensor.x - x_distance_sensor_left_intersection, sensor.x + x_distance_sensor_left_intersection])

    combined_ranges = combine_ranges(row)
    # print(combined_ranges)
    total = 0
    for r in combined_ranges:
        total += r[1] - r[0]
    # print(len(row), sorted([c.x for c in row]))
    # print(total)

    return total, combined_ranges


def day15_2(sensors, beacons, max_size):
    for rownr in tqdm(range(max_size)):
        _, combined_range_row = day15_1(sensors, beacons, rownr)
        if len(combined_range_row) > 1:
            x = combined_range_row[0][1] + 1
            return x * 4000000 + rownr


if __name__ == '__main__':
    test_sensors, test_beacons = read_input("data/test15_1.txt")
    sensors, beacons = read_input("data/input15_1.txt")
    # pairs = [[1, 20], [15, 20], [25, 30]]
    # minimum = 0
    # maximum = 30
    # missing_ranges = combine_ranges(pairs)
    # print(missing_ranges)
    print(day15_1(test_sensors, test_beacons, 10))
    print(day15_1(sensors, beacons, 2000000))
    print(day15_2(test_sensors, test_beacons, 20))
    print(day15_2(sensors, beacons, 4000000))

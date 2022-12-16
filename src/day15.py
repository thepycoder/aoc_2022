import math
import re


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
    largest_distance_between_sensor_and_beacon = 0
    most_left = 0
    most_right = 0
    with open(filename, 'r') as f:
        for line in f.readlines():
            groups = re.findall(regex, line, flags=re.MULTILINE)[0]
            sensor = Coord(int(groups[0]), int(groups[1]))
            beacon = Coord(int(groups[2]), int(groups[3]))
            sensors.append(sensor)
            beacons.append(beacon)

            if sensor - beacon > largest_distance_between_sensor_and_beacon:
                largest_distance_between_sensor_and_beacon = sensor - beacon
            
            for c in (sensor, beacon):
                if c.x < most_left:
                    most_left = c.x
                if c.x > most_right:
                    most_right = c.x

    return sensors, beacons, largest_distance_between_sensor_and_beacon, most_left, most_right


def combine_ranges(ranges):
    combined_ranges = []

    for irange in ranges:
        flag = True
        for erange in combined_ranges:
            # if overlapping left
            if irange[0] < erange[0] and erange[0] <= irange[1] <= erange[1]:
                erange[0] = irange[0]
                flag = False
                continue
            # if overlapping right
            if irange[1] >= erange[1] and erange[0] <= irange[0] <= erange[1]:
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


def day15(filename, rownr):
    row = []
    sensors, beacons, largest_distance_between_sensor_and_beacon, most_left, most_right = read_input(filename)
    for sensor, beacon in zip(sensors, beacons):
        sensor_range = sensor - beacon
        if sensor.y + sensor_range >= rownr >= sensor.y - sensor_range:
            x_distance_sensor_left_intersection = sensor_range - abs(sensor.y - rownr)
            left_intersection = Coord(sensor.x - x_distance_sensor_left_intersection, rownr)
            right_intersection = Coord(sensor.x + x_distance_sensor_left_intersection, rownr)
            row.append([left_intersection.x, right_intersection.x])

    combined_ranges = combine_ranges(row)
    print(combined_ranges)
    total = 0
    for r in combined_ranges:
        total += r[1] - r[0]
    # print(len(row), sorted([c.x for c in row]))
    print(total)

if __name__ == '__main__':
    # pairs = [[1, 20], [15, 20], [25, 30]]
    # minimum = 0
    # maximum = 30
    # missing_ranges = combine_ranges(pairs)
    # print(missing_ranges)
    day15("data/test15_1.txt", 10)
    day15("data/input15_1.txt", 2000000)
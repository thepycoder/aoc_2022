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


def day15(filename, rownr):
    row = set()
    sensors, beacons, largest_distance_between_sensor_and_beacon, most_left, most_right = read_input(filename)
    for sensor, beacon in zip(sensors, beacons):
        sensor_range = sensor - beacon
        if sensor.y + sensor_range >= rownr >= sensor.y - sensor_range:
            x_distance_sensor_left_intersection = sensor_range - abs(sensor.y - rownr)
            left_intersection = Coord(sensor.x - x_distance_sensor_left_intersection, rownr)
            right_intersection = Coord(sensor.x + x_distance_sensor_left_intersection, rownr)
            for x in range(left_intersection.x, right_intersection.x):
                row.add(Coord(x, rownr))

    # print(len(row), sorted([c.x for c in row]))
    print(len(row))

if __name__ == '__main__':
    day15("data/test15_1.txt", 10)
    day15("data/input15_1.txt", 2000000)
import re
import unittest
from collections import namedtuple
from typing import Dict

import matplotlib.pyplot as plt


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    lines = []
    for row in data.split('\n'):
        result = re.search(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', row)
        line = (int(result.group(1)), int(result.group(2)), int(result.group(3))), \
            (int(result.group(4)), int(result.group(5)), int(result.group(6)))
        lines.append(line)
    return lines


def plot_lines(lines):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for line in lines:
        x = [i[0] for i in line]
        y = [i[1] for i in line]
        z = [i[2] for i in line]
        ax.plot(x, y, z, linewidth=2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


Point = namedtuple('Point', ['x', 'y', 'z'])


class Brick:
    env: Dict[int, 'Brick'] = {}

    def __init__(self, coordinates):
        self.id = len(self.env)
        self.env[self.id] = self
        (x1, y1, z1), (x2, y2, z2) = coordinates
        self.p1 = Point(x1, y1, z1)
        self.p2 = Point(x2, y2, z2)

    def __repr__(self):
        return f'{self.id} ({self.p1.x}, {self.p1.y}, {self.p1.z}), ({self.p2.x}, {self.p2.y}, {self.p2.z})'

    def lowest_point(self):
        return min(self.p1.z, self.p2.z)

    def highest_point(self):
        return max(self.p1.z, self.p2.z)

    def on_ground(self):
        return self.lowest_point() == 1


def part_one(filename):
    data = read_puzzle_input(filename)
    lines = parse_data(data)
    for line in lines:
        Brick(line)
    for brick in Brick.env.values():
        print(f'Grounded: {brick.on_ground()} {brick}')

    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(517, part_one('Day_22_input.txt'))
        self.assertEqual(-1, part_one('Day_22_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(61276, part_two('Day_21_input.txt'))
        self.assertEqual(-1, part_two('Day_22_short_input.txt'))

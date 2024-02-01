import queue
import re
import unittest
from dataclasses import dataclass
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
    ax.set_zlim(1, 300)
    plt.show()


def plot_current_lines():
    lines = []
    for brick in Brick.env.values():
        lines.append(brick.coordinate_tuple())
    plot_lines(lines)


# Point = namedtuple('Point', ['x', 'y', 'z'])
@dataclass
class Point:
    x: int
    y: int
    z: int

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


def ranges_overlap(a, b):
    return not (a[1] < b[0] or a[0] > b[1])


class Brick:
    env: Dict[int, 'Brick'] = {}

    def __init__(self, coordinates):
        self._supporting = None
        self._supported_by = None
        self.id = len(self.env)
        self.env[self.id] = self
        (x1, y1, z1), (x2, y2, z2) = coordinates
        self.p1 = Point(x1, y1, z1)
        self.p2 = Point(x2, y2, z2)
        self.bricks_below = set()
        self.bricks_above = set()

    def __repr__(self):
        return f'{self.id} ({self.p1.x}, {self.p1.y}, {self.p1.z}), ({self.p2.x}, {self.p2.y}, {self.p2.z})'

    def coordinate_tuple(self):
        return (self.p1.x, self.p1.y, self.p1.z), (self.p2.x, self.p2.y, self.p2.z)

    @staticmethod
    def load_env(lines):
        for line in lines:
            Brick(line)

    def lowest_point(self):
        return min(self.p1.z, self.p2.z)

    def highest_point(self):
        return max(self.p1.z, self.p2.z)

    def on_ground(self):
        return self.lowest_point() == 1

    def overlaps(self, other):
        x1, y1, z1 = self.p1
        x2, y2, z2 = self.p2
        x_range1 = min(x1, x2), max(x1, x2)
        y_range1 = min(y1, y2), max(y1, y2)
        z_range1 = min(z1, z2), max(z1, z2)

        x1, y1, z1 = other.p1
        x2, y2, z2 = other.p2
        x_range2 = min(x1, x2), max(x1, x2)
        y_range2 = min(y1, y2), max(y1, y2)
        z_range2 = min(z1, z2), max(z1, z2)

        x_overlap = ranges_overlap(x_range1, x_range2)
        y_overlap = ranges_overlap(y_range1, y_range2)
        z_overlap = ranges_overlap(z_range1, z_range2)
        return x_overlap, y_overlap, z_overlap

    def supported_by(self):
        if self._supported_by is None:
            self._supported_by = [b for b in self.bricks_below if b.is_one_level_below(self)]
        return self._supported_by

    def supporting(self):
        if self._supporting is None:
            self._supporting = [b for b in self.bricks_above if self.is_one_level_below(b)]
        return self._supporting

    def overlaps_xy(self, other):
        overlap_x, overlap_y, _ = self.overlaps(other)
        return overlap_x and overlap_y

    def drop(self, n):
        self.p1.z -= n
        self.p2.z -= n

    def is_one_level_below(self, other: 'Brick'):
        return self.highest_point() == other.lowest_point() - 1


def drop_bricks():
    bricks = list(Brick.env.values())
    bricks.sort(key=lambda b: b.lowest_point())

    for brick in bricks:
        if brick.on_ground():
            continue

        lower_bricks = [lower for lower in bricks if lower.lowest_point() < brick.lowest_point()]
        if not lower_bricks:
            continue

        highest_z = 1
        for lower in lower_bricks:
            if lower.overlaps_xy(brick):
                lower.bricks_above.add(brick)
                brick.bricks_below.add(lower)
                highest_z = max(highest_z, lower.highest_point() + 1)

        if brick.lowest_point() > highest_z:
            brick.drop(brick.lowest_point() - highest_z)

    bricks.sort(key=lambda b: b.lowest_point())
    return bricks


def disintegrate(removed_brick):
    for above in removed_brick.supporting():
        if len(above.supported_by()) == 1:
            return 0
    return 1


def disintegrate_chain_reaction(removed_brick):
    def can_disintegrate(count, brick):
        return count == len(brick.supported_by())

    q = queue.SimpleQueue()
    q.put(removed_brick)
    disintegrated = {removed_brick.id: True}

    while not q.empty():
        brick = q.get()
        for above in brick.supporting():
            if above.id in disintegrated:
                continue
            supports_disintegrated_count = sum(
                1 for a in above.supported_by() if a.id in disintegrated)
            if can_disintegrate(supports_disintegrated_count, above):
                disintegrated[above.id] = True
            q.put(above)
    return len(disintegrated) - 1


def part_one(filename):
    data = read_puzzle_input(filename)
    lines = parse_data(data)
    Brick.load_env(lines)
    plot_current_lines()
    resting = drop_bricks()
    plot_current_lines()
    return sum(disintegrate(b) for b in resting)


def part_two(filename):
    data = read_puzzle_input(filename)
    lines = parse_data(data)
    Brick.load_env(lines)
    resting = drop_bricks()
    return sum(disintegrate_chain_reaction(b) for b in resting)


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(517, part_one('Day_22_input.txt'))
        self.assertEqual(5, part_one('Day_22_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(61276, part_two('Day_22_input.txt'))
        self.assertEqual(7, part_two('Day_22_short_input.txt'))

    def test_ranges_overlap(self):
        self.assertTrue(ranges_overlap((1, 5), (3, 8)))
        self.assertTrue(ranges_overlap((3, 8), (1, 5)))
        self.assertFalse(ranges_overlap((1, 5), (6, 8)))
        self.assertFalse(ranges_overlap((6, 8), (1, 5)))
        self.assertTrue(ranges_overlap((1, 100), (3, 5)))

    def test_overlaps(self):
        data = read_puzzle_input('Day_22_short_input.txt')
        lines = parse_data(data)
        Brick.load_env(lines)
        self.assertFalse(all(Brick.env[0].overlaps(Brick.env[6])))
        self.assertFalse(all(Brick.env[1].overlaps(Brick.env[6])))
        self.assertFalse(all(Brick.env[2].overlaps(Brick.env[6])))
        x_overlap, y_overlap, z_overlap = Brick.env[0].overlaps(Brick.env[6])
        self.assertTrue(x_overlap)
        self.assertTrue(y_overlap)
        self.assertFalse(z_overlap)

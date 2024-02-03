import re
import unittest
from itertools import combinations

from matplotlib import pyplot as plt


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    hail = []
    for row in data.split('\n'):
        r = re.search(r'(\d+), (\d+), (\d+) @ +(-?\d+), +(-?\d+), +(-?\d+)', row)
        hail.append(
            ((int(r.group(1)), int(r.group(2)), int(r.group(3))), (int(r.group(4)), int(r.group(5)), int(r.group(6)))))
    return hail


def graph_trajectories(hail):
    dtime = 1000000000000
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for (x, y, z), (vx, vy, vz) in hail:
        x2 = x + (dtime * vx)
        y2 = y + (dtime * vy)
        z2 = z + (dtime * vz)
        ax.plot([x, x2], [y, y2], [z, z2], linewidth=1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


def find_intersections(hail, window_min, window_max):
    for h1 in hail:
        for h3 in hail:
            if h1 == h3:
                continue
            (x1, y1, _), (vx1, vy1, _) = h1
            x2, y2 = x1 + vx1, y1 + vy1
            (x3, y3, _), (vx3, vy3, _) = h3
            x4, y4 = x3 + vx3, y3 + vy3
            px_numerator = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
            denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            py_numerator = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
            print()
            print(h1)
            print(h3)
            if denominator == 0:  # lines are parallel or coincident
                print('Parallel')
                continue
            px = px_numerator / denominator
            py = py_numerator / denominator
            print(f'Intersects {px}, {py}')
            if (window_min <= px <= window_max) and (window_min <= py <= window_max):
                print('In window')


def find_intersections2(hail, window_min, window_max):
    total = 0
    for h1, h2 in combinations(hail, 2):
        (x1, y1, _), (dx1, dy1, _) = h1
        (x2, y2, _), (dx2, dy2, _) = h2
        m1 = dy1 / dx1
        m2 = dy2 / dx2
        if m1 == m2:
            continue
        b1 = y1 - m1 * x1
        b2 = y2 - m2 * x2
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
        if all((window_min <= x <= window_max,
                window_min <= y <= window_max,
                (x > x1 and dx1 > 0) or (x < x1 and dx1 < 0),
                (x < x2 and dx2 > 0) or (x < x2 and dx2 < 0))):
            total += 1
    return total


def part_one(filename, window_min, window_max):
    data = read_puzzle_input(filename)
    hail = parse_data(data)
    result = find_intersections2(hail, window_min, window_max)
    # graph_trajectories(hail)
    return result


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(18098, part_one('Day_24_input.txt', 200_000_000_000_000, 400_000_000_000_000))
        self.assertEqual(2, part_one('Day_24_short_input.txt', 7, 27))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_24_input.txt'))
        self.assertEqual(-1, part_two('Day_24_short_input.txt'))

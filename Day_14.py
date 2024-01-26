import unittest

import numpy as np


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    platform = [list(r) for r in data.split('\n')]
    return platform


def tilt_platform(platform):
    width = len(platform[0])
    for outer_row in range(len(platform)):
        for row in range(1, len(platform) - outer_row):
            for col in range(width):
                if platform[row][col] == 'O' and platform[row - 1][col] == '.':
                    platform[row][col] = '.'
                    platform[row - 1][col] = 'O'


def part_one(filename):
    data = read_puzzle_input(filename)
    platform = parse_data(data)
    tilt_platform(platform)
    for row in platform:
        print(''.join(row))
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one('Day_14_input.txt'))
        self.assertEqual(136, part_one('Day_14_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_14_input.txt'))
        self.assertEqual(-1, part_two('Day_14_short_input.txt'))

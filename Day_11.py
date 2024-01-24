import unittest

import numpy as np


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    data = [[m for m in n] for n in data.split('\n')]
    data = np.array(data)
    return data


def part_one(filename):
    data = read_puzzle_input(filename)
    parse_data(data)
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(-1, part_one('Day_11_input.txt'))
        self.assertEqual(-1, part_one('Day_11_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_11_input.txt'))
        self.assertEqual(-1, part_two('Day_11_short_input.txt'))

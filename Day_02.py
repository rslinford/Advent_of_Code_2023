import re
import unittest

import numpy as np


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    return data.split('\n')


def part_one(filename):
    data = read_puzzle_input(filename)
    document = parse_data(data)
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    document = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(part_one('Day_02_input.txt'), -1)
        self.assertEqual(part_one('Day_02_short_input.txt'), -1)

    def test_part_two(self):
        # self.assertEqual(part_two('Day_01_input.txt'), -1)
        self.assertEqual(part_two('Day_02_input.txt'), -1)
        self.assertEqual(part_two('Day_02_short_input.txt'), -1)

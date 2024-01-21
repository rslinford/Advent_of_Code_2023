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
    document_value = 0
    for row in document:
        result = re.search(r'^\D*(\d)', row)
        left_digit = result.group(1)
        result = re.search(r'(\d)\D*$', row)
        right_digit = result.group(1)
        row_value = int(left_digit+right_digit)
        document_value += row_value

    return document_value


DIGITS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def find_digits(row, digits):
    indexes = np.zeros((len(digits), 2), dtype=int)
    for i, digit in enumerate(digits):
        indexes[i][0] = row.find(digit)
        indexes[i][1] = row.rfind(digit)
    return indexes


def part_two(filename):
    data = read_puzzle_input(filename)
    document = parse_data(data)
    for row in document:
        indexes = find_digits(row, DIGITS)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(part_one('Day_01_input.txt'), 56397)
        self.assertEqual(part_one('Day_01_short_input.txt'), 142)

    def test_part_two(self):
        # self.assertEqual(part_two('Day_01_input.txt'), -1)
        self.assertEqual(part_two('Day_01_short_input_02.txt'), 281)

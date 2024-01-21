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
        row_value = int(left_digit + right_digit)
        document_value += row_value

    return document_value


DIGIT_NAMES = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
               '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
DIGIT_VALUES = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
                'nine': 9, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}


def find_digits(row, digits):
    indexes = []
    for i, digit in enumerate(digits):
        left_index = row.find(digit)
        right_index = row.rfind(digit)
        if left_index != -1 or right_index != -1:
            indexes.append([digit, left_index, right_index])
    return indexes


def part_two(filename):
    data = read_puzzle_input(filename)
    document_value = 0
    document = parse_data(data)
    for row in document:
        indexes = find_digits(row, DIGIT_NAMES)
        indexes_sorted_left = np.array(sorted(indexes, key=lambda x: x[1]))
        indexes_sorted_right = np.array(sorted(indexes, key=lambda x: x[2], reverse=True))
        digit_left = indexes_sorted_left[0][0]
        digit_right = indexes_sorted_right[0][0]
        row_value = DIGIT_VALUES[digit_left] * 10 + DIGIT_VALUES[digit_right]
        document_value += row_value
    return document_value


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(part_one('Day_01_input.txt'), 56397)
        self.assertEqual(part_one('Day_01_short_input.txt'), 142)

    def test_part_two(self):
        # self.assertEqual(part_two('Day_01_input.txt'), -1)
        self.assertEqual(part_two('Day_01_input.txt'), 55701)
        self.assertEqual(part_two('Day_01_short_input_02.txt'), 281)

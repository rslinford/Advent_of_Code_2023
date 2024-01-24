import unittest

import numpy as np


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    data = [list(a) for a in data.split('\n')]
    return np.array(data)


def find_empty_columns(space):
    columns = []
    for x in range(space.shape[1]):
        column_is_empty = True
        for y in range(space.shape[0]):
            if space[y][x] == '#':
                column_is_empty = False
                break
        if column_is_empty:
            columns.append(x)
    return columns


def find_empty_rows(space):
    rows = []
    for y in range(space.shape[0]):
        row_is_empty = True
        for x in range(space.shape[1]):
            if space[y][x] == '#':
                row_is_empty = False
                break
        if row_is_empty:
            rows.append(y)
    return rows


def expand_columns(space, columns):
    columns.sort(reverse=True)
    dots = list('.' * space.shape[0])
    for column in columns:
        space = np.insert(space, column, dots, axis=1)
    return space


def expand_rows(space, rows):
    rows.sort(reverse=True)
    dots = list('.' * space.shape[1])
    for row in rows:
        space = np.insert(space, row, dots, axis=0)
    return space


def expand(space):
    columns = find_empty_columns(space)
    space = expand_columns(space, columns)
    rows = find_empty_rows(space)
    space = expand_rows(space, rows)
    return space


def part_one(filename):
    data = read_puzzle_input(filename)
    space = parse_data(data)
    space = expand(space)
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one('Day_11_input.txt'))
        self.assertEqual(374, part_one('Day_11_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_11_input.txt'))
        self.assertEqual(-1, part_two('Day_11_short_input.txt'))

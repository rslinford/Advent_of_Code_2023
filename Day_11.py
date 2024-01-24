import itertools
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


def find_galaxies(space):
    galaxies = []
    for x in range(space.shape[1]):
        for y in range(space.shape[0]):
            if space[y][x] == '#':
                galaxies.append((x, y))
    return galaxies


def calculate_shortest_paths_naive(combos):
    tally = 0
    for (x1, y1), (x2, y2) in combos:
        distance = abs(x1 - x2) + abs(y1 - y2)
        tally += distance
    return tally


def calculate_shortest_paths(space, expansion_factor):
    combos = list(itertools.combinations(find_galaxies(space), 2))
    empty_columns = find_empty_columns(space)
    empty_rows = find_empty_rows(space)
    tally = 0
    for (x1, y1), (x2, y2) in combos:
        empty_rows_crossed = 0
        empty_columns_crossed = 0
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if x in empty_columns:
                empty_columns_crossed += 1
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if y in empty_rows:
                empty_rows_crossed += 1
        distance = abs(x1 - x2) + abs(y1 - y2) + (empty_columns_crossed + empty_rows_crossed) * expansion_factor
        tally += distance
    return tally


def part_one_naive(filename):
    data = read_puzzle_input(filename)
    space = parse_data(data)
    space = expand(space)
    galaxies = find_galaxies(space)
    combos = list(itertools.combinations(galaxies, 2))
    tally = calculate_shortest_paths_naive(combos)
    return tally


def part_one(filename):
    data = read_puzzle_input(filename)
    space = parse_data(data)
    tally = calculate_shortest_paths(space, 1)
    return tally


def part_two(filename):
    data = read_puzzle_input(filename)
    space = parse_data(data)
    tally = calculate_shortest_paths(space, 1000000 - 1)
    return tally


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(9647174, part_one('Day_11_input.txt'))
        self.assertEqual(9647174, part_one_naive('Day_11_input.txt'))
        self.assertEqual(374, part_one('Day_11_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(377318892554, part_two('Day_11_input.txt'))

import unittest
from enum import Enum, auto

import numpy as np
from colorama import Fore


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position 
"""
CONNECTORS = {'|': [Direction.NORTH, Direction.SOUTH],
              '-': [Direction.EAST, Direction.WEST],
              'L': [Direction.NORTH, Direction.EAST],
              'J': [Direction.NORTH, Direction.WEST],
              '7': [Direction.SOUTH, Direction.WEST],
              'F': [Direction.SOUTH, Direction.EAST],
              '.': []}


def possible_directions(grid, x, y):
    directions = []
    if x > 0 and (grid[y][x - 1] == '-' or grid[y][x - 1] == 'L' or grid[y][x - 1] == 'F'):
        directions.append(Direction.WEST)
    if y > 0 and (grid[y - 1][x] == '|' or grid[y - 1][x] == '7' or grid[y - 1][x] == 'F'):
        directions.append(Direction.NORTH)
    if x < grid.shape[1] - 1 and (grid[y][x + 1] == '-' or grid[y][x + 1] == 'J' or grid[y][x + 1] == '7'):
        directions.append(Direction.EAST)
    if y < grid.shape[0] - 1 and (grid[y + 1][x] == '|' or grid[y + 1][x] == 'L' or grid[y + 1][x] == 'J'):
        directions.append(Direction.SOUTH)
    return directions


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    data = [[m for m in n] for n in data.split('\n')]
    data = np.array(data)
    return data


def find_the_s(grid):
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y][x] == 'S':
                return x, y
    assert False


def print_grid(grid, x_highlight, y_highlight, color=Fore.RED):
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if x == x_highlight and y == y_highlight:
                print(color + str(grid[y][x]), end='')
            else:
                print(Fore.WHITE + str(grid[y][x]), end='')
        print()


def follow_loop(grid, x, y):
    x1, y1 = x, y
    x2, y2 = x, y
    assert grid[y1][x1] == 'S'
    # print_grid(grid, x1, y1)
    d1 = possible_directions(grid, x1, y1)
    assert len(d1) == 2
    heading1 = d1[0]
    heading2 = d1[1]
    opposite_heading1 = None
    opposite_heading2 = None
    steps_taken = 0
    while True:
        match heading1:
            case Direction.NORTH:
                y1 -= 1
                opposite_heading1 = Direction.SOUTH
            case Direction.SOUTH:
                y1 += 1
                opposite_heading1 = Direction.NORTH
            case Direction.EAST:
                x1 += 1
                opposite_heading1 = Direction.WEST
            case Direction.WEST:
                x1 -= 1
                opposite_heading1 = Direction.EAST
        match heading2:
            case Direction.NORTH:
                y2 -= 1
                opposite_heading2 = Direction.SOUTH
            case Direction.SOUTH:
                y2 += 1
                opposite_heading2 = Direction.NORTH
            case Direction.EAST:
                x2 += 1
                opposite_heading2 = Direction.WEST
            case Direction.WEST:
                x2 -= 1
                opposite_heading2 = Direction.EAST
        steps_taken += 1
        print_grid(grid, x1, y1, color=Fore.BLUE)
        print()
        print_grid(grid, x2, y2, color=Fore.RED)
        print()
        print()
        if x1 == x2 and y1 == y2:
            return steps_taken
        d1 = possible_directions(grid, x1, y1)
        if opposite_heading1 in d1:
            d1.remove(opposite_heading1)
        heading1 = d1[0]
        d2 = possible_directions(grid, x2, y2)
        if opposite_heading2 in d2:
            d2.remove(opposite_heading2)
        heading2 = d2[0]


def part_one(filename):
    data = read_puzzle_input(filename)
    grid = parse_data(data)
    x, y = find_the_s(grid)
    return follow_loop(grid, x, y)


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one('Day_10_input.txt'))
        # self.assertEqual(4, part_one('Day_10_short_input.txt'))
        # self.assertEqual(8, part_one('Day_10_short_input_02.txt'))
        self.assertEqual(4, part_one('Day_10_short_input_03.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_10_input.txt'))
        self.assertEqual(-1, part_two('Day_10_short_input.txt'))

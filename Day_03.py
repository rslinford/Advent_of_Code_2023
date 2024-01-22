import unittest
from dataclasses import dataclass


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    data = data.split('\n')
    for row in data:
        row += '.'
    return data


@dataclass
class PartNumber:
    number: str = ''
    next_to_symbol: bool = False


def is_symbol(c):
    if c == '.':
        return False
    if '0' <= c <= '9':
        return False
    return True


def is_next_to_symbol(schematic, x, y) -> bool:
    width = len(schematic[0])
    if x > 0:
        if is_symbol(schematic[y][x - 1]):
            return True
        if y > 0:
            if is_symbol(schematic[y - 1][x - 1]):
                return True
        if y < len(schematic) - 1:
            if is_symbol(schematic[y + 1][x - 1]):
                return True
    if y > 0:
        if is_symbol(schematic[y - 1][x]):
            return True
        if x < width - 1:
            if is_symbol(schematic[y - 1][x + 1]):
                return True
    if x < width - 1:
        if is_symbol(schematic[y][x + 1]):
            return True
        if y < len(schematic) - 1:
            if is_symbol(schematic[y + 1][x + 1]):
                return True
    if y < len(schematic) - 1:
        if is_symbol(schematic[y + 1][x]):
            return True

    return False


def part_one(filename):
    data = read_puzzle_input(filename)
    schematic = parse_data(data)
    pn = PartNumber()
    sum_of_part_numbers = 0
    for y, row in enumerate(schematic):
        for x, c in enumerate(row):
            if '0' <= c <= '9':
                pn.number += c
                if is_next_to_symbol(schematic, x, y):
                    pn.next_to_symbol = True
            else:
                if pn.next_to_symbol:
                    sum_of_part_numbers += int(pn.number)
                pn = PartNumber()

    return sum_of_part_numbers


def part_two(filename):
    data = read_puzzle_input(filename)
    schematic = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(539433, part_one('Day_03_input.txt'))
        self.assertEqual(4361, part_one('Day_03_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_03_input.txt'))
        self.assertEqual(-1, part_two('Day_03_short_input.txt'))

    def test_is_next_to_symbol(self):
        data = read_puzzle_input('Day_03_short_input.txt')
        schematic = parse_data(data)
        self.assertFalse(is_next_to_symbol(schematic, 1, 0))
        self.assertTrue(is_next_to_symbol(schematic, 2, 0))
        self.assertTrue(is_next_to_symbol(schematic, 2, 4))
        self.assertFalse(is_next_to_symbol(schematic, 1, 4))

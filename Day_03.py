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

    def __hash__(self):
        return hash((self.number, self.next_to_symbol))

    def __mul__(self, other):
        if not isinstance(other, PartNumber):
            raise ValueError("other must be a PartNumber.")
        return int(self.number) * int(other.number)


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


def is_digit(c):
    return '0' <= c <= '9'


def extract_part_number_at(row, x):
    assert is_digit(row[x])
    width = len(row)
    start_index = x
    end_index = x
    while start_index > 0 and is_digit(row[start_index - 1]):
        start_index -= 1
    while end_index < width - 1 and is_digit(row[end_index + 1]):
        end_index += 1
    pn = PartNumber(next_to_symbol=True)
    pn.number = row[start_index:end_index + 1]
    return pn


def find_adjacent_part_numbers(schematic, x, y) -> list[PartNumber]:
    part_numbers = set()
    width = len(schematic[0])
    height = len(schematic)
    if x > 0 and y > 0 and is_digit(schematic[y - 1][x - 1]):
        part_numbers.add(extract_part_number_at(schematic[y - 1], x - 1))
    if y > 0 and is_digit(schematic[y - 1][x]):
        part_numbers.add(extract_part_number_at(schematic[y - 1], x))
    if y > 0 and x < width - 1 and is_digit(schematic[y - 1][x + 1]):
        part_numbers.add(extract_part_number_at(schematic[y - 1], x + 1))
    if x < width - 1 and is_digit(schematic[y][x + 1]):
        part_numbers.add(extract_part_number_at(schematic[y], x + 1))
    if y < height - 1 and x < width - 1 and is_digit(schematic[y + 1][x + 1]):
        part_numbers.add(extract_part_number_at(schematic[y + 1], x + 1))
    if y < height - 1 and is_digit(schematic[y + 1][x]):
        part_numbers.add(extract_part_number_at(schematic[y + 1], x))
    if y < height - 1 and x > 0 and is_digit(schematic[y + 1][x - 1]):
        part_numbers.add(extract_part_number_at(schematic[y + 1], x - 1))
    if x > 0 and is_digit(schematic[y][x - 1]):
        part_numbers.add(extract_part_number_at(schematic[y], x - 1))

    return list(part_numbers)


def part_two(filename):
    data = read_puzzle_input(filename)
    schematic = parse_data(data)
    total = 0
    for y, row in enumerate(schematic):
        for x, c in enumerate(row):
            if c == '*':
                part_numbers = find_adjacent_part_numbers(schematic, x, y)
                assert len(part_numbers) < 3
                if len(part_numbers) < 2:
                    continue
                total += part_numbers[0] * part_numbers[1]
    return total


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(539433, part_one('Day_03_input.txt'))
        self.assertEqual(4361, part_one('Day_03_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(75847567, part_two('Day_03_input.txt'))
        self.assertEqual(467835, part_two('Day_03_short_input.txt'))

    def test_is_next_to_symbol(self):
        data = read_puzzle_input('Day_03_short_input.txt')
        schematic = parse_data(data)
        self.assertFalse(is_next_to_symbol(schematic, 1, 0))
        self.assertTrue(is_next_to_symbol(schematic, 2, 0))
        self.assertTrue(is_next_to_symbol(schematic, 2, 4))
        self.assertFalse(is_next_to_symbol(schematic, 1, 4))

    def test_find_adjacent_part_numbers(self):
        data = read_puzzle_input('Day_03_short_input.txt')
        schematic = parse_data(data)
        part_numbers = find_adjacent_part_numbers(schematic, 3, 1)
        self.assertEqual(2, len(part_numbers))
        self.assertEqual(16345, part_numbers[0] * part_numbers[1])

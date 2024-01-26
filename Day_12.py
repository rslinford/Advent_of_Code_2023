import re
import unittest
from dataclasses import dataclass


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


@dataclass
class Record:
    conditions: str
    groups: list[int]


def parse_data(data: str):
    records = []
    for row in data.split('\n'):
        result = re.search(r'^([^ ]+) (.+)', row)
        condition = result.group(1)
        group = [int(a) for a in result.group(2).split(',')]
        records.append(Record(condition, group))
    return records


def count(conditions, groups):
    if not groups:
        return 0 if '#' in conditions else 1
    if not conditions:
        return 1 if not groups else 0

    tally = 0

    if conditions[0] in '.?':
        tally += count(conditions[1:], groups)
    if conditions[0] in '#?':
        if (
                groups[0] <= len(conditions)
                and '.' not in conditions[: groups[0]]
                and (groups[0] == len(conditions) or conditions[groups[0]] != '#')
        ):
            tally += count(conditions[groups[0] + 1:], groups[1:])
    return tally


def part_one(filename):
    data = read_puzzle_input(filename)
    records = parse_data(data)
    tally = 0
    for record in records:
        tally += count(record.conditions, record.groups)
    return tally


def part_two(filename):
    data = read_puzzle_input(filename)
    records = parse_data(data)
    tally = 0
    for record in records:
        conditions = '?'.join([record.conditions] * 5)
        groups = record.groups * 5
        tally += count(conditions, groups)
    return tally


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(7191, part_one('Day_12_input.txt'))
        self.assertEqual(21, part_one('Day_12_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(6512849198636, part_two('Day_12_input.txt'))
        self.assertEqual(525152, part_two('Day_12_short_input.txt'))

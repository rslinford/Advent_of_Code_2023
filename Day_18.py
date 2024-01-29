import re
import unittest
from dataclasses import dataclass


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


@dataclass
class DigPlanEntry:
    direction: str
    distance: int
    color: str


def parse_data(data: str):
    data = data.split('\n')
    dig_plan = []
    for row in data:
        result = re.search(r'^(\w) (\d+) \(#(\w+)\)$', row)
        dig_plan.append(DigPlanEntry(result.group(1), int(result.group(2)), result.group(3)))
    return dig_plan


def follow_dig_plan(dig_plan):
    x, y = (0, 0)
    cubes = {(x, y): 'ffffff'}
    for instruction in dig_plan:
        match instruction.direction:
            case 'U':
                for _ in range(instruction.distance):
                    y -= 1
                    cubes[(x, y)] = instruction.color
            case 'D':
                for _ in range(instruction.distance):
                    y += 1
                    cubes[(x, y)] = instruction.color
            case 'L':
                for _ in range(instruction.distance):
                    x -= 1
                    cubes[(x, y)] = instruction.color
            case 'R':
                for _ in range(instruction.distance):
                    x += 1
                    cubes[(x, y)] = instruction.color
    return cubes


def find_min_max(cubes):
    min_x = min([x for (x, y) in cubes.keys()])
    max_x = max([x for (x, y) in cubes.keys()])
    min_y = min([y for (x, y) in cubes.keys()])
    max_y = max([y for (x, y) in cubes.keys()])
    return min_x, max_x, min_y, max_y


def print_cubes(cubes):
    min_x, max_x, min_y, max_y = find_min_max(cubes)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            in_trench = (x, y) in cubes.keys()
            if in_trench:
                print('#', end='')
            else:
                print('.', end='')
        print()


def dig_out_interior(cubes):
    min_x, max_x, min_y, max_y = find_min_max(cubes)
    for y in range(min_y, max_y + 1):
        prev_in_trench = False
        interior = False
        for x in range(min_x, max_x + 1):
            in_trench = (x, y) in cubes.keys()
            if not in_trench and prev_in_trench:
                interior = not interior
            if interior and not in_trench:
                cubes[(x, y)] = 'ffffff'
            prev_in_trench = in_trench


def part_one(filename):
    data = read_puzzle_input(filename)
    dig_plan = parse_data(data)
    cubes = follow_dig_plan(dig_plan)
    print_cubes(cubes)
    dig_out_interior(cubes)
    print()
    print_cubes(cubes)
    return len(cubes)


def part_two(filename):
    data = read_puzzle_input(filename)
    dig_plan = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # Wrong answer: 78208
        # self.assertEqual(-1, part_one('Day_18_input.txt'))
        self.assertEqual(62, part_one('Day_18_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_18_input.txt'))
        self.assertEqual(-1, part_two('Day_18_short_input.txt'))

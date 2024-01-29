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


DIRECTIONS = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

DIR_ENCODING = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}


def convert_entry(entry):
    distance = int(entry.color[0:5], 16)
    direction = DIR_ENCODING[int(entry.color[5], 16)]
    return DigPlanEntry(direction, distance, 'ffffff')


def find_vertices(dig_plan, part_two=False):
    x, y = (0, 0)
    vertices = [(0, 0)]
    for a in dig_plan:
        if part_two:
            a = convert_entry(a)
        dx, dy = DIRECTIONS[a.direction]
        x += dx * a.distance
        y += dy * a.distance
        vertices.append((x, y))
    return vertices


def find_border_area(dig_plan):
    length = 0
    for a in dig_plan:
        length += a.distance
    return length / 2


def shoelace(vertices):
    a = 0
    b = 0
    for i in range(1, len(vertices)):
        x1, y1 = vertices[i - 1]
        x2, y2 = vertices[i]
        a += x1 * y2
        b += y1 * x2
    return abs(a - b) / 2


def part_one(filename):
    data = read_puzzle_input(filename)
    dig_plan = parse_data(data)
    vertices = find_vertices(dig_plan)
    interior_area = shoelace(vertices)
    border_length = find_border_area(dig_plan) + 1
    return interior_area + border_length


def part_two(filename):
    data = read_puzzle_input(filename)
    dig_plan = parse_data(data)
    vertices = find_vertices(dig_plan, part_two=True)
    interior_area = shoelace(vertices)
    border_length = find_border_area(dig_plan) + 1
    return interior_area + border_length


class Test(unittest.TestCase):
    def test_part_one(self):
        # Wrong answer: 78208
        self.assertEqual(76387, part_one('Day_18_input.txt'))
        self.assertEqual(62, part_one('Day_18_short_input.txt'))
        self.assertEqual(36, part_one('Day_18_short_input2.txt'))

    def test_part_two(self):
        self.assertEqual(250022188522074, part_two('Day_18_input.txt'))
        self.assertEqual(952408144115, part_two('Day_18_short_input.txt'))

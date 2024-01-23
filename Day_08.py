import re
import unittest
from dataclasses import dataclass
from enum import Enum, auto

import numpy as np


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


@dataclass
class Node:
    name: str
    left: str
    right: str


def parse_data(data: str) -> (str, dict[str, Node]):
    data = data.split('\n\n')
    directions = data[0]
    nodes = {}
    for row in data[1].split('\n'):
        result = re.search(r'(\w+) = \((\w+), (\w+)\)', row)
        nodes[result.group(1)] = Node(result.group(1), result.group(2), result.group(3))
    return directions, nodes


def follow_directions(directions, nodes: dict[str, Node]):
    steps_taken = 0
    current_node = nodes['AAA']
    while True:
        direction = directions[steps_taken % len(directions)]
        match direction:
            case 'L':
                current_node = nodes[current_node.left]
            case 'R':
                current_node = nodes[current_node.right]
            case _:
                assert False
        steps_taken += 1
        if current_node.name == 'ZZZ':
            break
    return steps_taken


def part_one(filename):
    data = read_puzzle_input(filename)
    directions, nodes = parse_data(data)
    steps_taken = follow_directions(directions, nodes)
    return steps_taken


def part_two(filename):
    data = read_puzzle_input(filename)
    hands = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(18023, part_one('Day_08_input.txt'))
        self.assertEqual(2, part_one('Day_08_short_input.txt'))
        self.assertEqual(6, part_one('Day_08_short_input_02.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_08_input.txt'))
        self.assertEqual(-1, part_two('Day_08_short_input.txt'))

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


def follow_directions_one(directions, nodes: dict[str, Node]):
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


def all_nodes_ending_in_a(nodes: dict[str, Node]):
    nodes_ending_in_a = []
    for node in nodes.values():
        if node.name[-1] == 'A':
            nodes_ending_in_a.append(node)
    return nodes_ending_in_a


def follow_directions_two(directions, nodes: dict[str, Node]):
    steps_taken = 0
    current_nodes = all_nodes_ending_in_a(nodes)
    while True:
        direction = directions[steps_taken % len(directions)]
        match direction:
            case 'L':
                for i in range(len(current_nodes)):
                    current_nodes[i] = nodes[current_nodes[i].left]
            case 'R':
                for i in range(len(current_nodes)):
                    current_nodes[i] = nodes[current_nodes[i].right]
            case _:
                assert False
        steps_taken += 1
        all_z = True
        for node in current_nodes:
            if node.name[-1] != 'Z':
                all_z = False
                break
        if all_z:
            break
    return steps_taken


def part_one(filename):
    data = read_puzzle_input(filename)
    directions, nodes = parse_data(data)
    steps_taken = follow_directions_one(directions, nodes)
    return steps_taken


def part_two(filename):
    data = read_puzzle_input(filename)
    directions, nodes = parse_data(data)
    steps_taken = follow_directions_two(directions, nodes)
    return steps_taken


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(18023, part_one('Day_08_input.txt'))
        self.assertEqual(2, part_one('Day_08_short_input.txt'))
        self.assertEqual(6, part_one('Day_08_short_input_02.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_08_input.txt'))
        self.assertEqual(6, part_two('Day_08_short_input_03.txt'))

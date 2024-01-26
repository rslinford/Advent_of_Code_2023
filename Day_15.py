import re
import unittest
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    return data.split(',')


def hash_it(s: str):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def part_one(filename):
    data = read_puzzle_input(filename)
    steps = parse_data(data)
    tally = 0
    for step in steps:
        tally += hash_it(step)
    return tally


@dataclass
class Lens:
    label: str
    focal_length: int


@dataclass
class Box:
    lenses: List[Lens] = field(default_factory=list)

    def find(self, label):
        for i in range(len(self.lenses)):
            if self.lenses[i].label == label:
                return i
        return -1

    def remove(self, label):
        i = self.find(label)
        if i >= 0:
            self.lenses.pop(i)

    def store(self, lens: Lens):
        i = self.find(lens.label)
        if i == -1:
            self.lenses.append(lens)
        else:
            self.lenses[i] = lens


def follow_steps(steps):
    boxes = defaultdict(Box)
    for step in steps:
        if '=' in step:
            result = re.search(r'^([^=]+)=(\d+)$', step.strip())
            label = result.group(1)
            focal_length = int(result.group(2))
            lens = Lens(label, focal_length)
            box = boxes[hash_it(label)]
            box.store(lens)
        else:
            assert '-' in step
            result = re.search(r'^([^-]+)-$', step.strip())
            label = result.group(1)
            box = boxes[hash_it(label)]
            box.remove(label)
    return boxes


def calculate_focusing_power(boxes):
    power = 0
    for k, v in boxes.items():
        for i, lens in enumerate(v.lenses):
            power += (k + 1) * (i + 1) * lens.focal_length
    return power


def part_two(filename):
    data = read_puzzle_input(filename)
    steps = parse_data(data)
    boxes = follow_steps(steps)
    power = calculate_focusing_power(boxes)
    return power


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(503154, part_one('Day_15_input.txt'))
        self.assertEqual(1320, part_one('Day_15_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_15_input.txt'))
        self.assertEqual(145, part_two('Day_15_short_input.txt'))

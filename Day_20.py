import unittest
from dataclasses import dataclass
from enum import Enum, auto

"""
Flip-flop modules (prefix %) are either on or off; they are initially off. 
If a flip-flop module receives a high pulse, it is ignored and nothing happens. 
However, if a flip-flop module receives a low pulse, it flips between on and off. 
If it was off, it turns on and sends a high pulse. If it was on, it turns off and 
sends a low pulse.

Conjunction modules (prefix &) remember the type of the most recent pulse received 
from each of their connected input modules; they initially default to remembering a 
low pulse for each input. When a pulse is received, the conjunction module first updates 
its memory for that input. Then, if it remembers high pulses for all inputs, it sends a 
low pulse; otherwise, it sends a high pulse.
"""


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    data = data.split('\n')
    return data


class PulseType(Enum):
    LOW = auto()
    HIGH = auto()


@dataclass
class Pulse:
    source: str
    type: PulseType
    target: str


class ModuleType(Enum):
    FLIP_FLOP = auto()
    CONJUNCTION = auto()
    BROADCASTER = auto()
    BUTTON = auto()


@dataclass
class Module:
    type: ModuleType
    name: str


class Bit:
    OFF = auto()
    ON = auto()


class FlipFlop(Module):
    state: Bit


def part_one(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(-1, part_one('Day_19_input.txt'))
        self.assertEqual(-1, part_one('Day_19_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_19_input.txt'))
        self.assertEqual(-1, part_two('Day_19_short_input.txt'))

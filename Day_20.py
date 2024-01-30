import re
import unittest
from dataclasses import dataclass, field
from enum import Enum, auto


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    modules = {}
    for row in data.split('\n'):
        result = re.search(r'([%&]?\w+) -> (.*)', row)
        name = result.group(1)
        targets = result.group(2)
        targets = [a.strip() for a in targets.split(',')]
        if name == 'broadcaster':
            modules[name] = Broadcaster(name, targets)
            modules['button'] = Button('button', [name])
        elif '%' in name:
            modules[name[1:]] = FlipFlop(name[1:], targets)
        elif '&' in name:
            modules[name[1:]] = Conjunction(name[1:], targets)
        else:
            assert False

    return modules


class PulseType(Enum):
    LOW = auto()
    HIGH = auto()


@dataclass
class Pulse:
    source: str
    type: PulseType
    target: str


# class ModuleType(Enum):
#     FLIP_FLOP = auto()
#     CONJUNCTION = auto()
#     BROADCASTER = auto()
#     BUTTON = auto()


class Module:
    env = {}

    def __init__(self, name, targets):
        self.name = name
        self.targets = targets
        self.env[self.name] = self


class Bit:
    OFF = auto()
    ON = auto()


class FlipFlop(Module):
    state: Bit


class Conjunction(Module):
    pulse_memory: dict = field(default_factory=dict)


class Broadcaster(Module):
    pass


class Button(Module):
    pass


def part_one(filename):
    data = read_puzzle_input(filename)
    modules = parse_data(data)
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    modules = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one('Day_20_input.txt'))
        self.assertEqual(-1, part_one('Day_20_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_20_input.txt'))
        self.assertEqual(-1, part_two('Day_20_short_input.txt'))

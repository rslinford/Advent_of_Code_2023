import re
import unittest
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum, auto


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    for row in data.split('\n'):
        result = re.search(r'([%&]?\w+) -> (.*)', row)
        name = result.group(1)
        targets = result.group(2)
        targets = [a.strip() for a in targets.split(',')]
        if name == 'broadcaster':
            Broadcaster(name, targets)
        elif '%' in name:
            FlipFlop(name[1:], targets)
        elif '&' in name:
            Conjunction(name[1:], targets)
        else:
            assert False
    # Initialize Conjunction memory to all low values for connected inputs.
    for conjunction in Module.env.values():
        if not isinstance(conjunction, Conjunction):
            continue
        for module in Module.env.values():
            if conjunction.name in module.targets:
                conjunction.pulse_memory[module.name] = PulseType.LOW


class PulseType(Enum):
    LOW = auto()
    HIGH = auto()


@dataclass
class Pulse:
    source: str
    type: PulseType


class Module:
    env = {}

    def __init__(self, name, targets):
        self.name = name
        self.targets = targets
        self.env[self.name] = self


class NullModule(Module):
    def __init__(self, name):
        super().__init__(name, [])

    def receive(self, pulse: Pulse):

        def callback():
            print(f'{pulse.source} -{pulse.type}-> {self.name}')
            out_pulse = Pulse(self.name, None)
            for target in self.targets:
                yield self.env[target].receive(out_pulse)

        return callback


class Bit:
    OFF = auto()
    ON = auto()


class FlipFlop(Module):

    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.state = Bit.OFF

    def receive(self, pulse: Pulse):

        def callback():
            print(f'{pulse.source} -{pulse.type}-> {self.name}')
            if pulse.type == PulseType.HIGH:
                return
            if self.state == Bit.ON:
                out_pulse = Pulse(self.name, PulseType.LOW)
            else:
                out_pulse = Pulse(self.name, PulseType.HIGH)
            self.state = Bit.OFF if self.state == Bit.ON else Bit.ON
            for target in self.targets:
                yield self.env[target].receive(out_pulse)

        return callback


class Conjunction(Module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.pulse_memory = defaultdict(lambda: PulseType.LOW)

    def receive(self, pulse: Pulse):

        def callback():
            print(f'{pulse.source} -{pulse.type}-> {self.name}')
            self.pulse_memory[pulse.source] = pulse.type
            if all(a == PulseType.HIGH for a in self.pulse_memory.values()):
                out_pulse = Pulse(self.name, PulseType.LOW)
            else:
                out_pulse = Pulse(self.name, PulseType.HIGH)
            for target in self.targets:
                if target in self.env:
                    yield self.env[target].receive(out_pulse)
                else:
                    yield NullModule(target).receive(out_pulse)

        return callback


class Broadcaster(Module):
    def receive(self, pulse: Pulse):
        def callback():
            print(f'{pulse.source} -{pulse.type}-> {self.name}')
            out_pulse = Pulse(self.name, pulse.type)
            for target in self.targets:
                yield self.env[target].receive(out_pulse)

        return callback


def push_the_button():
    q = deque()
    q.append(Module.env['broadcaster'].receive(Pulse('button', PulseType.LOW)))
    while q:
        cb = q.popleft()
        if cb is not None:
            q.extend(cb())


def part_one(filename):
    data = read_puzzle_input(filename)
    parse_data(data)
    push_the_button()
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one('Day_20_input.txt'))
        # self.assertEqual(-1, part_one('Day_20_short_input.txt'))
        self.assertEqual(-1, part_one('Day_20_short_input2.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_20_input.txt'))
        self.assertEqual(-1, part_two('Day_20_short_input.txt'))

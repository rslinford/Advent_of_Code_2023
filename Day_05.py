import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    return data.strip().split('\n')


def part_one(filename):
    data = read_puzzle_input(filename)
    cards = parse_data(data)
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    cards = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(-1, part_one('Day_05_input.txt'))
        self.assertEqual(-1, part_one('Day_05_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_05_input.txt'))
        self.assertEqual(-1, part_two('Day_05_short_input.txt'))

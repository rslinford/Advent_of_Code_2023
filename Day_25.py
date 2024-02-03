import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    connections = []
    # for row in data.splitlines():
    #     a, b = row.split(': ')
    #     for c in b.split(' '):
    #         connections.append((a, c))
    return connections


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
        self.assertEqual(-1, part_one('Day_25_input.txt'))
        self.assertEqual(-1, part_one('Day_25_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_25_input.txt'))
        self.assertEqual(-1, part_two('Day_24_short_input.txt'))

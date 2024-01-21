import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    return data.split('\n')


def part_one(filename):
    data = read_puzzle_input(filename)
    document = parse_data(data)
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    document = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        result = part_one('Day_01_input.txt')
        self.assertEqual(result, -1)

    def test_part_two(self):
        result = part_two('Day_01_input.txt')
        self.assertEqual(result, -1)

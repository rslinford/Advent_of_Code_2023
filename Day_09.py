import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    return [[int(y) for y in x.split()] for x in data.split('\n')]


def calculate_next_sequence(sequence):
    next_sequence = []
    for i in range(len(sequence) - 1):
        next_sequence.append(sequence[i + 1] - sequence[i])
    return next_sequence


def print_sequences(sequences):
    for i, sequence in enumerate(sequences):
        print(i, sequence)


def extrapolate_value(sequence):
    sequences = [sequence]
    while not all(x == 0 for x in sequences[-1]):
        sequences.append(calculate_next_sequence(sequences[-1]))
    sequences[-1].append(0)
    for i in range(len(sequences) - 1, -1, -1):
        sequences[i - 1].append(sequences[i - 1][-1] + sequences[i][-1])
    return sequences[0][-1]


def extrapolate_value_backwards(sequence):
    sequences = [sequence]
    while not all(x == 0 for x in sequences[-1]):
        sequences.append(calculate_next_sequence(sequences[-1]))
    sequences[-1].insert(0, 0)
    for i in range(len(sequences) - 1, -1, -1):
        sequences[i - 1].insert(0, sequences[i - 1][0] - sequences[i][0])
    return sequences[0][0]


def part_one(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    total = 0
    for row in data:
        extrapolated_value = extrapolate_value(row)
        total += extrapolated_value
    return total


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    total = 0
    for row in data:
        extrapolated_value = extrapolate_value_backwards(row)
        total += extrapolated_value
    return total


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(1882395907, part_one('Day_09_input.txt'))
        self.assertEqual(114, part_one('Day_09_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(1005, part_two('Day_09_input.txt'))
        self.assertEqual(2, part_two('Day_09_short_input.txt'))

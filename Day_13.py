import copy
import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    patterns = []
    for row in data.split('\n\n'):
        patterns.append(row.split('\n'))
    return patterns


def find_horizontal_reflection(pattern, ignore_row=None):
    for i in range(len(pattern) - 1):
        if ignore_row and i == ignore_row - 1:
            continue
        if pattern[i] == pattern[i + 1]:
            spread = 1
            is_reflection = True
            for j in range(i, -1, -1):
                if i + spread >= len(pattern):
                    break
                if pattern[j] != pattern[i + spread]:
                    is_reflection = False
                    break
                spread += 1
            if is_reflection:
                return i + 1
    return 0


def columns_equal(pattern, col1, col2):
    for i in range(len(pattern)):
        if pattern[i][col1] != pattern[i][col2]:
            return False
    return True


def find_vertical_reflection(pattern, ignore_col=None):
    width = len(pattern[0])
    for i in range(width - 1):
        if ignore_col and i == ignore_col - 1:
            continue
        if columns_equal(pattern, i, i + 1):
            spread = 1
            is_reflection = True
            for j in range(i, -1, -1):
                if i + spread >= width:
                    break
                if not columns_equal(pattern, j, i + spread):
                    is_reflection = False
                    break
                spread += 1
            if is_reflection:
                return i + 1
    return 0


def find_reflection(pattern, ignore_col=None, ignore_row=None):
    result = find_horizontal_reflection(pattern, ignore_row) * 100
    if result:
        return result
    result = find_vertical_reflection(pattern, ignore_col)
    # assert result
    return result


def flip_bit_at(pattern, col, row):
    new_pattern = copy.deepcopy(pattern)
    bit = '.' if new_pattern[row][col] == '#' else '#'
    new_pattern[row] = new_pattern[row][:col] + bit + new_pattern[row][col + 1:]
    return new_pattern


def find_reflection_two(pattern):
    vertical_result = 0
    horizontal_result = find_horizontal_reflection(pattern)
    if not horizontal_result:
        vertical_result = find_vertical_reflection(pattern)
        if not vertical_result:
            assert False
    width = len(pattern[0])
    for row in range(len(pattern)):
        for col in range(width):
            candidate = flip_bit_at(pattern, col, row)
            result = find_reflection(candidate, vertical_result, horizontal_result)
            if result:
                return result
    assert False


def part_one(filename):
    data = read_puzzle_input(filename)
    patterns = parse_data(data)
    tally = 0
    for pattern in patterns:
        tally += find_reflection(pattern)
    return tally


def part_two(filename):
    data = read_puzzle_input(filename)
    patterns = parse_data(data)
    tally = 0
    for pattern in patterns:
        tally += find_reflection_two(pattern)
    return tally


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(39939, part_one('Day_13_input.txt'))
        self.assertEqual(405, part_one('Day_13_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_13_input.txt'))
        self.assertEqual(400, part_two('Day_13_short_input.txt'))

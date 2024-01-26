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


def find_horizontal_reflection(pattern):
    for i in range(len(pattern) - 1):
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


def find_vertical_reflection(pattern):
    width = len(pattern[0])
    for i in range(width - 1):
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


def find_reflection(pattern):
    result = find_horizontal_reflection(pattern) * 100
    if result:
        return result
    result = find_vertical_reflection(pattern)
    assert result
    return result


def part_one(filename):
    data = read_puzzle_input(filename)
    patterns = parse_data(data)
    tally = 0
    for pattern in patterns:
        tally += find_reflection(pattern)
    return tally


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(-1, part_one('Day_13_input.txt'))
        self.assertEqual(405, part_one('Day_13_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_13_input.txt'))
        self.assertEqual(-1, part_two('Day_13_short_input.txt'))

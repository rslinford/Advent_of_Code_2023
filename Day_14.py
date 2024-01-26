import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    platform = [list(r) for r in data.split('\n')]
    return platform


def tilt_platform_north(platform):
    width = len(platform[0])
    for outer_row in range(len(platform)):
        for row in range(1, len(platform) - outer_row):
            for col in range(width):
                if platform[row][col] == 'O' and platform[row - 1][col] == '.':
                    platform[row][col] = '.'
                    platform[row - 1][col] = 'O'


def tilt_platform_south(platform):
    width = len(platform[0])
    for outer_row in range(len(platform)):
        for row in range(len(platform) - 2, outer_row - 1, -1):
            for col in range(width):
                if platform[row][col] == 'O' and platform[row + 1][col] == '.':
                    platform[row][col] = '.'
                    platform[row + 1][col] = 'O'


def tilt_platform_west(platform):
    width = len(platform[0])
    for outer_col in range(width):
        for col in range(1, width - outer_col):
            for row in range(len(platform)):
                if platform[row][col] == 'O' and platform[row][col - 1] == '.':
                    platform[row][col] = '.'
                    platform[row][col - 1] = 'O'


def tilt_platform_east(platform):
    width = len(platform[0])
    for outer_col in range(width):
        for col in range(width - 2, outer_col - 1, -1):
            for row in range(len(platform)):
                if platform[row][col] == 'O' and platform[row][col + 1] == '.':
                    platform[row][col] = '.'
                    platform[row][col + 1] = 'O'


def cycle_platform(platform):
    tilt_platform_north(platform)
    tilt_platform_west(platform)
    tilt_platform_south(platform)
    tilt_platform_east(platform)


def weigh_platform(platform):
    width = len(platform[0])
    weight = 0
    for row in range(len(platform)):
        for col in range(width):
            if platform[row][col] == 'O':
                weight += len(platform) - row
    return weight


def part_one(filename):
    data = read_puzzle_input(filename)
    platform = parse_data(data)
    tilt_platform_north(platform)
    weight = weigh_platform(platform)
    return weight


def platform_to_string(platform):
    return '\n'.join([''.join(row) for row in platform])


def part_two(filename):
    data = read_puzzle_input(filename)
    platform = parse_data(data)
    memory = []
    billion = 1_000_000_000
    for i in range(billion):
        cycle_platform(platform)
        snap = platform_to_string(platform)
        try:
            original = memory.index(snap)
            cycle_length = i - original
            offset = (billion - i) % cycle_length
            if offset == 1:
                break
        except ValueError:
            pass
        memory.append(snap)
    weight = weigh_platform(platform)
    return weight


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(107951, part_one('Day_14_input.txt'))
        self.assertEqual(136, part_one('Day_14_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_14_input.txt'))
        self.assertEqual(64, part_two('Day_14_short_input.txt'))

import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    grid = [list(a) for a in data.split('\n')]
    return grid


def find_start(grid):
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == 'S':
                return x, y
    assert False


DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def walk_a_step(grid, locations):
    height = len(grid)
    width = len(grid[0])
    new_locations = set()
    for x, y in locations:
        for dx, dy in DIRS:
            x2 = x + dx
            y2 = y + dy
            if grid[y2 % height][x2 % width] == '.' or grid[y2 % height][x2 % width] == 'S':
                new_locations.add((x2, y2))
    return new_locations


def print_grid(grid, locations):
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if (x, y) in locations:
                print('O', end='')
            else:
                print(col, end='')
        print()


def part_one(filename, steps):
    data = read_puzzle_input(filename)
    grid = parse_data(data)
    locations = {find_start(grid)}
    for n in range(steps):
        locations = walk_a_step(grid, locations)
        print(f'After {n + 1} steps')
        print_grid(grid, locations)
        print()
    return len(locations)


def part_two(filename, steps):
    data = read_puzzle_input(filename)
    grid = parse_data(data)
    locations = {find_start(grid)}
    for n in range(steps):
        locations = walk_a_step(grid, locations)
    return len(locations)


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(3600, part_one('Day_21_input.txt', 64))
        self.assertEqual(16, part_one('Day_21_short_input.txt', 6))

    def test_part_two(self):
        # self.assertEqual(-1, part_two('Day_21_input.txt'), 26501365)
        self.assertEqual(50, part_two('Day_21_short_input.txt', 10))
        self.assertEqual(167004, part_two('Day_21_short_input.txt', 500))

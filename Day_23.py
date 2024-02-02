import sys
import unittest


sys.setrecursionlimit(10000)


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    grid = [list(a) for a in data.split('\n')]
    grid_map = {}
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            grid_map[(x, y)] = c
    start, end = find_start_and_end(grid)
    return grid_map, start, end


def find_start_and_end(grid):
    height = len(grid)
    start = grid[0].index('.'), 0
    end = grid[height - 1].index('.'), height - 1
    return start, end


DIRS = [(0, -1), (0, 1), (1, 0), (-1, 0)]
OPPOSITE_DIR = {'v': (0, -1), '^': (0, 1), '<': (1, 0), '>': (-1, 0)}


def add_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return x1 + x2, y1 + y2


def take_a_step(current_pos, end, grid_map, history, step_count, is_wet):
    if current_pos == end:
        return step_count
    longest_step_count = -1
    for d in DIRS:
        next_pos = add_points(current_pos, d)
        if next_pos not in grid_map:
            continue  # out of bounds
        if grid_map[next_pos] == '#':
            continue  # forest
        if is_wet and grid_map[next_pos] in '^v><' and OPPOSITE_DIR[grid_map[next_pos]] == d:
            continue  # can't go against the
        if next_pos in history:
            continue
        new_history = set(history)
        new_history.add(next_pos)
        new_step_count = take_a_step(next_pos, end, grid_map, new_history, step_count + 1, is_wet)
        longest_step_count = max(longest_step_count, new_step_count)
    return longest_step_count


def take_a_hike(grid_map, start, end, is_wet):
    history = {start}
    return take_a_step(start, end, grid_map, history, 0, is_wet)


def part_one(filename):
    data = read_puzzle_input(filename)
    grid_map, start, end = parse_data(data)
    result = take_a_hike(grid_map, start, end, True)
    return result


def part_two(filename):
    data = read_puzzle_input(filename)
    grid_map, start, end = parse_data(data)
    result = take_a_hike(grid_map, start, end, False)
    return result


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(2278, part_one('Day_23_input.txt'))
        self.assertEqual(94, part_one('Day_23_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(6734, part_two('Day_23_input.txt'))
        # self.assertEqual(154, part_two('Day_23_short_input.txt'))

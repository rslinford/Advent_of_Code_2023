import unittest
from dataclasses import dataclass
from enum import Enum, auto
from heapq import heappush, heappop

from colorama import Fore


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    return [[int(b) for b in list(a)] for a in data.split('\n')]


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def __getitem__(self, key):
        if len(key) != 2:
            raise ValueError(f'Expected a length of 2. Received length {len(key)} instead.')
        x, y = key
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.grid[y][x]

    def print_visited(self, visited):
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if VisitedKey(x, y) in visited:
                    print(Fore.RED + str(c), end='')
                else:
                    print(Fore.LIGHTWHITE_EX + str(c), end='')
            print()


class Heading(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class QueueItem:
    heat_loss: int
    x: int
    y: int
    heading: Heading
    heading_step: int

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.heat_loss < other.heat_loss


@dataclass
class VisitedKey:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


def opposites(heading1, heading2):
    if (heading1, heading2) in [(Heading.UP, Heading.DOWN), (Heading.DOWN, Heading.UP)]:
        return True
    if (heading1, heading2) in [(Heading.LEFT, Heading.RIGHT), (Heading.RIGHT, Heading.LEFT)]:
        return True
    return False


def search(grid):
    headings = {Heading.UP: (0, -1), Heading.DOWN: (0, 1), Heading.LEFT: (-1, 0), Heading.RIGHT: (1, 0)}
    queue = []
    heappush(queue, QueueItem(0, 0, 0, Heading.RIGHT, 0))
    visited = {VisitedKey(0, 0): 0}
    while queue:
        qi: QueueItem = heappop(queue)
        for heading, (dx, dy) in headings.items():
            local_heat_loss = grid[(qi.x + dx, qi.y + dy)]
            if not local_heat_loss:
                continue
            if (qi.heading == heading and qi.heading_step == 3) or opposites(qi.heading, heading):
                continue
            visited_key = VisitedKey(qi.x + dx, qi.y + dy)
            if visited_key in visited:
                current_heat_loss = visited[visited_key]
            else:
                current_heat_loss = float('inf')
            if qi.heat_loss + local_heat_loss < current_heat_loss:
                if qi.heading == heading:
                    new_heading_step = qi.heading_step + 1
                else:
                    new_heading_step = 1
                visited[visited_key] = qi.heat_loss + local_heat_loss
                heappush(queue,
                         QueueItem(qi.heat_loss + local_heat_loss, qi.x + dx, qi.y + dy, heading, new_heading_step))
                grid.print_visited(visited)
                print()

    ends = [heat_loss for vi, heat_loss in visited.items() if (vi.x, vi.y) == (grid.width - 1, grid.height - 1)]
    return min(ends)


def part_one(filename):
    data = read_puzzle_input(filename)
    grid = Grid(parse_data(data))
    return search(grid)


def part_two(filename):
    data = read_puzzle_input(filename)
    grid = Grid(parse_data(data))
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(851, part_one('Day_17_input.txt'))
        self.assertEqual(102, part_one('Day_17_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(982, part_two('Day_17_input.txt'))
        self.assertEqual(-1, part_two('Day_17_short_input.txt'))

    def test_grid(self):
        data = read_puzzle_input('Day_17_short_input.txt')
        data = parse_data(data)
        g = Grid(data)
        self.assertEqual(2, g[(0, 0)])
        self.assertEqual(3, g[(12, 12)])
        self.assertEqual(5, g[(2, 2)])
        self.assertIsNone(g[(12, 13)])
        self.assertIsNone(g[(13, 12)])
        self.assertIsNone(g[(-1, 4)])
        self.assertIsNone(g[(5, -1)])

    def test_queue(self):
        queue = []
        heappush(queue, QueueItem(4, 1, 1))
        heappush(queue, QueueItem(1, 2, 3))
        heappush(queue, QueueItem(6, 5, 4))
        qi: QueueItem = heappop(queue)
        self.assertEqual(1, qi.heat_loss)
        self.assertEqual(2, qi.x)
        self.assertEqual(3, qi.y)

import unittest
from dataclasses import dataclass
from enum import Enum, auto


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    return [list(row) for row in data.split('\n')]


def contraption_to_string(contraption):
    s = [''.join(a) for a in contraption]
    return '\n'.join(s)


def light_map_to_string(light_map):
    s = []
    for row in light_map:
        str_row = ''.join([str(a) for a in row])
        s.append(str_row)
    return '\n'.join(s)


class Heading(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Cursor:
    x: int
    y: int
    heading: Heading


def light_up_contraption(contraption):
    width, height = len(contraption[0]), len(contraption)
    light_map = [[0] * width for _ in range(height)]
    cursors = [Cursor(0, 0, Heading.RIGHT)]
    while cursors:
        for cursor in cursors:
            light_map[cursor.y][cursor.x] += 1
            match contraption[cursor.y][cursor.x]:
                case '.':
                    match cursor.heading:
                        case Heading.UP:
                            if cursor.y > 0:
                                cursor.y -= 1
                            else:
                                cursors.remove(cursor)
                        case Heading.DOWN:
                            if cursor.y < height - 1:
                                cursor.y += 1
                            else:
                                cursors.remove(cursor)
                        case Heading.LEFT:
                            if cursor.x > 0:
                                cursor.x -= 1
                            else:
                                cursors.remove(cursor)
                        case Heading.RIGHT:
                            if cursor.x < width - 1:
                                cursor.x += 1
                            else:
                                cursors.remove(cursor)
                case '|':
                    pass
                case '-':
                    pass
                case '/':
                    match cursor.heading:
                        case Heading.UP:
                            if cursor.x < width - 1:
                                cursor.x += 1
                                cursor.heading = Heading.RIGHT
                            else:
                                cursors.remove(cursor)
                        case Heading.DOWN:
                            if cursor.x > 0:
                                cursor.x -= 1
                                cursor.heading = Heading.LEFT
                            else:
                                cursors.remove(cursor)
                        case Heading.LEFT:
                            if cursor.y < height - 1:
                                cursor.y += 1
                                cursor.heading = Heading.DOWN
                            else:
                                cursors.remove(cursor)
                        case Heading.RIGHT:
                            if cursor.y < height - 1:
                                cursor.y += 1
                                cursor.heading = Heading.UP
                            else:
                                cursors.remove(cursor)
                case '\\':
                    match cursor.heading:
                        case Heading.UP:
                            if cursor.x > 0:
                                cursor.x -= 1
                                cursor.heading = Heading.LEFT
                            else:
                                cursors.remove(cursor)
                        case Heading.DOWN:
                            if cursor.x < width - 1:
                                cursor.x += 1
                                cursor.heading = Heading.RIGHT
                            else:
                                cursors.remove(cursor)
                        case Heading.LEFT:
                            if cursor.y > 0:
                                cursor.y -= 1
                                cursor.heading = Heading.UP
                            else:
                                cursors.remove(cursor)
                        case Heading.RIGHT:
                            if cursor.y < height - 1:
                                cursor.y += 1
                                cursor.heading = Heading.DOWN
                            else:
                                cursors.remove(cursor)
                case _:
                    assert False
            match cursor.heading:
                case Heading.UP:
                    if cursor.y == 0:
                        cursors.remove(cursor)
                    else:
                        cursor.y -= 1
                case Heading.DOWN:
                    if cursor.y == height - 1:
                        cursors.remove(cursor)
                    else:
                        cursor.y += 1
                case Heading.LEFT:
                    if cursor.x == 0:
                        cursors.remove(cursor)
                    else:
                        cursor.x -= 1
                case Heading.RIGHT:
                    if cursor.x == width - 1:
                        cursors.remove(cursor)
                    else:
                        cursor.y += 1

    print(light_map_to_string(light_map))

    return light_map



def part_one(filename):
    data = read_puzzle_input(filename)
    contraption = parse_data(data)
    light_up_contraption(contraption)
    print(contraption_to_string(contraption))
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one('Day_16_input.txt'))
        self.assertEqual(-1, part_one('Day_16_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_16_input.txt'))
        self.assertEqual(-1, part_two('Day_16_short_input.txt'))

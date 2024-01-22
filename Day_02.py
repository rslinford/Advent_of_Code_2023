import re
import unittest
from dataclasses import dataclass


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


@dataclass
class Draw:
    red: int = 0
    green: int = 0
    blue: int = 0

    @property
    def power(self):
        return self.red * self.green * self.blue


@dataclass
class Game:
    id: int
    draws: list[Draw]


def parse_data(data: str) -> list[Game]:
    games = []
    data = data.split('\n')
    for row in data:
        row = row.split(':')
        result = re.search(r'(\d+)', row[0])
        game = Game(int(result.group(1)), [])
        games.append(game)
        for draw_text in row[1].split(';'):
            draw = Draw()
            game.draws.append(draw)
            for color_text in draw_text.split(','):
                result = re.search(r'(\d+) (\w+)', color_text)
                count = int(result.group(1))
                color = result.group(2)
                match color:
                    case 'red':
                        draw.red += count
                    case 'green':
                        draw.green += count
                    case 'blue':
                        draw.blue += count
                    case _:
                        assert False

    return games


def game_passes(game, max_draw):
    for draw in game.draws:
        if draw.red > max_draw.red:
            return False
        if draw.green > max_draw.green:
            return False
        if draw.blue > max_draw.blue:
            return False
    return True


def part_one(filename):
    data = read_puzzle_input(filename)
    games = parse_data(data)
    max_draw = Draw(red=12, green=13, blue=14)
    sum_of_ids = 0
    for game in games:
        if game_passes(game, max_draw):
            sum_of_ids += game.id
    return sum_of_ids


def find_minimal_set(game) -> Draw:
    minimal_set = Draw()
    for draw in game.draws:
        if draw.red > minimal_set.red:
            minimal_set.red = draw.red
        if draw.green > minimal_set.green:
            minimal_set.green = draw.green
        if draw.blue > minimal_set.blue:
            minimal_set.blue = draw.blue
    return minimal_set


def part_two(filename):
    data = read_puzzle_input(filename)
    games = parse_data(data)
    total = 0
    for game in games:
        minimal_set = find_minimal_set(game)
        total += minimal_set.power
    return total


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(2278, part_one('Day_02_input.txt'))
        self.assertEqual(8, part_one('Day_02_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(67953, part_two('Day_02_input.txt'))
        self.assertEqual(2286, part_two('Day_02_short_input.txt'))

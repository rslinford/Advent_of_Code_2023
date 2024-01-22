import re
import unittest
from dataclasses import dataclass, field


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


@dataclass
class Card:
    id: int
    winning_numbers: list[int] = field(default_factory=list)
    numbers_owned: list[int] = field(default_factory=list)


def parse_data(data: str) -> list[Card]:
    cards = []
    for row in data.split('\n'):
        result = re.search(r'^Card +(\d+):([^|]+)\|(.+)', row)
        card = Card(int(result.group(1)))
        cards.append(card)
        winning = result.group(2)
        owned = result.group(3)
        for n in winning.strip().split(' '):
            if len(n.strip()) == 0:
                continue
            card.winning_numbers.append(int(n))
        for n in owned.strip().split(' '):
            if len(n.strip()) == 0:
                continue
            card.numbers_owned.append(int(n))

    return cards


def score_card(card):
    count = 0
    for n in card.winning_numbers:
        if n in card.numbers_owned:
            count += 1
    return 2 ** (count - 1) if count > 0 else 0


def part_one(filename):
    data = read_puzzle_input(filename)
    cards = parse_data(data)
    total = 0
    for card in cards:
        total += score_card(card)
    return total


def part_two(filename):
    data = read_puzzle_input(filename)
    cards = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(18519, part_one('Day_04_input.txt'))
        self.assertEqual(13, part_one('Day_04_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_04_input.txt'))
        self.assertEqual(-1, part_two('Day_04_short_input.txt'))

    def test_parse_data(self):
        data = read_puzzle_input('Day_04_short_input.txt')
        cards = parse_data(data)
        self.assertEqual(6, len(cards))
        self.assertEqual(1, cards[0].id)
        self.assertEqual(41, cards[0].winning_numbers[0])
        self.assertEqual(17, cards[0].winning_numbers[4])
        self.assertEqual(83, cards[0].numbers_owned[0])
        self.assertEqual(53, cards[0].numbers_owned[7])
        self.assertEqual(31, cards[5].winning_numbers[0])
        self.assertEqual(72, cards[5].winning_numbers[4])
        self.assertEqual(74, cards[5].numbers_owned[0])
        self.assertEqual(11, cards[5].numbers_owned[7])

    def test_score_card(self):
        data = read_puzzle_input('Day_04_short_input.txt')
        cards = parse_data(data)
        self.assertEqual(8, score_card(cards[0]))
        self.assertEqual(2, score_card(cards[1]))
        self.assertEqual(2, score_card(cards[2]))
        self.assertEqual(1, score_card(cards[3]))
        self.assertEqual(0, score_card(cards[4]))
        self.assertEqual(0, score_card(cards[5]))

import re
import unittest
from dataclasses import dataclass
from enum import Enum, auto

import numpy as np

CARD_ORDER = {'A': 12, 'K': 11, 'Q': 10, 'J': 9, 'T': 8, '9': 7, '8': 6, '7': 5, '6': 4, '5': 3, '4': 2, '3': 1, '2': 0}


class HandType(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()

    def __lt__(self, other):
        if other is None:
            return False
        if isinstance(other, HandType):
            return self.value < other.value
        return NotImplemented


@dataclass
class Hand:
    cards: str
    bid: int
    type: HandType = None

    def __lt__(self, other):
        if other is None:
            return False
        if isinstance(other, Hand):
            if self.type != other.type:
                return self.type < other.type
            for i in range(len(self.cards)):
                n = compare_cards(self.cards[i], other.cards[i])
                if n == 0:
                    continue
                elif n == -1:
                    return True
                else:
                    return False
            return False

        return NotImplemented

    def __post_init__(self):
        self.categorize_hand()

    def categorize_hand(self):
        counts = count_cards(self)
        max_count = max(counts)
        if max_count == 5:
            self.type = HandType.FIVE_OF_A_KIND
            return
        if max_count == 4:
            self.type = HandType.FOUR_OF_A_KIND
            return
        if max_count == 1:
            self.type = HandType.HIGH_CARD
            return
        number_of_pairs = 0
        for count in counts:
            if count == 2:
                number_of_pairs += 1
        if number_of_pairs == 2:
            self.type = HandType.TWO_PAIR
            return
        if max_count == 3 and number_of_pairs == 1:
            self.type = HandType.FULL_HOUSE
            return
        if max_count == 3 and number_of_pairs == 0:
            self.type = HandType.THREE_OF_A_KIND
            return
        if number_of_pairs == 1:
            self.type = HandType.ONE_PAIR
            return
        assert False


def compare_cards(card1, card2):
    value1 = CARD_ORDER[card1]
    value2 = CARD_ORDER[card2]
    if value1 > value2:
        return 1
    elif value1 == value2:
        return 0
    else:
        return -1


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str) -> list[Hand]:
    data = data.split('\n')
    hands = []
    for row in data:
        result = re.search(r'(\w+) (\d+)', row)
        cards = result.group(1)
        bid = result.group(2)
        hands.append(Hand(cards, int(bid)))

    return hands


def count_cards(hand):
    counts = np.zeros(len(CARD_ORDER), dtype=int)
    for card in hand.cards:
        counts[CARD_ORDER[card]] += 1
    return counts


def part_one(filename):
    data = read_puzzle_input(filename)
    hands = parse_data(data)
    hands.sort()
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    hands = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one('Day_07_input.txt'))
        self.assertEqual(-1, part_one('Day_07_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_07_input.txt'))
        self.assertEqual(-1, part_two('Day_07_short_input.txt'))

    def test_compare_cards(self):
        self.assertEqual(1, compare_cards('A', 'K'))
        self.assertEqual(0, compare_cards('A', 'A'))
        self.assertEqual(-1, compare_cards('K', 'A'))

    def test_categorize_hands(self):
        data = read_puzzle_input('Day_07_short_input.txt')
        hands = parse_data(data)
        self.assertEqual(HandType.ONE_PAIR, hands[0].type)
        self.assertEqual(HandType.THREE_OF_A_KIND, hands[1].type)
        self.assertEqual(HandType.TWO_PAIR, hands[2].type)
        hand = Hand('TTTTT', 123)
        self.assertEqual(HandType.FIVE_OF_A_KIND, hand.type)
        hand = Hand('T2222', 123)
        self.assertEqual(HandType.FOUR_OF_A_KIND, hand.type)
        hand = Hand('55599', 123)
        self.assertEqual(HandType.FULL_HOUSE, hand.type)
        hand = Hand('89TJQ', 123)
        self.assertEqual(HandType.HIGH_CARD, hand.type)

    def test_less_than(self):
        h1 = Hand('TTTTT', 123)
        h2 = Hand('77777', 123)
        self.assertTrue(h1 > h2)
        h1 = Hand('23456', 123)
        h2 = Hand('23457', 123)
        self.assertTrue(h1 < h2)
        h1 = Hand('44552', 123)
        h2 = Hand('99234', 123)
        self.assertTrue(h1 > h2)
        h1 = Hand('98765', 123)
        h2 = Hand('98765', 123)
        self.assertTrue(h1 == h2)

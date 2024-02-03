import unittest

import networkx as nx
from matplotlib import pyplot as plt


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    connections = []
    for row in data.splitlines():
        a, b = row.split(': ')
        for c in b.split(' '):
            connections.append((a, c))
    return connections


"""
Cuts to the following edges:
tmb, gpj
mtc, rhh
xtx, njn
"""


def part_one(filename):
    data = read_puzzle_input(filename)
    connections = parse_data(data)
    g = nx.Graph()
    for con in connections:
        g.add_edge(con[0], con[1])
    # nx.draw(g, with_labels=True)
    # plt.show()
    cv, p = nx.stoer_wagner(g)
    result = len(p[0]) * len(p[1])
    return result


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(-1, part_one('Day_25_input.txt'))
        self.assertEqual(54, part_one('Day_25_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_25_input.txt'))
        self.assertEqual(-1, part_two('Day_24_short_input.txt'))

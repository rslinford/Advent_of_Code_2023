import random
import unittest
from collections import defaultdict, deque


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
    connections = defaultdict(set)
    for row in data.splitlines():
        a, b = row.split(': ')
        for c in b.split(' '):
            connections[a].add(c)
            connections[c].add(a)
    return connections


"""
Cuts to the following edges:
tmb, gpj
mtc, rhh
xtx, njn
"""


def part_one(filename):
    data = read_puzzle_input(filename)
    graph = parse_data(data)
    inbetween_count = defaultdict(int)
    for node in graph:
        q = deque([(node, [])])
        visited = {node}
        while q:
            current_node, path = q.popleft()
            for edge in path:
                inbetween_count[edge] += 1
            for nxt in graph[current_node]:
                if nxt not in visited:
                    visited.add(nxt)
                    edge = tuple(sorted([current_node, nxt]))
                    q.append((nxt, path + [edge]))
    busy_edges = sorted(inbetween_count, key=inbetween_count.get)[-3:]
    for node1, node2 in busy_edges:
        graph[node1].remove(node2)
        graph[node2].remove(node1)

    node = random.choice(list(graph.keys()))
    q = deque([node])
    visited = set()
    while q:
        node = q.popleft()
        if node not in visited:
            visited.add(node)
            for nxt in graph[node]:
                q.append(nxt)
    result = len(visited) * (len(graph) - len(visited))
    return result


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(558376, part_one('Day_25_input.txt'))
        self.assertEqual(54, part_one('Day_25_short_input.txt'))

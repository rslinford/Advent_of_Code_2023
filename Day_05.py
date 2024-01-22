import math
import unittest
from dataclasses import dataclass, field


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


@dataclass
class Range:
    destination_range_start: int
    source_range_start: int
    range_length: int


@dataclass
class AlmanacMap:
    name: str
    ranges: list[Range] = field(default_factory=list)


def parse_data(data: str) -> (list[int], list[AlmanacMap]):
    data = data.strip().split('\n\n')
    seeds = [int(x) for x in data[0].split(' ') if x.isnumeric()]
    almanac_maps = []
    for map_text in data[1:]:
        map_text = map_text.split('\n')
        map_name = map_text[0].split(' ')[0]
        almanac_map = AlmanacMap(map_name)
        almanac_maps.append(almanac_map)
        for row in map_text[1:]:
            row = row.split(' ')
            almanac_map.ranges.append(Range(int(row[0]), int(row[1]), int(row[2])))

    return seeds, almanac_maps


def follow_map(n, almanac_map: AlmanacMap):
    for r in almanac_map.ranges:
        if r.source_range_start <= n < r.source_range_start + r.range_length:
            return r.destination_range_start + (n - r.source_range_start)
    return n


def follow_maps(seed, almanac_maps) -> int:
    n = seed
    for almanac_map in almanac_maps:
        n = follow_map(n, almanac_map)
    return n


def part_one(filename):
    data = read_puzzle_input(filename)
    seeds, almanac_maps = parse_data(data)
    lowest_location = math.inf
    for seed in seeds:
        location = follow_maps(seed, almanac_maps)
        if location < lowest_location:
            lowest_location = location
    return lowest_location


@dataclass
class SeedRange:
    start_seed: int
    range_length: int


def make_seed_ranges(seeds) -> list[SeedRange]:
    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append(SeedRange(seeds[i], seeds[i + 1]))
    return seed_ranges


def part_two(filename):
    data = read_puzzle_input(filename)
    seeds, almanac_maps = parse_data(data)
    lowest_location = math.inf
    seed_ranges = make_seed_ranges(seeds)
    for seed_range in seed_ranges:
        print(f'Working on {seed_range}')
        for seed in range(seed_range.start_seed, seed_range.start_seed + seed_range.range_length):
            location = follow_maps(seed, almanac_maps)
            if location < lowest_location:
                lowest_location = location

    return lowest_location


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(175622908, part_one('Day_05_input.txt'))
        self.assertEqual(35, part_one('Day_05_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_05_input.txt'))
        self.assertEqual(46, part_two('Day_05_short_input.txt'))

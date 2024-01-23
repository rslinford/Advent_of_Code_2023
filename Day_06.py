import unittest
from dataclasses import dataclass


@dataclass
class Race:
    time: int
    distance: int


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str) -> list[Race]:
    data = data.strip().split('\n')
    times = [int(x) for x in data[0].split(' ') if x.isnumeric()]
    distances = [int(x) for x in data[1].split(' ') if x.isnumeric()]
    races = []
    for i in range(len(times)):
        races.append(Race(times[i], distances[i]))
    return races


def count_ways_to_beat_the_record(race):
    tally = 0
    print(race)
    for hold_button_down in range(race.time + 1):
        remaining_time = race.time - hold_button_down
        distance_traveled = remaining_time * hold_button_down
        if distance_traveled > race.distance:
            tally += 1

    return tally


def part_one(filename):
    data = read_puzzle_input(filename)
    races = parse_data(data)
    tally = 1
    for race in races:
        n = count_ways_to_beat_the_record(race)
        tally *= n
    return tally


def consolidate_races(races):
    time = ''
    distance = ''
    for race in races:
        time += str(race.time)
        distance += str(race.distance)
    race = Race(int(time), int(distance))
    return race


def part_two(filename):
    data = read_puzzle_input(filename)
    races = parse_data(data)
    race = consolidate_races(races)
    count = count_ways_to_beat_the_record(race)
    return count


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(608902, part_one('Day_06_input.txt'))
        self.assertEqual(288, part_one('Day_06_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_06_input.txt'))
        self.assertEqual(71503, part_two('Day_06_short_input.txt'))

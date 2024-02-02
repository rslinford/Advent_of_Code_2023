#!/usr/bin/env python3
# 2023 Day 23: A Long Walk

import sys

sys.setrecursionlimit(10000)


def process_input(filename):
    """Acquire input data"""
    with open(filename) as file:
        input = file.read().splitlines()

    map = {}
    start = (1, 0)
    end = (len(input[0]) - 2, len(input) - 1)

    for y, line in enumerate(input):
        for x, ch in enumerate(line):
            map[x, y] = ch

    return map, start, end


def take_a_hike():
    path = set()
    path.add(start)
    longest_walk = take_a_step(start, path, 0)
    return longest_walk


def take_a_step(cur_pos, path, steps):
    if cur_pos == end:
        print(steps)
        return steps
    longest_steps = -1
    for d, dir in enumerate('v>^<'):
        move_to = adjust_pos(cur_pos, dir)
        tile = map.get(move_to, '#')
        if tile == '#':
            continue  # can't step in forest
        if move_to in path:
            continue  # can't step on same tile twice
        if tile == '^<v>'[d]:
            continue  # can't move upslope
        new_path = set(path)
        new_path.add(move_to)
        new_steps = take_a_step(move_to, new_path, steps + 1)
        longest_steps = max(longest_steps, new_steps)
    return longest_steps


def adjust_pos(coord, dir):
    x, y = coord
    adjust = {'>': (1, 0), '<': (-1, 0), 'v': (0, 1), '^': (0, -1)}
    ax, ay = adjust[dir]
    x += ax
    y += ay
    return (x, y)


# -----------------------------------------------------------------------------------------

filename = 'input.txt'
# filename = 'sample.txt'

map, start, end = process_input(filename)
cache = {}

longest_walk = take_a_hike()

print()
print('Longest walk:', longest_walk)

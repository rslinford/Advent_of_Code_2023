NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)


def reverse_dir(dir: tuple[int, int]):
    return dir[0] * -1, dir[1] * -1


Point = tuple[int, int]
Grid = list[list[str]]


def padd(a: Point, b: Point) -> Point:
    return a[0] + b[0], a[1] + b[1]


def gget(g: Grid, p: Point) -> str:
    x, y = p[0], p[1]
    if (x < 0) or (x >= len(g[0])) or (y < 0) or (y >= len(g)):
        return '.'
    return g[y][x]


def connections(tile: str):
    if tile == '-':
        return EAST, WEST
    if tile == '|':
        return NORTH, SOUTH
    if tile == 'F':
        return EAST, SOUTH
    if tile == 'L':
        return NORTH, EAST
    if tile == 'J':
        return NORTH, WEST
    if tile == '7':
        return SOUTH, WEST
    print("unhandled tile encountered: ", tile)
    assert False  # uh-oh, something wrong!


def solve(start: Point, grid: Grid):
    visited = [start]
    next_dirs = {NORTH, SOUTH, EAST, WEST}
    while True:
        for d in next_dirs:
            n = padd(visited[-1], d)
            # see if it's a valid tile we can travel to
            tile = gget(grid, n)
            if tile == '.':
                continue
            if tile == 'S':
                return visited
            if reverse_dir(d) in connections(tile):
                # yes, we can travel here
                next_dirs = set(connections(tile))
                next_dirs.remove(reverse_dir(d))
                visited.append(n)
                break


def part1(start: Point, grid: Grid):
    path = solve(start, grid)
    print(f"Part 1: {len(path) / 2}")


if __name__ == '__main__':
    with open('Day_10_short_input_03.txt') as f:
        data = f.read()
    print(data)
    grid = [list(line) for line in data.splitlines()]
    start = None
    for (y, row) in enumerate(grid):
        if 'S' in row:
            start = (row.index('S'), y)
            break
    part1(start, grid)

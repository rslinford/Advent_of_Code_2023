with open("Day_11_input.txt", "r") as file:
    input = file.read().splitlines()


def find_galaxies_and_empty_spaces(input):
    galaxies = []
    for row, line in enumerate(input):
        for col, c in enumerate(line):
            if c == "#":
                galaxies.append((row, col))

    all_rows = set([g[0] for g in galaxies])
    all_cols = set([g[1] for g in galaxies])
    empty_rows = sorted(set(range(row)).difference(all_rows))
    empty_cols = sorted(set(range(col)).difference(all_cols))

    return galaxies, empty_rows, empty_cols


solution1 = 0
solution2 = 0
expand_2 = 1000000 - 1
galaxies, empty_rows, empty_cols = find_galaxies_and_empty_spaces(input)

for i, galaxy in enumerate(galaxies):
    for j in range(i + 1, len(galaxies)):
        galaxy2 = galaxies[j]
        empty_rows_passed = len(
            [
                r
                for r in empty_rows
                if (galaxy2[0] < r < galaxy[0]) or (galaxy[0] < r < galaxy2[0])
            ]
        )
        empty_cols_passed = len(
            [
                c
                for c in empty_cols
                if (galaxy2[1] < c < galaxy[1]) or (galaxy[1] < c < galaxy2[1])
            ]
        )

        solution1 += (
                abs(galaxy[0] - galaxy2[0])
                + abs(galaxy[1] - galaxy2[1])
                + empty_rows_passed
                + empty_cols_passed
        )
        solution2 += (
                abs(galaxy[0] - galaxy2[0])
                + abs(galaxy[1] - galaxy2[1])
                + (empty_rows_passed + empty_cols_passed) * expand_2
        )

print("Solution 1: ", solution1)
print("Solution 2: ", solution2)

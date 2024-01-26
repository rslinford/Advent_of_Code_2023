from functools import cache

with open("Day_12_short_input.txt", "r") as file:
    input = file.read().splitlines()


@cache
def count_arrangements(conditions, rules):
    if not rules:
        return 0 if "#" in conditions else 1
    if not conditions:
        return 1 if not rules else 0

    result = 0

    if conditions[0] in ".?":
        result += count_arrangements(conditions[1:], rules)
    if conditions[0] in "#?":
        if (
                rules[0] <= len(conditions)
                and "." not in conditions[: rules[0]]
                and (rules[0] == len(conditions) or conditions[rules[0]] != "#")
        ):
            result += count_arrangements(conditions[rules[0] + 1:], rules[1:])

    return result


solution1 = 0
solution2 = 0
for line in input:
    conditions, rules = line.split()
    rules = eval(rules)
    solution1 += count_arrangements(conditions, rules)

    conditions = "?".join([conditions] * 5)
    rules = rules * 5
    solution2 += count_arrangements(conditions, rules)

print("Solution 1:", solution1)
print("Solution 2:", solution2)

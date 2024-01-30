import re
import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_workflows(data):
    workflows = {}
    for row in data.split('\n'):
        result = re.search(r'^(\w+)\{(.*)\}$', row)
        name = result.group(1)
        rules = result.group(2)
        workflows[name] = rules.split(',')
    return workflows


def parse_specs(data):
    spec_list = []
    for row in data.split('\n'):
        result = re.search(r'\{(.*)\}', row)
        row = result.group(1)
        spec = {}
        spec_list.append(spec)
        for e in row.split(','):
            result = re.search(r'(\w)=(\d+)', e)
            spec[result.group(1)] = int(result.group(2))

    return spec_list


def parse_data(data: str):
    data = data.split('\n\n')
    workflows = parse_workflows(data[0])
    specs = parse_specs(data[1])
    return workflows, specs


def follow_workflows(workflows, specs):
    accepted_specs = []
    for spec in specs:
        wf = workflows['in']
        while wf:
            for rule in wf:
                if ':' in rule:
                    result = re.search(r'(\w)(.)(\d+):(\w+)', rule)
                    v = result.group(1)
                    op = result.group(2)
                    n = int(result.group(3))
                    w = result.group(4)
                    if op == '<' and spec[v] < n:
                        if w == 'A':
                            accepted_specs.append(spec)
                            wf = None
                        elif w == 'R':
                            wf = None
                        else:
                            wf = workflows[w]
                        break
                    elif op == '>' and spec[v] > n:
                        if w == 'A':
                            accepted_specs.append(spec)
                            wf = None
                        elif w == 'R':
                            wf = None
                        else:
                            wf = workflows[w]
                        break
                else:
                    if rule == 'A':
                        accepted_specs.append(spec)
                        wf = None
                    elif rule == 'R':
                        wf = None
                    else:
                        wf = workflows[rule]
                    break

    return accepted_specs


def sum_total(accepted_specs):
    total = 0
    for spec in accepted_specs:
        total += sum(a for a in spec.values())
    return total


def part_one(filename):
    data = read_puzzle_input(filename)
    workflows, specs = parse_data(data)
    accepted_specs = follow_workflows(workflows, specs)
    ans = sum_total(accepted_specs)
    return ans


def part_two(filename):
    data = read_puzzle_input(filename)
    workflows, specs = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(434147, part_one('Day_19_input.txt'))
        self.assertEqual(19114, part_one('Day_19_short_input.txt'))

    def test_part_two(self):
        self.assertEqual(136146366355609, part_two('Day_19_input.txt'))
        self.assertEqual(-1, part_two('Day_19_short_input.txt'))

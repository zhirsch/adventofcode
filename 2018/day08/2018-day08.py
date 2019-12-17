#!/usr/bin/python3

with open('2018-day08-input.txt') as f:
    input = [int(x) for x in f.read().split()]


#input = [int(x) for x in '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'.split()]


class Tree:

    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata


def parse_tree(input):
    num_children = input.pop(0)
    num_metadata = input.pop(0)
    children = [parse_tree(input) for _ in range(num_children)]
    metadata = [input.pop(0) for _ in range(num_metadata)]
    return Tree(children, metadata)


def compute_value(node):
    if not node.children:
        return sum(node.metadata)
    value = 0
    for i in node.metadata:
        if 0 < i <= len(node.children):
            value += compute_value(node.children[i - 1])
    return value


tree = parse_tree(input)
print(compute_value(tree))

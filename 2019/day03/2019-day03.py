#!/usr/bin/python3

wires = []
with open('2019-day03-input.txt') as f:
    for line in f:
        wires.append(line.strip().split(','))
# wires = [
#    'R8,U5,L5,D3'.split(','),
#    'U7,R6,D4,L4'.split(','),
# ]

grid = {(0, 0): 0}


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_vector(direction):
    return {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1),
    }[direction]


def walk(wire, callback):
    pos = (0, 0)
    for step in wire:
        vector = get_vector(step[0])
        for _ in range(int(step[1:])):
            pos = (pos[0] + vector[0], pos[1] + vector[1])
            callback(pos)


class Wire0Handler:

    def __init__(self):
        self.count = 0

    def __call__(self, pos):
        self.count += 1
        if pos not in grid:
            grid[pos] = self.count


walk(wires[0], Wire0Handler())


class Wire1Handler:

    def __init__(self):
        self.count = 0
        self.shortest_total = float('inf')

    def __call__(self, pos):
        self.count += 1
        if pos in grid:
            self.shortest_total = min(self.shortest_total, grid[pos] + self.count)


wire1handler = Wire1Handler()
walk(wires[1], wire1handler)

print(wire1handler.shortest_total)

#!/usr/bin/python3

import collections


def i(x, y):
    rack_id = x + 10
    return (rack_id * y + 5235) * rack_id // 100 % 10 - 5


I = collections.defaultdict(int)
for x in range(1, 301):
    for y in range(1, 301):
        I[(x, y)] = (
            i(x, y) +
            I[(x + 0, y - 1)] +
            I[(x - 1, y + 0)] -
            I[(x - 1, y - 1)]
        )

max_coord = None
max_power_level = float('-inf')
for s in range(1, 301):
    print(s)
    for x in range(1, 301 - s):
        for y in range(1, 301 - s):
            p = (
                I[(x + s, y + s)] +
                I[(x + 0, y + 0)] -
                I[(x + s, y + 0)] -
                I[(x + 0, y + s)]
            )
            if p > max_power_level:
                max_power_level = p
                max_coord = (x, y, s)

print(max_coord)

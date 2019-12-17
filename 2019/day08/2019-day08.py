#!/usr/bin/python3

import collections

with open('2019-day08-input.txt') as f:
    inp = [int(x) for x in f.read().strip()]

WIDTH = 25
HEIGHT = 6

raster = collections.defaultdict(lambda: 2)
for i, v in enumerate(inp):
    x = (i % (WIDTH * HEIGHT)) % WIDTH
    y = (i % (WIDTH * HEIGHT)) // WIDTH
    if raster[(x, y)] == 2:
        raster[(x, y)] = v

for i, v in enumerate(raster):
    x = i % WIDTH
    y = i // WIDTH
    print('x' if raster[(x, y)] == 1 else ' ', end='\n' if x == 24 else '')

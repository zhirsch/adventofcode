#!/usr/bin/python3

import re

PARSE = re.compile(r'^position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>$')


class Star:

    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def __repr__(self):
        return 'position=<%d, %d> velocity=<%d, %d>' % (self.x, self.y, self.dx, self.dy)

    def tick(self, c):
        self.x += self.dx * c
        self.y += self.dy * c


stars = []
with open('2018-day10-input.txt') as f:
    for line in f:
        m = PARSE.search(line.strip())
        stars.append(Star(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))

for star in stars:
    star.tick(10_027)

min_x = min(star.x for star in stars)
min_y = min(star.y for star in stars)
max_x = max(star.x for star in stars)
max_y = max(star.y for star in stars)

for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        for star in stars:
            if x == star.x and y == star.y:
                print('#', end='')
                break
        else:
            print('.', end='')
    print('')

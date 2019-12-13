#!/usr/bin/python3

import itertools
import math
import pprint
import re

PARSE_RE = re.compile(r'<x=([-0-9]+), y=([-0-9]+), z=([-0-9]+)>')


class Moon:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.dx = 0
        self.dy = 0
        self.dz = 0

    @staticmethod
    def parse(line):
        m = PARSE_RE.search(line)
        if not m:
            raise ValueError('bad input "%s"' % line)
        return Moon(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    def __str__(self):
        return '(%5d, %5d, %5d) moving at (%4d, %4d, %4d) with energy %d' % (
            self.x, self.y, self.z, self.dx, self.dy, self.dz, self.energy)

    def apply_gravity(self, other):
        self.dx += self._compute_acceleration(self.x, other.x)
        self.dy += self._compute_acceleration(self.y, other.y)
        self.dz += self._compute_acceleration(self.z, other.z)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz

    @property
    def energy(self):
        return (abs(self.x) + abs(self.y) + abs(self.z)) * (abs(self.dx) + abs(self.dy) + abs(self.dz))

    @staticmethod
    def _compute_acceleration(p1, p2):
        if p1 < p2:
            return 1
        if p1 > p2:
            return -1
        return 0


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def main():
    with open('input.txt') as f:
        inp = f.read()
#     inp = """<x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>"""
#     inp = """
#     <x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>"""
    initial_moons = [Moon.parse(line) for line in inp.strip().splitlines()]
    moons = [Moon.parse(line) for line in inp.strip().splitlines()]

    pprint.pprint([str(x) for x in moons])

    period_x, period_y, period_z = None, None, None
    for i in itertools.count():
        if period_x is not None and period_y is not None and period_z is not None:
            break
        for a in moons:
            for b in moons:
                if a == b:
                    continue
                a.apply_gravity(b)
        for moon in moons:
            moon.move()

        if period_x is None and all(moons[i].x == initial_moons[i].x and moons[i].dx == 0 for i in range(4)):
            print("x @ %d" % i)
            pprint.pprint([str(x) for x in moons])
            print()
            period_x = i + 1
        if period_y is None and all(moons[i].y == initial_moons[i].y and moons[i].dy == 0 for i in range(4)):
            print("y @ %d" % i)
            pprint.pprint([str(x) for x in moons])
            print()
            period_y = i + 1
        if period_z is None and all(moons[i].z == initial_moons[i].z and moons[i].dz == 0 for i in range(4)):
            print("z @ %d" % i)
            pprint.pprint([str(x) for x in moons])
            print()
            period_z = i + 1

    print(lcm(lcm(period_x, period_y), period_z))


if __name__ == '__main__':
    main()

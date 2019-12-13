#!/usr/bin/python3

import math


def distance(base, other):
    return math.sqrt((base[0] - other[0]) ** 2 + (base[1] - other[1]) ** 2)


def main():
    with open('input.txt') as f:
        inp = f.read().strip().splitlines()

    asteroids = set()
    for y, row in enumerate(inp):
        for x, value in enumerate(row):
            if value == '#':
                asteroids.add((x, y))

    angles = {}
    base = (22, 28)  # (16, 23)
    for asteroid in sorted(asteroids):
        if base == asteroid:
            continue
        angle = math.atan2(-(asteroid[1] - base[1]), asteroid[0] - base[0])
        angle -= math.pi / 2
        if angle <= 0:
            angle = 2 * math.pi - abs(angle)
        angles.setdefault(angle, []).append((distance(base, asteroid), asteroid))
    for values in angles.values():
        values.sort()

    asteroids.discard(base)

    i = 1
    while asteroids:
        for angle in sorted(angles, reverse=True):
            if not angles[angle]:
                continue
            asteroid = angles[angle].pop(0)[1]
            asteroids.discard(asteroid)
            print('%-3d: %s' % (i, asteroid))
            i += 1


if __name__ == '__main__':
    main()

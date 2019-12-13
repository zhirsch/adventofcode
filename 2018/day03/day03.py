#!/usr/bin/python3

import re


class Claim:
    PARSE = re.compile(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

    def __init__(self, id, x, y, w, h):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @staticmethod
    def of(s):
        m = Claim.PARSE.search(s)
        if not m:
            raise ValueError('oops')
        id = m.group(1)
        x = int(m.group(2))
        y = int(m.group(3))
        w = int(m.group(4))
        h = int(m.group(5))
        return Claim(id, x, y, w, h)

    def __iter__(self):
        for i in range(self.w):
            for j in range(self.h):
                yield (self.x + i, self.y + j)


class Fabric:

    def __init__(self, claims):
        self._squares = {}
        for claim in claims:
            for (x, y) in claim:
                self._squares.setdefault((x, y), []).append(claim)

    @property
    def squares(self):
        return self._squares.values()


def compute(claims):
    claims = set(claims)
    fabric = Fabric(claims)
    overlapping = set()
    for square in fabric.squares:
        if len(square) > 1:
            overlapping.update(square)
    return (claims - overlapping).pop()


def main():
    with open('input.txt') as f:
        print(compute(Claim.of(x) for x in f).id)


if __name__ == '__main__':
    main()

#!/usr/bin/python3


def shortest(grid, portals, w, h, src, dst):
    q = [(src, 0, 0)]  # pos, level, dist
    seen = {(src[0], src[1], 0)}  # pos x, # pos y, level

    while q:
        pos, level, dist = q.pop(0)
        if pos == dst and level == 0:
            return dist

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = pos[0] + dx, pos[1] + dy
            newlevel = level
            if grid[nx, ny].isupper():
                newlevel += -1 if (nx == 1 or ny == 1 or nx == w - 2 or ny == h - 2) else 1

                c = grid[min(nx, nx + dx), min(ny, ny + dy)] + grid[max(nx, nx + dx), max(ny, ny + dy)]
                if c not in ('AA', 'ZZ') and newlevel >= 0:
                    if pos == portals[c][0]:
                        nx, ny = portals[c][1]
                    else:
                        nx, ny = portals[c][0]

            if (nx, ny, newlevel) in seen:
                continue
            seen.add((nx, ny, newlevel))

            if grid[nx, ny] == '.':
                q.append(((nx, ny), newlevel, dist + 1))


def main():
    with open('input.txt') as f:
        inp = f.read().strip('\n').splitlines()

    grid = {}
    for y, line in enumerate(inp):
        for x, ch in enumerate(line):
            grid[x, y] = ch

    w = len(inp[0])
    h = len(inp)

    portals = {}
    for x in range(w - 1):
        for y in range(h - 1):
            if not grid[x, y].isupper():
                continue
            if grid[x, y + 1].isupper():
                c = grid[x, y] + grid[x, y + 1]
                if y > 0 and grid[x, y - 1] == '.':
                    portals.setdefault(c, []).append((x, y - 1))
                elif y < h - 2 and grid[x, y + 2] == '.':
                    portals.setdefault(c, []).append((x, y + 2))
            if grid[x + 1, y].isupper():
                c = grid[x, y] + grid[x + 1, y]
                if x > 0 and grid[x - 1, y] == '.':
                    portals.setdefault(c, []).append((x - 1, y))
                elif x < w - 2 and grid[x + 2, y] == '.':
                    portals.setdefault(c, []).append((x + 2, y))
    del x, y

    src = portals['AA'][0]
    dst = portals['ZZ'][0]

    print(shortest(grid, portals, w, h, src, dst))


if __name__ == '__main__':
    main()

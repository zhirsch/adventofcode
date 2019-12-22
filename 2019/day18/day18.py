#!/usr/bin/python3

DELTA_POS_LIST = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]


def reachable(grid, initial_pos, acquired_keys):
    queue = [initial_pos]
    distances = {initial_pos: 0}
    keys = {}
    while queue:
        pos = queue.pop(0)
        for dx, dy in DELTA_POS_LIST:
            new_pos = (pos[0] + dx, pos[1] + dy)
            ch = grid.get(new_pos)
            if not ch or ch == '#':
                continue
            if new_pos in distances:
                continue
            distances[new_pos] = distances[pos] + 1
            if ch.isupper() and ch.lower() not in acquired_keys:
                continue
            if ch.islower() and ch not in acquired_keys:
                keys[ch] = (distances[new_pos], new_pos)
                continue
            queue.append(new_pos)
    return keys


def reachable4(grid, starts, acquired_keys):
    keys = {}
    for i, start in starts.items():
        for key, (distance, pos) in reachable(grid, start, acquired_keys).items():
            new_starts = starts.copy()
            new_starts[i] = pos
            keys[key] = distance, new_starts
    return keys


def find_shortest_distance_internal(grid, starts, acquired_keys):
    distances = []
    for key, (distance, new_starts) in reachable4(grid, starts, acquired_keys).items():
        distances.append(distance + find_shortest_distance(grid, new_starts, acquired_keys | {key}))
    return min(distances or [0])


def find_shortest_distance(grid, starts, acquired_keys, memo={}):
    if (frozenset(starts.values()), acquired_keys) in memo:
        return memo[frozenset(starts.values()), acquired_keys]
    min_distance = find_shortest_distance_internal(grid, starts, acquired_keys)
    memo[frozenset(starts.values()), acquired_keys] = min_distance
    return min_distance


def main():
    with open('input.txt') as f:
        inp = f.read().strip().splitlines()

    grid = {}
    initial_x, initial_y = None, None
    for y, line in enumerate(inp):
        for x, ch in enumerate(line):
            grid[x, y] = ch
            if ch == '@':
                initial_x, initial_y = (x, y)

    grid[initial_x - 1, initial_y - 1] = '@'
    grid[initial_x - 1, initial_y + 0] = '#'
    grid[initial_x - 1, initial_y + 1] = '@'
    grid[initial_x + 0, initial_y - 1] = '#'
    grid[initial_x + 0, initial_y + 0] = '#'
    grid[initial_x + 0, initial_y + 1] = '#'
    grid[initial_x + 1, initial_y - 1] = '@'
    grid[initial_x + 1, initial_y + 0] = '#'
    grid[initial_x + 1, initial_y + 1] = '@'

    starts = {
        1: (initial_x - 1, initial_y - 1),
        2: (initial_x - 1, initial_y + 1),
        3: (initial_x + 1, initial_y - 1),
        4: (initial_x + 1, initial_y + 1),
    }
    # starts = {
    #     1: (initial_x, initial_y),
    # }

    print(find_shortest_distance(grid, starts, frozenset()))


if __name__ == '__main__':
    main()

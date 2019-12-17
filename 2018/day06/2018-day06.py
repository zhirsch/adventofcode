#!/usr/bin/python3


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


locations = []
with open('2018-day06-input.txt') as f:
    for line in f:
        tx, ty = line.strip().split(',')
        locations.append((int(tx), int(ty)))

min_x = min(x for x, y in locations)
max_x = max(x for x, y in locations)
min_y = min(y for x, y in locations)
max_y = max(y for x, y in locations)

grid = {}
for x in range(min_x, max_x + 1):
    for y in range(min_y, max_y + 1):
        pt = (x, y)
        grid[pt] = sum(distance(x, pt) for x in locations) < 10_000
print(sum(1 for x in grid.values() if x))

# distance_grid = {}
# location_grid = {}
# excluded_locations = set()
# for x in range(min_x, max_x + 1):
#     for y in range(min_y, max_y + 1):
#         pt = (x, y)
#         for i, location in enumerate(locations):
#             dist = distance(pt, location)
#             if pt not in distance_grid:
#                 distance_grid[pt] = dist
#                 location_grid[pt] = i
#                 continue
#             if dist < distance_grid[pt]:
#                 distance_grid[pt] = dist
#                 location_grid[pt] = i
#                 continue
#             if dist == distance_grid[pt]:
#                 location_grid[pt] = None
#                 continue
#         if x in (min_x, max_x) or y in (min_y, max_y):
#             excluded_locations.add(location_grid[pt])
#
# counts = collections.defaultdict(int)
# for location in location_grid.values():
#     if location is None:
#         continue
#     if location in excluded_locations:
#         continue
#     counts[location] += 1
#
# print(max(counts.values()))

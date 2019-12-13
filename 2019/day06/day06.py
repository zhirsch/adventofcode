#!/usr/bin/python3

import heapdict


def parse(lines):
    edges = {}
    for line in (x.strip() for x in lines if x.strip()):
        a, b = line.split(')', 1)
        edges.setdefault(a, []).append(b)
        edges.setdefault(b, []).append(a)
    return edges


def transfers(edges, src, dst):
    unvisited = heapdict.heapdict()
    unvisited[src] = 0

    distances = {src: 0}

    while unvisited:
        current, _ = unvisited.popitem()
        for node in edges[current]:
            alt = distances[current] + 1
            if alt < distances.get(node, float('inf')):
                distances[node] = alt
                unvisited[node] = alt
    return distances[dst]


def main():
    with open('input.txt') as f:
        edges = parse(f.readlines())

    assert len(edges['YOU']) == 1
    assert len(edges['SAN']) == 1
    print(transfers(edges, edges['YOU'][0], edges['SAN'][0]))


if __name__ == '__main__':
    main()

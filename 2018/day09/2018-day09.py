#!/usr/bin/python3

import re

PARSE = re.compile(r'^(\d+) players; last marble is worth (\d+) points$')

with open('2018-day09-input.txt') as f:
    m = PARSE.search(f.read().strip())
    players = int(m.group(1))
    marbles = int(m.group(2))
marbles *= 100


class Node:

    def __init__(self, marble):
        self.marble = marble
        self.next = self
        self.prev = self


class Circle:

    def __init__(self):
        self.circle = Node(0)
        self.current_marble = self.circle

    def insert(self, marble):
        node = Node(marble)
        node.next = self.current_marble.next.next
        node.next.prev = node
        node.prev = self.current_marble.next
        node.prev.next = node
        self.current_marble = node

    def pop(self):
        node = self.current_marble.prev.prev.prev.prev.prev.prev.prev
        self.current_marble = node.next
        node.prev.next = node.next
        node.next.prev = node.prev
        return node.marble


circle = Circle()
scores = {x: 0 for x in range(players)}
current_player = 0


for marble in range(1, marbles + 1):
    if marble % 23 == 0:
        scores[current_player] += marble + circle.pop()
    else:
        circle.insert(marble)
    current_player = (current_player + 1) % players
print(max(scores.values()))

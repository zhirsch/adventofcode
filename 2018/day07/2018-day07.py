#!/usr/bin/python3

import collections
import itertools
import pprint
import re

PARSE = re.compile(r'^Step (.) must be finished before step (.) can begin\.$')

step_dependencies = collections.defaultdict(set)
steps = set()


def parse(line):
    m = PARSE.search(line.strip())
    steps.add(m.group(1))
    steps.add(m.group(2))
    step_dependencies[m.group(2)].add(m.group(1))


with open('2018-day07-input.txt') as f:
    for line in f:
        parse(line)
# for line in [
#     'Step C must be finished before step A can begin.',
#     'Step C must be finished before step F can begin.',
#     'Step A must be finished before step B can begin.',
#     'Step A must be finished before step D can begin.',
#     'Step B must be finished before step E can begin.',
#     'Step D must be finished before step E can begin.',
#     'Step F must be finished before step E can begin.',
# ]:
#     parse(line)

pprint.pprint(steps)
pprint.pprint(step_dependencies)


class Worker:

    def __init__(self, id):
        self._id = id
        self._step = None
        self._remaining = -1

    def __str__(self):
        if self.busy:
            return 'Worker %d is working on %s (%d left)' % (self._id, self._step, self._remaining)
        return 'Worker %d is idle' % self._id

    def __repr__(self):
        return 'Worker(%d)' % self._id

    @property
    def busy(self):
        return self._step is not None

    def start(self, step):
        self._step = step
        self._remaining = 60 + (ord(step) - ord('A') + 1

    def tick(self):
        if not self.busy:
            return None
        self._remaining -= 1
        if self._remaining == 0:
            step = self._step
            self._step = None
            return step
        return None


order = []
def finish_step(step):
    order.append(step)
    for dependencies in step_dependencies.values():
        dependencies.discard(step)


workers = [Worker(x + 1) for x in range(5)]
for i in itertools.count(-1):
    print('%02d: %s' % (i, [str(x) for x in workers]))
    if not steps and not any(worker.busy for worker in workers):
        break
    free_workers = []
    for worker in workers:
        step = worker.tick()
        if step:
            finish_step(step)
        if not worker.busy:
            free_workers.append(worker)
    for free_worker in free_workers:
        for step in sorted(steps):
            if not step_dependencies[step]:
                free_worker.start(step)
                steps.remove(step)
                step_dependencies.pop(step)
                break
print(order)
print(i)

#!/usr/bin/python3

import collections
import re

GUARD_RE = re.compile('Guard #(\d+) begins shift')
TIME_RE = re.compile('\d\d\d\d-\d\d-\d\d \d\d:(\d\d)')


def compute(input):
    guards = {}
    i = 0
    while i < len(input):
        line = input[i]
        i += 1

        m = GUARD_RE.search(line)
        guard = guards.setdefault(int(m.group(1)), collections.defaultdict(int))

        asleep = None
        while i < len(input) and 'begins shift' not in input[i]:
            line = input[i]
            i += 1

            m = TIME_RE.search(line)
            if 'falls asleep' in line:
                asleep = int(m.group(1))
            if 'wakes up' in line:
                for minute in range(asleep, int(m.group(1))):
                    guard[minute] += 1

    max_guard = None
    max_minute = None
    max_asleep = 0
    for guard, minutes in guards.items():
        if not minutes:
            continue
        minute = max(minutes, key=lambda x: minutes[x])
        if max_asleep < minutes[minute]:
            max_guard = guard
            max_minute = minute
            max_asleep = minutes[minute]

    return max_guard * max_minute

def main():
    with open('input.txt') as f:
        # print(compute([
        #     "[1518-11-01 00:00] Guard #10 begins shift",
        #     "[1518-11-01 00:05] falls asleep",
        #     "[1518-11-01 00:25] wakes up",
        #     "[1518-11-01 00:30] falls asleep",
        #     "[1518-11-01 00:55] wakes up",
        #     "[1518-11-01 23:58] Guard #99 begins shift",
        #     "[1518-11-02 00:40] falls asleep",
        #     "[1518-11-02 00:50] wakes up",
        #     "[1518-11-03 00:05] Guard #10 begins shift",
        #     "[1518-11-03 00:24] falls asleep",
        #     "[1518-11-03 00:29] wakes up",
        #     "[1518-11-04 00:02] Guard #99 begins shift",
        #     "[1518-11-04 00:36] falls asleep",
        #     "[1518-11-04 00:46] wakes up",
        #     "[1518-11-05 00:03] Guard #99 begins shift",
        #     "[1518-11-05 00:45] falls asleep",
        #     "[1518-11-05 00:55] wakes up",
        # ]))
        print(compute(sorted(f.read().splitlines())))


if __name__ == '__main__':
    main()

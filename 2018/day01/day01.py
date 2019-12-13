#!/usr/bin/python3


def compute(changes):
    frequencies = set()
    frequency = 0
    while True:
        for change in changes:
            if frequency in frequencies:
                return frequency
            frequencies.add(frequency)
            frequency += change


def main():
    with open('input.txt') as f:
        frequency = compute(list(int(x) for x in f))
        assert frequency == 83130
        print(frequency)


if __name__ == '__main__':
    main()

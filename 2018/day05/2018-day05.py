#!/usr/bin/python3


def compute_fixed(input):
    accum = []
    for x in input:
        if not accum:
            accum.append(x)
            continue
        if str.isupper(accum[-1]) == str.isupper(x):
            accum.append(x)
            continue
        if accum[-1].lower() != x.lower():
            accum.append(x)
            continue
        accum.pop()
    return len(accum)


def compute(input):
    min_length = len(input)
    for type in sorted(set(x.lower() for x in input)):
        length = compute_fixed(x for x in input if x not in (type.lower(), type.upper()))
        print('%s: %d' % (type, length))
        min_length = min(length, min_length)
    return min_length


def main():
    with open('2018-day05-input.txt') as f:
        units = compute(list(f.read().strip()))
        print(units)


if __name__ == '__main__':
    main()

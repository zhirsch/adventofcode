#!/usr/bin/python3


def do_phase(inp, offset):
    outp = inp.copy()
    accum = 0
    for i in range(len(inp), offset, -1):
        accum += inp[i - 1]
        outp[i - 1] = accum % 10
    return outp


def main():
    with open('input.txt') as f:
        inp = [int(x) for x in f.read().strip()] * 10_000
    offset = int(''.join(str(x) for x in inp[:7]))
    assert offset > len(inp) / 2
    for _ in range(100):
        inp = do_phase(inp, offset)
    print(''.join(str(x) for x in inp[offset:offset + 8]))


if __name__ == '__main__':
    main()

#!/usr/bin/python3


def compute(ids):
    for x in ids:
        for y in ids:
            if x == y:
                continue
            if len(x) != len(y):
                continue
            same = ''
            differ = False
            for i in range(len(x)):
                if x[i] == y[i]:
                    same += x[i]
                    continue
                if differ:
                    break
                differ = True
            else:
                return same


def main():
    with open('input.txt') as f:
        checksum = compute(list(f))
        print(checksum)


if __name__ == '__main__':
    main()

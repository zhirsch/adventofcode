#!/usr/bin/python3 -tt
# https://adventofcode.com/2019/day/1

def needed_fuel(mass):
    fuel = mass // 3 - 2
    if fuel <= 0:
        return 0
    return fuel + needed_fuel(fuel)


def compute(mass_list):
    return sum(needed_fuel(x) for x in mass_list)


def main():
    with open('input.txt') as f:
        fuel = compute(int(x) for x in f)
        assert fuel == 4982961
        print(fuel)


if __name__ == '__main__':
    main()

#!/usr/bin/python3


class IntcodeComputer:

    def __init__(self, program):
        self.program = program
        self.ip = 0
        self.halted = False

    def step(self):
        {
            1: lambda: self._add(),
            2: lambda: self._mul(),
            99: lambda: self._hlt(),
        }[self._get_opcode()]()

    def _get_opcode(self):
        return self._get_int()

    def _get_int(self):
        value = self.program[self.ip]
        self.ip += 1
        return value

    def _add(self):
        a = self._get_int()
        b = self._get_int()
        d = self._get_int()
        self.program[d] = self.program[a] + self.program[b]

    def _mul(self):
        a = self._get_int()
        b = self._get_int()
        d = self._get_int()
        self.program[d] = self.program[a] * self.program[b]

    def _hlt(self):
        self.halted = True


def compute(initial_program):
    for noun in range(99):
        for verb in range(99):
            computer = IntcodeComputer(initial_program[:])
            computer.program[1] = noun
            computer.program[2] = verb
            while not computer.halted:
                computer.step()
            if computer.program[0] == 19690720:
                return 100 * noun + verb


def main():
    with open('input.txt') as f:
        print(compute([int(x) for x in f.read().split(',')]))


if __name__ == '__main__':
    main()

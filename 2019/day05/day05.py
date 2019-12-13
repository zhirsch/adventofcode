#!/usr/bin/python3

import collections


class IntcodeComputer:

    def __init__(self, program, inputs, outputs):
        self.program = program
        self.inputs = inputs
        self.outputs = outputs
        self.ip = 0
        self.halted = False

    def run(self):
        while not self.halted:
            self.step()

    def step(self):
        opcode, modes = self._decode(self._advance_ip())
        {
            1: lambda: self._add(modes),
            2: lambda: self._multiply(modes),
            3: lambda: self._input(),
            4: lambda: self._output(modes),
            5: lambda: self._jump_if_true(modes),
            6: lambda: self._jump_if_false(modes),
            7: lambda: self._less_than(modes),
            8: lambda: self._equals(modes),
            99: lambda: self._hlt(),
        }[opcode]()

    def _advance_ip(self):
        value = self.program[self.ip]
        self.ip += 1
        return value

    @staticmethod
    def _decode(instr):
        opcode = instr % 100
        instr //= 100
        modes = collections.defaultdict(int)
        while instr > 0:
            modes[len(modes)] = instr % 10
            instr //= 10
        return opcode, modes

    def _get_int(self, at, mode):
        return {
            0: lambda: self.program[at],
            1: lambda: at,
        }[mode]()

    def _add(self, modes):
        a = self._get_int(self._advance_ip(), modes[0])
        b = self._get_int(self._advance_ip(), modes[1])
        d = self._advance_ip()
        self.program[d] = a + b

    def _multiply(self, modes):
        a = self._get_int(self._advance_ip(), modes[0])
        b = self._get_int(self._advance_ip(), modes[1])
        d = self._advance_ip()
        self.program[d] = a * b

    def _input(self):
        d = self._advance_ip()
        self.program[d] = self.inputs.pop(0)

    def _output(self, modes):
        a = self._get_int(self._advance_ip(), modes[0])
        self.outputs.append(a)

    def _jump_if_true(self, modes):
        p = self._get_int(self._advance_ip(), modes[0])
        d = self._get_int(self._advance_ip(), modes[1])
        if p != 0:
            self.ip = d

    def _jump_if_false(self, modes):
        p = self._get_int(self._advance_ip(), modes[0])
        d = self._get_int(self._advance_ip(), modes[1])
        if p == 0:
            self.ip = d

    def _less_than(self, modes):
        a = self._get_int(self._advance_ip(), modes[0])
        b = self._get_int(self._advance_ip(), modes[1])
        d = self._advance_ip()
        self.program[d] = 1 if a < b else 0

    def _equals(self, modes):
        a = self._get_int(self._advance_ip(), modes[0])
        b = self._get_int(self._advance_ip(), modes[1])
        d = self._advance_ip()
        self.program[d] = 1 if a == b else 0

    def _hlt(self):
        self.halted = True


def main():
    inputs = [1]
    outputs = []
    with open('input.txt') as f:
        program = [int(x) for x in f.read().split(',')]
    IntcodeComputer(program, inputs, outputs).run()
    print(outputs)


if __name__ == '__main__':
    main()

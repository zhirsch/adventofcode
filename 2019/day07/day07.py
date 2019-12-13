#!/usr/bin/python3

import asyncio
import collections
import itertools


class IntcodeComputer:

    def __init__(self, program, input_queue, output_queue):
        self.program = program
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.ip = 0
        self.halted = False

    async def run(self):
        while not self.halted:
            await self.step()

    async def step(self):
        opcode, modes = self._decode(self._advance_ip())
        await {
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

    def _decode(self, instr):
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

    async def _add(self, modes):
        a = self._get_int(self._advance_ip(), modes[0])
        b = self._get_int(self._advance_ip(), modes[1])
        d = self._advance_ip()
        self.program[d] = a + b

    async def _multiply(self, modes):
        a = self._get_int(self._advance_ip(), modes[0])
        b = self._get_int(self._advance_ip(), modes[1])
        d = self._advance_ip()
        self.program[d] = a * b

    async def _input(self):
        d = self._advance_ip()
        self.program[d] = await self.input_queue.get()

    async def _output(self, modes):
        a = self._get_int(self._advance_ip(), modes[0])
        await self.output_queue.put(a)

    async def _jump_if_true(self, modes):
        p = self._get_int(self._advance_ip(), modes[0])
        d = self._get_int(self._advance_ip(), modes[1])
        if p != 0:
            self.ip = d

    async def _jump_if_false(self, modes):
        p = self._get_int(self._advance_ip(), modes[0])
        d = self._get_int(self._advance_ip(), modes[1])
        if p == 0:
            self.ip = d

    async def _less_than(self, modes):
        a = self._get_int(self._advance_ip(), modes[0])
        b = self._get_int(self._advance_ip(), modes[1])
        d = self._advance_ip()
        self.program[d] = 1 if a < b else 0

    async def _equals(self, modes):
        a = self._get_int(self._advance_ip(), modes[0])
        b = self._get_int(self._advance_ip(), modes[1])
        d = self._advance_ip()
        self.program[d] = 1 if a == b else 0

    async def _hlt(self):
        self.halted = True


async def evaluate(program, permutation):
    input_a = asyncio.Queue()
    input_b = asyncio.Queue()
    input_c = asyncio.Queue()
    input_d = asyncio.Queue()
    input_e = asyncio.Queue()

    await input_a.put(permutation[0])
    await input_a.put(0)
    await input_b.put(permutation[1])
    await input_c.put(permutation[2])
    await input_d.put(permutation[3])
    await input_e.put(permutation[4])

    await asyncio.gather(
        IntcodeComputer(program.copy(), input_a, input_b).run(),
        IntcodeComputer(program.copy(), input_b, input_c).run(),
        IntcodeComputer(program.copy(), input_c, input_d).run(),
        IntcodeComputer(program.copy(), input_d, input_e).run(),
        IntcodeComputer(program.copy(), input_e, input_a).run(),
    )
    return await input_a.get()


def main():
    with open('input.txt') as f:
        program = [int(x) for x in f.read().strip().split(',')]
    permutations = itertools.permutations(range(5, 10))
    print(max(asyncio.run(evaluate(program, x)) for x in permutations))


if __name__ == '__main__':
    main()

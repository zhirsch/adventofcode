#!/usr/bin/python3

import asyncio
import collections


class IntcodeComputer:

    def __init__(self, program, input_queue, output_queue):
        self.program = program
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.ip = 0
        self.relative_base = 0
        self.halted = asyncio.Event()

    @property
    def finished(self):
        return self.halted.is_set() and self.output_queue.empty()

    async def run(self):
        while not self.halted.is_set():
            await self.step()

    async def step(self):
        opcode, modes = self._decode(self._advance_ip())
        await {
            1: lambda: self._add(modes),
            2: lambda: self._multiply(modes),
            3: lambda: self._input(modes),
            4: lambda: self._output(modes),
            5: lambda: self._jump_if_true(modes),
            6: lambda: self._jump_if_false(modes),
            7: lambda: self._less_than(modes),
            8: lambda: self._equals(modes),
            9: lambda: self._relative_base_offset(modes),
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

    def _read(self, at, mode):
        if mode == 0:
            self._extend_program(at)
            return self.program[at]
        if mode == 1:
            return at
        if mode == 2:
            at = self.relative_base + at
            self._extend_program(at)
            return self.program[at]
        raise ValueError('bad read mode')

    def _write(self, at, mode, value):
        if mode == 0:
            self._extend_program(at)
            self.program[at] = value
            return
        if mode == 1:
            raise ValueError('write with mode=1 not allowed')
        if mode == 2:
            at = self.relative_base + at
            self._extend_program(at)
            self.program[at] = value
            return
        raise ValueError('bad write mode')

    def _extend_program(self, at):
        while at >= len(self.program):
            self.program.append(0)

    async def _add(self, modes):
        a = self._read(self._advance_ip(), modes[0])
        b = self._read(self._advance_ip(), modes[1])
        d = self._advance_ip()
        self._write(d, modes[2], a + b)

    async def _multiply(self, modes):
        a = self._read(self._advance_ip(), modes[0])
        b = self._read(self._advance_ip(), modes[1])
        d = self._advance_ip()
        self._write(d, modes[2], a * b)

    async def _input(self, modes):
        d = self._advance_ip()
        self._write(d, modes[0], await self.input_queue.get())

    async def _output(self, modes):
        a = self._read(self._advance_ip(), modes[0])
        await self.output_queue.put(a)

    async def _jump_if_true(self, modes):
        p = self._read(self._advance_ip(), modes[0])
        d = self._read(self._advance_ip(), modes[1])
        if p != 0:
            self.ip = d

    async def _jump_if_false(self, modes):
        p = self._read(self._advance_ip(), modes[0])
        d = self._read(self._advance_ip(), modes[1])
        if p == 0:
            self.ip = d

    async def _less_than(self, modes):
        a = self._read(self._advance_ip(), modes[0])
        b = self._read(self._advance_ip(), modes[1])
        d = self._advance_ip()
        self._write(d, modes[2], 1 if a < b else 0)

    async def _equals(self, modes):
        a = self._read(self._advance_ip(), modes[0])
        b = self._read(self._advance_ip(), modes[1])
        d = self._advance_ip()
        self._write(d, modes[2], 1 if a == b else 0)

    async def _relative_base_offset(self, modes):
        a = self._read(self._advance_ip(), modes[0])
        self.relative_base += a

    async def _hlt(self):
        self.halted.set()


async def inbeam(program, x, y):
    computer = IntcodeComputer(program.copy(), asyncio.Queue(), asyncio.Queue())
    await computer.input_queue.put(x)
    await computer.input_queue.put(y)
    await computer.run()
    return await computer.output_queue.get() == 1


async def run(program):
    x, y = 0, 0
    while True:
        print(x, y)
        while True:
            tr = await inbeam(program, x + 99, y)
            if not tr:
                break
            bl = await inbeam(program, x +  0, y + 99)
            br = await inbeam(program, x + 99, y + 99)
            if bl and br:
                print(x * 10_000 + y)
                return
            x += 1
        y += 1
        while True:
            tl = await inbeam(program, x, y)
            if not tl:
                break
            x -= 1
        x += 1


def main():
    with open('input.txt') as f:
        program = [int(x) for x in f.read().split(',')]
    asyncio.run(run(program))


if __name__ == '__main__':
    main()

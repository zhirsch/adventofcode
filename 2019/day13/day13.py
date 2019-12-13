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


async def move(input_queue, paddle_x, ball_x):
    if paddle_x > ball_x:
        await input_queue.put(-1)
    elif paddle_x < ball_x:
        await input_queue.put(1)
    else:
        await input_queue.put(0)


def display_grid(grid):
    max_x = max(e[0] for e in grid)
    max_y = max(e[1] for e in grid)

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            ch = {
                0: ' ',
                1: 'W',
                2: 'B',
                3: '=',
                4: '*',
            }[grid.get((x, y), 0)]
            print(ch, end='')
        print()
    print()
    print()


async def pump(computer):
    while not computer.halted.is_set() or not computer.output_queue.empty():
        x = await computer.output_queue.get()
        y = await computer.output_queue.get()
        tile_id = await computer.output_queue.get()
        yield x, y, tile_id


async def execute(computer):
    grid = {}
    paddle_x = None
    score = None

    await computer.input_queue.put(0)
    async for (x, y, value) in pump(computer):
        if x == -1 and y == 0:
            score = value
            display_grid(grid)
            continue
        grid[(x, y)] = value
        if value == 3:
            paddle_x = x
            continue
        if value == 4 and score is not None:
            await move(computer.input_queue, paddle_x, x)
    print('final score = %d' % score)


async def run(program):
    program[0] = 2

    input_queue = asyncio.Queue(maxsize=1)
    output_queue = asyncio.Queue()
    computer = IntcodeComputer(program, input_queue, output_queue)
    await asyncio.gather(computer.run(), execute(computer))
    await computer.run()


def main():
    with open('input.txt') as f:
        program = [int(x) for x in f.read().split(',')]
    asyncio.run(run(program))


if __name__ == '__main__':
    main()

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


def print_grid(grid):
    min_x = min(e[0] for e in grid)
    max_x = max(e[0] for e in grid)
    min_y = min(e[1] for e in grid)
    max_y = max(e[1] for e in grid)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            value = grid.get((x, y), '?')
            print(value, end='')
        print()
    print()


async def execute(computer, pos, grid):
    await move(computer, pos, 1, grid)
    await move(computer, pos, 2, grid)
    await move(computer, pos, 3, grid)
    await move(computer, pos, 4, grid)


async def move(computer, pos, direction, grid):
    pos = next_pos(pos, direction)
    if pos in grid:
        return
    await computer.input_queue.put(direction)
    result = await computer.output_queue.get()
    if result == 0:
        grid[pos] = '#'
        return
    if result == 1:
        grid[pos] = '.'
    if result == 2:
        grid[pos] = 'O'
    await execute(computer, pos, grid)
    await computer.input_queue.put(opposite_direction(direction))
    assert await computer.output_queue.get() == 1


def next_pos(pos, direction):
    return {
        1: (pos[0], pos[1] + 1),
        2: (pos[0], pos[1] - 1),
        3: (pos[0] - 1, pos[1]),
        4: (pos[0] + 1, pos[1]),
    }[direction]


def opposite_direction(direction):
    return {
        1: 2,
        2: 1,
        3: 4,
        4: 3,
    }[direction]


async def run(program):
    computer = IntcodeComputer(program, asyncio.Queue(), asyncio.Queue())
    asyncio.create_task(computer.run())

    pos = (0, 0)
    grid = {pos: '.'}
    await execute(computer, pos, grid)
    print_grid(grid)

    min_x = min(e[0] for e in grid)
    max_x = max(e[0] for e in grid)
    min_y = min(e[1] for e in grid)
    max_y = max(e[1] for e in grid)
    for minutes in itertools.count(1):
        new_grid = grid.copy()
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                pos = (x, y)
                value = grid.get((x, y), '#')
                if value in ('#', '.'):
                    continue
                if value == 'O':
                    for direction in [1, 2, 3, 4]:
                        spread_pos = next_pos(pos, direction)
                        if grid.get(spread_pos, '#') == '.':
                            new_grid[spread_pos] = 'O'
        print(minutes)
        grid = new_grid
        if not any(x == '.' for x in grid.values()):
            break


def main():
    with open('input.txt') as f:
        program = [int(x) for x in f.read().split(',')]
    asyncio.run(run(program))


if __name__ == '__main__':
    main()

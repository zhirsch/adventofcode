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


async def send_line(computer, line):
    for ch in line:
        await computer.input_queue.put(ord(ch))
    await computer.input_queue.put(ord('\n'))


async def recv_line(computer):
    line = []
    while True:
        output = await computer.output_queue.get()
        print(output)
        output = chr(output)
        if output == '\n':
            return ''.join(line)
        line.append(output)


async def recv_grid(computer):
    grid = {}
    for y in itertools.count():
        line = await recv_line(computer)
        if line == '':
            break
        for x, ch in enumerate(line):
            grid[(x, y)] = ch
    return grid


def find_robot(grid):
    for y in range(39):
        for x in range(63):
            p = (x, y)
            if grid[p] in ('^', '<', '>', 'v'):
                return p, grid[p]
    return None


async def execute(computer):
    # A  = R,6,L,12,R,6
    # B  =     L,12,R,6,L,8
    # C  = L,12,R,12,L,10,L,10

    # A  = R,6,L,12,R,6
    # B  =     L,12,R,6,L,8
    # C  = L,12,R,12,L,10,L,10

    # R,6,L,12,R,6
    # R,6,L,12,R,6
    # L,12,R,6,L,8,L,12
    # R,12,L,10,L,10
    # L,12,R,6,L,8,L,12
    # R,12,L,10,L,10
    # L,12,R,6,L,8,L,12
    # R,12,L,10,L,10
    # L,12,R,6,L,8,L,12
    # R,6,L,12,R,6

    # A,A,B,C,B,C,B,C,B,B    4,R,6

    grid = await recv_grid(computer)
    robot_pos, robot = find_robot(grid)

    assert await recv_line(computer) == 'Main:'
    await send_line(computer, 'A,A,B,C,B,C,B,C,B,A')

    assert await recv_line(computer) == 'Function A:'
    await send_line(computer, 'R,6,L,12,R,6')

    assert await recv_line(computer) == 'Function B:'
    await send_line(computer, 'L,12,R,6,L,8,L,12')

    assert await recv_line(computer) == 'Function C:'
    await send_line(computer, 'R,12,L,10,L,10')

    assert await recv_line(computer) == 'Continuous video feed?'
    await send_line(computer, 'n')

    assert await recv_line(computer) == ''

    while not computer.finished:
        print_grid(grid)
        grid[robot_pos] = '%'
        robot_pos, robot = find_robot(await recv_grid(computer))
        grid[robot_pos] = robot


def print_grid(grid):
    min_x = min(e[0] for e in grid)
    max_x = max(e[0] for e in grid)
    min_y = min(e[1] for e in grid)
    max_y = max(e[1] for e in grid)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            ch = grid[(x, y)]
            if ch == '.':
                ch = ' '
            print(ch, end='')
        print()
    print()


async def run(program):
    program[0] = 2
    computer = IntcodeComputer(program, asyncio.Queue(), asyncio.Queue())
    await asyncio.gather(computer.run(), execute(computer))


def main():
    with open('input.txt') as f:
        program = [int(x) for x in f.read().split(',')]
    asyncio.run(run(program))


if __name__ == '__main__':
    main()

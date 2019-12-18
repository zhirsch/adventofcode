#!/usr/bin/python3

from ortools.linear_solver import pywraplp


class Reaction:

    def __init__(self, output, inputs):
        self.output = output
        self.inputs = inputs

    @staticmethod
    def parse(s):
        lhs, rhs = s.strip().split(' => ', 1)
        return Reaction(Chemical.parse(rhs), [Chemical.parse(x) for x in lhs.split(', ')])


class Chemical:

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    @staticmethod
    def parse(s):
        quantity, name = s.strip().split(None, 1)
        return Chemical(name.strip(), int(quantity))


def define_lp(solver, reactions):
    consumed = {chemical.name: [] for reaction in reactions for chemical in reaction.inputs}
    produced = {'ORE': solver.IntVar(0, float('inf'), 'ORE')}

    # The number of times the reaction occurs controls how much of each chemical is consumed and produced.
    for i, reaction in enumerate(reactions):
        count_var = solver.IntVar(0, float('inf'), 'Count_%d' % i)
        for chemical in reaction.inputs:
            consumed_var = solver.IntVar(0, float('inf'), '%s_%d' % (chemical.name, i))
            solver.Add(count_var * chemical.quantity == consumed_var)
            consumed[chemical.name].append(consumed_var)
        produced_var = solver.IntVar(0, float('inf'), reaction.output.name)
        solver.Add(count_var * reaction.output.quantity == produced_var)
        produced[reaction.output.name] = produced_var

    # The total amount of each chemical that is consumed across all reactions must be no more than the total amount of
    # that chemical that is produced.
    for name in consumed:
        solver.Add(sum(consumed[name]) <= produced[name])


def main():
    reactions = []
    with open('input.txt') as f:
        for line in f:
            reactions.append(Reaction.parse(line.strip()))

    # Part 1
    solver = pywraplp.Solver('day14', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    define_lp(solver, reactions)
    solver.Add(solver.LookupVariable('FUEL') == 1)
    objective = solver.Objective()
    objective.SetCoefficient(solver.LookupVariable('ORE'), 1)
    objective.SetMinimization()
    solver.Solve()
    print('PART 1: ORE = %d' % solver.LookupVariable('ORE').solution_value())

    # Part 2
    solver = pywraplp.Solver('day14', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    define_lp(solver, reactions)
    solver.Add(solver.LookupVariable('ORE') == 1_000_000_000_000)
    objective = solver.Objective()
    objective.SetCoefficient(solver.LookupVariable('FUEL'), 1)
    objective.SetMaximization()
    solver.Solve()
    print('PART 2: FUEL = %d' % solver.LookupVariable('FUEL').solution_value())


if __name__ == '__main__':
    main()

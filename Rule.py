from util import *

"""
shows a grammar rule in the form: LHS -> RHS
RHS = right-hand side
LHS = left-hand side
"""


class Rule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def get_all_symbols(self):
        return list(self.lhs + self.rhs)

    def get_rhs_symbols(self):
        return list(self.rhs)

    def get_rhs_non_terminals(self):
        return [rhs for rhs in self.get_rhs_symbols() if is_non_terminal(rhs)]

    def get_lhs_symbols(self):
        return list(self.lhs)

    def is_unit_production(self):
        return len(self.rhs) == 1 and is_non_terminal(self.rhs)

    def __str__(self):
        return self.lhs + "  ->  " + self.rhs

    def __eq__(self, other):
        if type(other) is Rule:
            return self.lhs == other.lhs and self.rhs == other.rhs
        return False

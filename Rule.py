from util import *


class Rule:
    def __init__(self, lhs, rhs):
        """
        RHS = right-hand side
        LHS = left-hand side
        """
        self.lhs = lhs
        self.rhs = rhs

    def get_all_rule_symbols(self):
        return list(self.lhs + self.rhs)

    def get_rhs_symbols(self):
        return list(self.rhs)

    def get_rhs_non_terminals(self):
        return [rhs for rhs in self.get_rhs_symbols() if is_non_terminal(rhs)]

    def get_lhs_symbols(self):
        return list(self.lhs)

    def __str__(self):
        return self.lhs + "  ->  " + self.rhs

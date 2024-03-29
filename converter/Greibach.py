from converter.Chomsky import Chomsky
from converter.Converter import Converter
from converter.Rule import Rule
from converter.util import *

"""
Please watch these tutorial for further explanations:
-   Greibach normal form:
    https://www.youtube.com/watch?v=ZCbJan6CGNM&list=PLBlnK6fEyqRgp46KUv4ZY69yXmpwKOIev&index=81
-   Removal of left recursion:
    https://www.youtube.com/watch?v=rauqqM0nfuI&list=PLBlnK6fEyqRgp46KUv4ZY69yXmpwKOIev&index=82
"""


class Greibach(Converter):
    def __init__(self, grammar):
        super().__init__(grammar)
        self.mapping = dict()
        self.reverse_mapping = dict()

    def convert(self):
        chomsky_converter = Chomsky(self.grammar, should_simplify=False)
        self.grammar = chomsky_converter.convert()

        self.map_non_terminal_to_ordered_symbols()
        self.sort_rules()
        self.remove_left_recursion()
        self.make_rhs_first_symbol_terminal()
        self.grammar.sort()
        return self.grammar

    def map_non_terminal_to_ordered_symbols(self):
        """
        Assign a value "i" for non-terminals with ascending order
        """
        current_number = 0
        for rule in self.grammar.rules:
            rule_symbols = rule.get_all_symbols()
            for symbol in rule_symbols:
                if is_non_terminal(symbol) and symbol not in self.mapping:
                    self.mapping[symbol] = current_number
                    self.reverse_mapping[current_number] = symbol
                    current_number += 1

    def sort_rules(self):
        """
        Alter the rules so that the non-terminals are in ascending order, such that if a production s of form
        Ai -> Aj x, then i < j
        """
        while True:
            for index, rule in enumerate(self.grammar.rules):
                # Check if i > j
                if is_non_terminal(rule.rhs[0]) and self.mapping[rule.lhs] > self.mapping[rule.rhs[0]]:
                    matching_rules = self.grammar[rule.rhs[0]]
                    new_rules = []
                    # substitute Aj using production rules
                    for r in matching_rules:
                        # avoid left recursion
                        if r.lhs != r.rhs[0]:
                            new_rule = Rule(rule.lhs, r.rhs + rule.rhs[1:])
                            new_rules.append(new_rule)
                    self.grammar.rules += new_rules
                    self.grammar.rules.remove(rule)
                    break
            else:
                break

    def remove_left_recursion(self):
        while True:
            for index, rule in enumerate(self.grammar.rules):
                if is_non_terminal(rule.rhs[0]) and rule.lhs == rule.rhs[0]:
                    # find all recursive rules with same lhs
                    recursive_rules = [r for r in self.grammar[rule.lhs] if r.lhs == r.rhs[0]]

                    new_symbols = []
                    for rule2 in recursive_rules:
                        new_non_terminal = self.grammar.get_unused_non_terminal()
                        new_symbols.append(new_non_terminal)
                        self.grammar.rules.append(Rule(new_non_terminal, rule2.rhs[1:]))
                        self.grammar.rules.append(Rule(new_non_terminal, rule2.rhs[1:]+new_non_terminal))

                    self.grammar.rules = [rule for rule in self.grammar.rules if rule not in recursive_rules]

                    for sym in new_symbols:
                        lhs_alternative_rules = self.grammar[rule.lhs]
                        new_rules = []
                        for r in lhs_alternative_rules:
                            new_rules.append(Rule(rule.lhs, r.rhs + sym))
                        self.grammar.rules += new_rules

                    break
            else:
                break

    def make_rhs_first_symbol_terminal(self):
        while True:
            for index, rule in enumerate(self.grammar.rules):
                if is_non_terminal(rule.rhs[0]):
                    indices = self.grammar.find_rules_by_lhs(rule.rhs[0])
                    for idx in indices:
                        self.grammar.rules.append(Rule(rule.lhs, self.grammar.rules[idx].rhs + rule.rhs[1:]))
                    self.grammar.rules.remove(rule)
                    break
            else:
                break

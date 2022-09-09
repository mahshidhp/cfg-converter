from Chomsky import Chomsky
from Converter import Converter
from util import *

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
        chomsky_converter = Chomsky(self.grammar)
        self.grammar = chomsky_converter.convert()
        self.messages = chomsky_converter.messages

        self.map_non_terminal_to_ordered_symbols()
        self.sort_rules()
        self.remove_left_recursion()
        return self.grammar

    def map_non_terminal_to_ordered_symbols(self):
        current_number = 0
        for rule in self.grammar.rules:
            rule_symbols = rule["lhs"] + rule["rhs"]
            for symbol in rule_symbols:
                if is_non_terminal(symbol) and symbol not in self.mapping:
                    self.mapping[symbol] = current_number
                    self.reverse_mapping[current_number] = symbol
                    current_number += 1

    def sort_rules(self):
        while True:
            for i in range(len(self.grammar.rules)):
                rule = self.grammar.rules[i]
                if is_non_terminal(rule["rhs"][0]) and self.mapping[rule["lhs"]] >= self.mapping[rule["rhs"][0]]:
                    indices = self.grammar.find_rules_by_lhs(rule["rhs"][0])
                    for index in indices:
                        pass
            else:
                break

    def remove_left_recursion(self):
        pass

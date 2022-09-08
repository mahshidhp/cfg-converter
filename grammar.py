from util import *
import random
import string


class Grammar:
    def __init__(self, rules):
        self.rules = rules
        self.terminals = set()
        self.non_terminals = set()

        self.split_rules()
        self.detect_symbols()

    def detect_symbols(self):
        for rule in self.rules:
            rule_symbols = rule["rhs"] + rule["lhs"]
            for symbol in rule_symbols:
                if is_terminal(symbol):
                    self.terminals.add(symbol)
                elif is_non_terminal(symbol):
                    self.non_terminals.add(symbol)

    def split_rules(self):
        """
        split rules with more than 1 right-hand-side to multiple rules with 1 right-hand-side
        example:
        A -> a | b | c
        will be converted to:
        A -> a
        A -> b
        A -> c
        """
        for i in range(len(self.rules)):
            if len(self.rules[i]["rhs"]) > 1:
                for rhs in self.rules[i]["rhs"][1:]:
                    self.rules.append({"lhs": self.rules[i]["lhs"], "rhs": rhs})
            self.rules[i]["rhs"] = self.rules[i]["rhs"][0]

    def get_unused_non_terminal(self):
        new_symbol = random.choice(string.ascii_uppercase)
        while new_symbol in self.non_terminals:
            new_symbol = random.choice(string.ascii_uppercase)
        self.non_terminals.add(new_symbol)
        return new_symbol

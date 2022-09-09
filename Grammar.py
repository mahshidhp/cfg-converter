from util import *
from Rule import Rule
import random
import string


class Grammar:
    def __init__(self, rules):
        self.rules = []
        self.terminals = set()
        self.non_terminals = set()
        self.start_symbol = 'S'

        self.build_rules(rules)
        self.detect_symbols()

    def detect_symbols(self):
        for rule in self.rules:
            for symbol in rule.get_all_rule_symbols():
                if is_terminal(symbol):
                    self.terminals.add(symbol)
                elif is_non_terminal(symbol):
                    self.non_terminals.add(symbol)

    def split_rules(self, rules):
        """
        split rules with more than 1 right-hand-side to multiple rules with 1 right-hand-side
        example:
        A -> a | b | c
        will be converted to:
        A -> a
        A -> b
        A -> c
        """
        for i in range(len(rules)):
            if len(rules[i]["rhs"]) > 1:
                for rhs in rules[i]["rhs"][1:]:
                    rules.append({"lhs": rules[i]["lhs"], "rhs": rhs})
            rules[i]["rhs"] = rules[i]["rhs"][0]

        return rules

    def build_rules(self, rules):
        rules = self.split_rules(rules)
        self.rules = [Rule(rule["lhs"], rule["rhs"]) for rule in rules]

    def get_unused_non_terminal(self):
        new_symbol = random.choice(string.ascii_uppercase)
        while new_symbol in self.non_terminals:
            new_symbol = random.choice(string.ascii_uppercase)
        self.non_terminals.add(new_symbol)
        return new_symbol

    def find_rules_by_lhs(self, lhs):
        result = []
        for index, rule in enumerate(self.rules):
            if rule.lhs == lhs:
                result.append(index)
        return result

    def find_rules_by_rhs(self, rhs):
        result = []
        for index, rule in enumerate(self.rules):
            if rule.rhs == rhs:
                result.append(index)
        return result

    def get_json_rules(self):
        return [{"rhs": rule.rhs, "lhs": rule.lhs} for rule in self.rules]
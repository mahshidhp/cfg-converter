from util import *
from Rule import Rule
from collections import defaultdict
import random
import string


class Grammar:
    def __init__(self, rules):
        self.rules = []
        self.build_rules(rules)
        self.terminals = set()
        self.non_terminals = set()
        self.detect_symbols()
        self.start_symbol = self.detect_start_symbol()
        if not self.check_is_CFG():
            raise Exception("Input grammar is not CFG.")

    def detect_start_symbol(self):
        return '$' if '$' in self.non_terminals else 'S'

    def __getitem__(self, lhs):
        return [self.rules[i] for i in self.find_rules_by_lhs(lhs)]

    def detect_symbols(self):
        for rule in self.rules:
            for symbol in rule.get_all_symbols():
                if is_terminal(symbol):
                    self.terminals.add(symbol)
                elif is_non_terminal(symbol):
                    self.non_terminals.add(symbol)

    @staticmethod
    def split_rules(rules):
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

    def check_is_CFG(self):
        """
        Context free grammars (CFGs) have rules in the following format:
        A -> {T U V}*
        where A is a non-terminal, T is set of terminals and V is set of non-terminals.
        """
        for rule in self.rules:
            if rule.lhs is None or len(rule.lhs) != 1 or is_terminal(rule.lhs):
                return False
            for symbol in rule.get_all_symbols():
                if not is_terminal(symbol) and not is_non_terminal(symbol):
                    return False
        return True

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

    def get_json_compact_rules(self):
        rules_dict = defaultdict()
        for rule in self.rules:
            if rule.lhs not in rules_dict:
                rules_dict[rule.lhs] = [rule.rhs]
            else:
                rules_dict[rule.lhs].append(rule.rhs)
        return [{"rhs": rhs, "lhs": lhs} for lhs, rhs in rules_dict.items()]

    # def is_tag(self, sym):
    #     """
    #     Checks whether the given symbol is a tag, i.e. a non-terminal with rules
    #     to solely terminals.
    #     """
    #
    #     if is_non_terminal(sym):
    #         rules = [self.rules[i] for i in self.find_rules_by_lhs(sym)]
    #         return all(is_terminal(s) for r in rules for s in r.rhs)
    #     return False

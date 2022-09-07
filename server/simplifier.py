from util import *

EPSILON = "ε"


class Simplifier:
    def __init__(self, grammar):
        self.grammar = grammar
        self.messages = []

    def simplify(self):
        # self.remove_redundant_rules()
        self.remove_unit_production()
        # self.remove_null_production()
        return self.grammar

    """
    Removing redundant symbols:
    
    phase 1:
    A -> a
    """
    def remove_redundant_rules(self):
        pass

    def generate_redundant_rules_message(self, redundant_rules):
        if len(redundant_rules) == 0:
            self.messages.append("There were no redundant rules")
        elif len(redundant_rules) == 1:
            self.messages.append(redundant_rules[0] + " was redundant")
        else:
            redundant_rules_str = ",".join(redundant_rules)
            self.messages.append(redundant_rules_str + " were redundant")

    """
    Unit production:
    A -> B  (A,B ∈ non-terminals)
    
    1- Add A -> x to grammar whenever B -> x occurs
    2- Delete A -> B from grammar
    """
    def remove_unit_production(self):
        unit_productions = []
        while True:
            for rule in self.grammar.rules:
                if self.check_is_unit_production(rule) and self.find_rules_by_lhs(rule["rhs"]):
                    next_rule_index = self.find_rules_by_lhs(rule["rhs"])
                    if next_rule_index:
                        unit_productions.append(rule["lhs"]+"  →  "+rule["rhs"])
                        rule["rhs"] = self.grammar.rules[next_rule_index]["rhs"]
                        del(self.grammar.rules[next_rule_index])
                        break
            else:
                break
        self.generate_unit_production_message(unit_productions)

    def check_is_unit_production(self, rule):
        return len(rule["rhs"]) == 1 and len(rule["lhs"]) == 1 and \
               is_non_terminal(rule["lhs"]) and is_non_terminal(rule["rhs"])

    def generate_unit_production_message(self, unit_productions):
        unit_productions_str = ",".join(unit_productions)
        if len(unit_productions) == 0:
            self.messages.append("There were no unit productions")
        elif len(unit_productions) == 1:
            self.messages.append(unit_productions_str + " was unit production")
        else:
            self.messages.append(unit_productions_str + " were unit productions")

    """
    Null production:
    A -> ε or A -> ... -> ε
    
    1- Look for all productions whose right-side contains A
    2- Replace each occurrences of A in these productions with ε
    3- Add the result productions to the grammar
    """
    def remove_null_production(self):
        null_productions = []
        while True:
            for rule in self.grammar.rules:
                if rule["rhs"] == EPSILON:
                    prev_element = rule["lhs"]
                    while len(prev_element) != 1:
                        next_null_rule = self.find_rules_by_rhs(prev_element)
            else:
                break
        self.generate_null_production_message(null_productions)

    def generate_null_production_message(self, null_productions):
        if len(null_productions) == 0:
            self.messages.append("There were no null productions")
        elif len(null_productions) == 1:
            self.messages.append(null_productions[0] + " was null production")
        else:
            null_productions_str = ",".join(null_productions)
            self.messages.append(null_productions_str + " were null productions")

    def find_rules_by_lhs(self, lhs):
        for i in range(len(self.grammar.rules)):
            rule = self.grammar.rules[i]
            if rule["lhs"] == lhs:
                return i
        return None

    def find_rules_by_rhs(self, rhs):
        for i in range(len(self.grammar.rules)):
            rule = self.grammar.rules[i]
            if rule["rhs"] == rhs:
                return i
        return None

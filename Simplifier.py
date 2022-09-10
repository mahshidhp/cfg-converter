from util import *

EPSILON = "ε"


class Simplifier:
    def __init__(self, grammar):
        self.grammar = grammar
        self.messages = []

    def simplify(self):
        self.remove_redundant_rules()
        self.remove_unit_production()
        # self.remove_null_production()
        return self.grammar

    """
    Removing redundant symbols:
    
    phase 1:
    find non-terminals that don't generate a terminal and remove rules containing them
    phase 2:
    find non-terminal tha are unreachable from starting symbol
    """
    def remove_redundant_rules(self):
        # Phase 1
        prev_set = set()
        current_set = self.grammar.terminals.copy()
        while prev_set != current_set:
            prev_set = current_set.copy()
            for rule in self.grammar.rules:
                # check if current rule derives any of current_set symbols
                rhs_current_set_intersection = [symbol for symbol in rule.get_rhs_symbols() if symbol in current_set]
                if len(rhs_current_set_intersection) > 0:
                    current_set.add(rule.lhs)

        redundant_non_terminals = self.grammar.non_terminals.difference(current_set)
        self.remove_rules_with_redundant_symbols(redundant_non_terminals)

        # Phase 2
        prev_set = set()
        current_set = {self.grammar.start_symbol}
        while prev_set != current_set:
            prev_set = current_set.copy()
            for rule in self.grammar.rules:
                if rule.lhs in current_set:
                    new_visited_non_terminals = rule.get_rhs_non_terminals()
                    current_set.update(new_visited_non_terminals)

        redundant_non_terminals.update(self.grammar.non_terminals.difference(current_set))
        self.remove_rules_with_redundant_symbols(redundant_non_terminals)

        self.generate_redundant_rules_message(list(redundant_non_terminals))

    def remove_rules_with_redundant_symbols(self, redundant_non_terminals):
        redundant_rules_indices = []
        for index, rule in enumerate(self.grammar.rules):
            rule_symbols = set(rule.get_all_rule_symbols())
            if rule_symbols.intersection(redundant_non_terminals):
                redundant_rules_indices.append(index)
        self.grammar.rules = [rule for index, rule in enumerate(self.grammar.rules)
                              if index not in redundant_rules_indices]

    def generate_redundant_rules_message(self, redundant_non_terminals):
        if len(redundant_non_terminals) == 0:
            self.messages.append("There were no redundant non-terminals.")
        elif len(redundant_non_terminals) == 1:
            self.messages.append(redundant_non_terminals[0] + " was redundant.")
        else:
            redundant_rules_str = ", ".join(redundant_non_terminals)
            self.messages.append(redundant_rules_str + " were redundant.")

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
                if self.check_is_unit_production(rule) and \
                        len((next_indices := self.grammar.find_rules_by_lhs(rule.rhs))):
                    unit_productions.append(str(rule))
                    for index in next_indices:
                        self.grammar.rules[index].lhs = rule.lhs
                    self.grammar.rules.remove(rule)
                    break
            else:
                break
        self.generate_unit_production_message(unit_productions)

    def check_is_unit_production(self, rule):
        return len(rule.rhs) == 1 and len(rule.lhs) == 1 and is_non_terminal(rule.rhs) and is_non_terminal(rule.lhs)

    def generate_unit_production_message(self, unit_productions):
        unit_productions_str = ", ".join(unit_productions)
        if len(unit_productions) == 0:
            self.messages.append("There were no unit productions.")
        elif len(unit_productions) == 1:
            self.messages.append(unit_productions_str + " was unit production.")
        else:
            self.messages.append(unit_productions_str + " were unit productions.")

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
                        next_null_rules = self.grammar.find_rules_by_rhs(prev_element)
            else:
                break
        self.generate_null_production_message(null_productions)

    def generate_null_production_message(self, null_productions):
        if len(null_productions) == 0:
            self.messages.append("There were no null productions.")
        elif len(null_productions) == 1:
            self.messages.append(null_productions[0] + " was null production.")
        else:
            null_productions_str = ", ".join(null_productions)
            self.messages.append(null_productions_str + " were null productions.")


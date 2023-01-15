from converter.util import *
from converter.Rule import Rule
import copy

EPSILON = "ε"


class Simplifier:
    def __init__(self, grammar):
        self.grammar = grammar
        self.grammar_timeline = []  # report of simplifications on grammar
        self.messages = []

    def simplify(self):
        self.add_new_start_symbol()
        self.remove_redundant_non_terminals()
        self.remove_unreachable_symbols()
        self.remove_null_productions()
        self.remove_unit_productions()

    def add_new_start_symbol(self):
        if self.check_start_symbol_is_used():
            new_start_symbol = "$"
            self.messages.append(f"'{new_start_symbol}' is now the start symbol.")
            new_rule = Rule(new_start_symbol, self.grammar.start_symbol)
            self.grammar.rules.insert(0, new_rule)
            self.grammar.non_terminals.add(new_start_symbol)
            self.grammar.start_symbol = new_start_symbol
            self.grammar_timeline.append(copy.deepcopy(self.grammar))

    def check_start_symbol_is_used(self):
        for rule in self.grammar.rules:
            if self.grammar.start_symbol in rule.get_rhs_symbols():
                return True
        return False

    """
    find non-terminals that don't generate a terminal and remove rules containing them
    """
    def remove_redundant_non_terminals(self):
        prev_set = set()
        current_set = self.grammar.terminals.copy()
        while prev_set != current_set:
            prev_set = current_set.copy()
            for rule in self.grammar.rules:
                # check if current rule derives any of current_set symbols
                rhs_current_set_intersection = [symbol for symbol in rule.get_rhs_symbols() if symbol in current_set]
                if len(rhs_current_set_intersection) > 0:
                    current_set.add(rule.lhs)

        redundant_symbols = self.grammar.non_terminals.difference(current_set)
        self.remove_rules_with_redundant_symbols(redundant_symbols)
        self.generate_redundant_non_terminals_message(list(redundant_symbols))
        self.grammar_timeline.append(copy.deepcopy(self.grammar))

    def generate_redundant_non_terminals_message(self, redundant_symbols):
        if len(redundant_symbols) == 0:
            self.messages.append("All non-terminal symbols derive a terminal symbol.")
        elif len(redundant_symbols) == 1:
            self.messages.append(redundant_symbols[0] + " does not derive a terminal symbol.")
        else:
            redundant_rules_str = ", ".join(redundant_symbols)
            self.messages.append(redundant_rules_str + " do not derive a terminal symbol.")

    """
    find symbols that are unreachable from starting symbol and remove rules containing them
    """
    def remove_unreachable_symbols(self):
        prev_set = set()
        current_set = {self.grammar.start_symbol}
        while prev_set != current_set:
            prev_set = current_set.copy()
            for rule in self.grammar.rules:
                if rule.lhs in current_set:
                    current_set.update(rule.get_all_symbols())

        all_symbols = self.grammar.non_terminals.union(self.grammar.terminals)
        unreachable_symbols = all_symbols.difference(current_set)
        self.remove_rules_with_redundant_symbols(unreachable_symbols)
        self.generate_unreachable_symbols_message(list(unreachable_symbols))
        self.grammar_timeline.append(copy.deepcopy(self.grammar))

    def generate_unreachable_symbols_message(self, redundant_symbols):
        if len(redundant_symbols) == 0:
            self.messages.append("There were no unreachable symbols.")
        elif len(redundant_symbols) == 1:
            self.messages.append(redundant_symbols[0] + " is unreachable from starting symbol.")
        else:
            redundant_rules_str = ", ".join(redundant_symbols)
            self.messages.append(redundant_rules_str + " are unreachable from starting symbol.")

    def remove_rules_with_redundant_symbols(self, redundant_symbols):
        redundant_rules_indices = []
        for index, rule in enumerate(self.grammar.rules):
            rule_symbols = set(rule.get_all_symbols())
            if rule_symbols.intersection(redundant_symbols):
                redundant_rules_indices.append(index)
        self.grammar.rules = [rule for index, rule in enumerate(self.grammar.rules)
                              if index not in redundant_rules_indices]

    """
    Unit production:
    A -> B  (A,B ∈ non-terminals)
    
    1- Add A -> x to grammar whenever B -> x occurs
    2- Delete A -> B from grammar
    """
    def remove_unit_productions(self):
        current = dict().fromkeys(self.grammar.non_terminals)
        current = {key: {key} for key in current}
        prev = dict()
        while current != prev:
            prev = copy.deepcopy(current)
            for rule in self.grammar.rules:
                if rule.is_unit_production():
                    for non_t, non_t_unit_set in current.items():
                        if rule.lhs in non_t_unit_set:
                            non_t_unit_set.add(rule.rhs)

        new_rules = []
        for non_t_a, non_t_a_unit_set in current.items():
            for non_t_b in non_t_a_unit_set:
                non_t_b_rules = self.grammar[non_t_b]
                for rule in non_t_b_rules:
                    if not rule.is_unit_production():
                        new_rule = Rule(non_t_a, rule.rhs)
                        new_rules.append(new_rule)

        unit_productions = [str(rule) for rule in self.grammar.rules if rule.is_unit_production()]
        self.grammar.rules = [rule for rule in self.grammar.rules if not rule.is_unit_production()]

        for rule in new_rules:
            if rule not in self.grammar.rules:
                self.grammar.rules.append(rule)

        self.generate_unit_production_message(unit_productions)
        self.grammar_timeline.append(copy.deepcopy(self.grammar))

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
    def remove_null_productions(self):
        nullable_non_terminals = []
        while True:
            for rule in self.grammar.rules:
                if rule.rhs == EPSILON:
                    nullable_non_terminals.append(rule.lhs)
                    if rule.lhs != self.grammar.start_symbol:
                        self.grammar.rules.remove(rule)
                    break
                # check if rhs is all non-terminals and all of them are nullable
                elif len(rule.get_rhs_symbols()) == len(rule.get_rhs_non_terminals()) and \
                        all(t in nullable_non_terminals for t in rule.get_rhs_non_terminals()):
                    nullable_non_terminals.append(rule.lhs)
                    break
            else:
                break

        for nullable_non_t in nullable_non_terminals:
            if nullable_non_t != self.grammar.start_symbol:
                self.add_new_rules_by_replacing_nullable_symbol(nullable_non_t)

        self.generate_null_production_message(nullable_non_terminals)
        self.grammar_timeline.append(copy.deepcopy(self.grammar))

    def add_new_rules_by_replacing_nullable_symbol(self, nullable_symbol):
        new_rules = []
        for rule in self.grammar.rules:
            occ_indices = [index for index, sym in enumerate(rule.get_rhs_symbols()) if sym == nullable_symbol]
            # for all combinations of occurrence indices add a new rule
            combinations = find_all_combinations_of_arr(occ_indices)
            for comb in combinations:
                new_rhs = "".join([char for ind, char in enumerate(rule.rhs) if ind not in comb])
                new_rules.append(Rule(rule.lhs, new_rhs))
        self.grammar.rules += new_rules

    def generate_null_production_message(self, nullable_non_terminals):
        if len(nullable_non_terminals) == 0:
            self.messages.append("There were no nullable non-terminals.")
        elif len(nullable_non_terminals) == 1:
            self.messages.append(nullable_non_terminals[0] + " was nullable.")
        else:
            null_productions_str = ", ".join(nullable_non_terminals)
            self.messages.append(null_productions_str + " were nullable.")


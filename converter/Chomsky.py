from converter.Converter import Converter
from converter.Rule import Rule
from converter.util import *


class Chomsky(Converter):
    def convert(self):
        if self.check_start_symbol_is_used():
            self.messages.append("'$' is now the start symbol.")
            self.grammar.rules.insert(0, Rule("$", self.grammar.start_symbol))
            self.grammar.non_terminals.add("$")

        while True:
            for rule in self.grammar.rules:
                if len(rule.rhs) == 2 and (is_terminal(rule.rhs[0]) or is_terminal(rule.rhs[1])):
                    """
                    A -> xB  converts to: A -> CB, C -> x
                    A -> Bx  converts to: A -> BC, C -> x
                    A -> xy  converts to: A -> BC, B -> x, C -> y
                    """
                    if is_terminal(rule.rhs[0]):
                        new_symbol = self.grammar.get_unused_non_terminal()
                        new_rule = Rule(new_symbol, rule.rhs[0])
                        self.grammar.rules.append(new_rule)
                        rule.rhs = new_symbol + rule.rhs[1]

                    if is_terminal(rule.rhs[1]):
                        new_symbol = self.grammar.get_unused_non_terminal()
                        new_rule = Rule(new_symbol, rule.rhs[1])
                        self.grammar.rules.append(new_rule)
                        rule.rhs = rule.rhs[0] + new_symbol

                    break

                elif len(rule.rhs) > 2:
                    """
                    A -> BCDE...L
                    converts to:
                    A -> BZ, Z -> CDE...L
                    and then:
                    A -> BZ, Z -> CX, X -> DE...L
                    and so on
                    """
                    new_symbol = self.grammar.get_unused_non_terminal()
                    new_rule = Rule(new_symbol, rule.rhs[1:])
                    rule.rhs = rule.rhs[0] + new_symbol
                    self.grammar.rules.append(new_rule)
                    break
            else:
                break

        return self.grammar

    def check_start_symbol_is_used(self):
        for rule in self.grammar.rules:
            if self.grammar.start_symbol in rule.get_rhs_symbols():
                return True
        return False

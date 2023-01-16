from converter.Converter import Converter
from converter.Rule import Rule
from converter.util import *


class Chomsky(Converter):
    def convert(self):
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

        self.sort()
        return self.grammar

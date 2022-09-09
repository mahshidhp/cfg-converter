from Converter import Converter
from Simplifier import Simplifier
from util import *


class Chomsky(Converter):
    def convert(self):
        simplifier = Simplifier(self.grammar)
        self.grammar = simplifier.simplify()
        self.messages = simplifier.messages
        return self.grammar
        if self.check_start_symbol_is_used():
            self.messages.append("'$' is now the start symbol.")
            # push to start
            self.grammar.rules.append({"lhs": "$", "rhs": "S"})
            self.grammar.non_terminals.add("$")

        while True:
            for rule in self.grammar.rules:
                if len(rule["rhs"]) == 2 and (is_terminal(rule["rhs"][0]) or is_terminal(rule["rhs"][1])):
                    """
                    A -> xB  converts to: A -> CB, C -> x
                    A -> Bx  converts to: A -> BC, C -> x
                    A -> xy  converts to: A -> BC, B -> x, C -> y
                    """
                    if is_terminal(rule["rhs"][0]):
                        new_symbol = self.grammar.get_unused_non_terminal()
                        new_rule = {"lhs": new_symbol, "rhs": rule["rhs"][0]}
                        self.grammar.rules.append(new_rule)
                        rule["rhs"] = new_symbol + rule["rhs"][1]

                    if is_terminal(rule["rhs"][1]):
                        new_symbol = self.grammar.get_unused_non_terminal()
                        new_rule = {"lhs": new_symbol, "rhs": rule["rhs"][1]}
                        self.grammar.rules.append(new_rule)
                        rule["rhs"] = rule["rhs"][0] + new_symbol

                    break

                elif len(rule["rhs"]) > 2:
                    """
                    A -> BCDE..L
                    converts to:
                    A -> BZ, Z -> CDE...L
                    and then:
                    A -> BZ, Z -> CX, X -> DE...L
                    and so on
                    """
                    new_symbol = self.grammar.get_unused_non_terminal()
                    new_rule = {"lhs": new_symbol, "rhs": rule["rhs"][1:]}
                    rule["rhs"] = rule["rhs"][0] + new_symbol
                    self.grammar.rules.append(new_rule)
                    break
            else:
                break

        return self.grammar

    def check_start_symbol_is_used(self):
        for rule in self.grammar.rules:
            if "S" in rule["rhs"]:
                return True
        return False

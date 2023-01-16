from abc import ABC, abstractmethod
from converter.Simplifier import Simplifier


class Converter(ABC):
    def __init__(self, grammar, should_simplify=True):
        if should_simplify:
            self.simplifier = Simplifier(grammar)
            self.simplifier.simplify()
            self.grammar = self.simplifier.grammar
        else:
            self.grammar = grammar

    @abstractmethod
    def convert(self):
        pass

    def sort(self):
        dollar_production = self.grammar["$"]
        s_productions = self.grammar["S"]
        other_productions = [rule for rule in self.grammar.rules if rule not in dollar_production + s_productions]
        self.grammar.rules = dollar_production + s_productions + other_productions


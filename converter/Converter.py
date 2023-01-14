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

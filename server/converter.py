from abc import ABC, abstractmethod


class Converter(ABC):
    def __init__(self, grammar):
        self.grammar = grammar
        self.messages = []

    @abstractmethod
    def convert(self):
        pass

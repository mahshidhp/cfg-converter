from chomsky import Chomsky
from converter import Converter


class Greibach(Converter):

    def convert(self):
        chomsky_converter = Chomsky(self.grammar)
        self.grammar = chomsky_converter.convert()
        self.messages = chomsky_converter.messages

        mapping = dict.fromkeys(self.grammar.non_terminals)

        for i in range(len(self.grammar.rules)):
            rule = self.grammar.rules[i]

        return self.grammar

    def remove_left_recursion(self):
        pass

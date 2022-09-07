from chomsky import Chomsky
from converter import Converter


class Greibach(Converter):
    def convert(self):
        chomsky_converter = Chomsky(self.grammar)
        self.grammar = chomsky_converter.convert()
        self.messages = chomsky_converter.messages



        return self.grammar


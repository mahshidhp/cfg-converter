import json
import copy
from converter.Grammar import Grammar
from converter.Parser import Parser


if __name__ == "__main__":
    rules_arr = json.loads(open("./sample_grammars.json", "r").read())
    texts = ["ab", "x + x * x"]
    for i, rules in enumerate(rules_arr):
        grammar = Grammar(copy.deepcopy(rules))
        Parser(grammar, texts[i]).parse()

import copy
import json
import random
from converter.Grammar import Grammar
from converter.Chomsky import Chomsky
from converter.Greibach import Greibach

CHOMSKY = 1
GREIBACH = 2

colors = ['\033[95m', '\033[94m', '\033[96m', '\033[92m', '\033[93m', '\033[91m']
END_COLOR = '\033[0m'
CURRENT_COLOR = ""


def print_colored(text):
    print(CURRENT_COLOR + text + END_COLOR)


def print_pretty_rules(title, grammar):
    print_colored(title)
    for rule in grammar.rules:
        print_colored(str(rule))
    print_colored("--------------------------------")


def test(grammar, conversion_form):
    global CURRENT_COLOR
    CURRENT_COLOR = random.choice(colors)
    print_pretty_rules("input grammar", grammar)
    converter = None
    if conversion_form == CHOMSKY:
        converter = Chomsky(grammar)
    elif conversion_form == GREIBACH:
        converter = Greibach(grammar)
    converter.convert()
    # print result
    simplified_hist = converter.simplifier.grammar_timeline
    simplifier_msg = converter.simplifier.messages
    for i in range(len(simplified_hist)):
        print_pretty_rules(simplifier_msg[i], simplified_hist[i])
    print_pretty_rules("RESULT\n"+"\n".join(converter.messages), converter.grammar)
    print("***********************************************************************")


if __name__ == "__main__":
    rules_arr = json.loads(open("./sample_grammars.json", "r").read())
    for rules in rules_arr:
        grammar = Grammar(copy.deepcopy(rules))
        test(grammar, CHOMSKY)
        grammar = Grammar(copy.deepcopy(rules))
        test(grammar, GREIBACH)

import random

from converter.Parser import Parser


class TestcaseGenerator:
    def __init__(self, grammar1, grammar2):
        self.grammar1 = grammar1
        self.grammar2 = grammar2

    def generate(self, count):
        acc_by_grammar1 = self.grammar1.generate_example_words(count)
        rej_by_grammar2 = self.generate_unacceptable_words_from_grammar2(count)
        acc_by_grammar2 = self.filter_acceptable_words_for_grammar2(acc_by_grammar1)
        rej_by_grammar1 = self.filter_unacceptable_words_for_grammar1(rej_by_grammar2)
        return [acc_by_grammar1, rej_by_grammar1, acc_by_grammar2, rej_by_grammar2]

    def generate_unacceptable_words_from_grammar2(self, count):
        terminals = list(self.grammar2.terminals)
        if 'ε' in terminals:
            terminals.remove('ε')

        unacceptable_words = []
        while len(unacceptable_words) < count:
            random_word_length = random.randint(2, 10)
            random_word = "".join([random.choice(terminals) for _ in range(random_word_length)])
            is_acceptable = Parser(self.grammar2, random_word).parse()
            if not is_acceptable and random_word not in unacceptable_words:
                unacceptable_words.append(random_word)

        return unacceptable_words

    def filter_acceptable_words_for_grammar2(self, acc_by_grammar1):
        acc_by_grammar2 = []
        for word in acc_by_grammar1:
            is_acceptable = Parser(self.grammar2, word).parse()
            acc_by_grammar2.append(word if is_acceptable else None)
        return acc_by_grammar2

    def filter_unacceptable_words_for_grammar1(self, rej_by_grammar2):
        rej_by_grammar1 = []
        for word in rej_by_grammar2:
            is_acceptable = Parser(self.grammar1, word).parse()
            rej_by_grammar1.append(word if not is_acceptable else None)
        return rej_by_grammar1

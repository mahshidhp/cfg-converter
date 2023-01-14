from converter.Rule import Rule
from converter.util import *


class State:
    def __init__(self, rule, dot_index, start_column):
        self.rule = rule
        self.dot_index = dot_index
        self.start_column = start_column
        self.end_colum = None

    def completed(self):
        return self.dot_index >= len(self.rule.rhs)

    def next_term(self):
        if self.completed():
            return None
        return self.rule.rhs[self.dot_index]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        rhs = self.rule.get_rhs_symbols()
        rhs.insert(self.dot_index, "$")
        rhs = " ".join(rhs)
        return "%-5s -> %-20s  [%s, %s]" % (self.rule.lhs, rhs, self.start_column, self.end_colum)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.rule, self.dot_index, self.start_column) == (other.rule, other.dot_index, other.start_column)

    def __ne__(self, other):
        return not (self == other)


class Column:
    def __init__(self, index, token):
        self.index = index
        self.token = token
        self.states = []

    def add(self, state):
        if state not in self.states:
            state.end_colum = self
            self.states.append(state)
            return True
        return False

    def print(self):
        print(f'col no {self.index} - token: {self.token}')
        print("--------------------------------------------")
        for state in self:
            # if state.completed():
            print(state)
        print()

    def __str__(self):
        return f'#{self.index}'

    def __iter__(self):
        return iter(self.states)


class Parser:
    def __init__(self, grammar, text):
        self.grammar = grammar
        self.text = text
        tokens = [token for token in list(text) if not token.isspace()]
        self.table = [Column(i, tok) for i, tok in enumerate([None] + tokens)]

    def parse(self):
        start_sym = self.grammar.start_symbol
        self.table[0].add(State(rule=Rule("%", start_sym), dot_index=0, start_column=self.table[0]))

        for i in range(0, len(self.table)):
            col = self.table[i]
            for state in col:
                if state.completed():
                    self.complete(col, state)
                else:
                    term = state.next_term()
                    if is_non_terminal(term):
                        self.predict(col, state)
                    elif is_terminal(term) and i+1 < len(self.table):
                        next_col = self.table[i+1]
                        self.scan(next_col, state, term)

            # self.handle_epsilon(col)
            self.table[i].print()

        for state in self.table[-1]:
            if state.rule.lhs == "%" and state.completed() and state.start_column is self.table[0]:
                root = state
                return True
        else:
            return False

    def predict(self, col, state):
        term = state.next_term()
        if is_terminal(term):
            return
        rules = self.grammar[term]
        for rule in rules:
            new_state = State(rule, 0, col)
            col.add(new_state)

    def scan(self, next_col, state, term):
        if term == next_col.token:
            new_state = State(rule=state.rule, dot_index=state.dot_index+1, start_column=state.start_column)
            next_col.add(new_state)

    def complete(self, col, state):
        if not state.completed():
            return
        for state2 in state.start_column:
            t = state2.next_term()
            if t and is_non_terminal(t) and t == state.rule.lhs:
                st3 = State(rule=state2.rule, dot_index=state2.dot_index+1, start_column=state2.start_column)
                col.add(st3)

    def handle_epsilon(self, col):
        changed = True
        while changed:
            changed = False
            for state in col:
                if self.complete(col, state):
                    changed = True
                self.predict(col, state)

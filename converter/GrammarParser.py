from converter.Rule import Rule


start_symbol = 'S'


class EarleyState(object):
    """
    Represents a state in the Earley algorithm.
    """

    GAM = '<GAM>'

    def __init__(self, rule, dot=0, sent_pos=0, chart_pos=0, back_pointers=[]):
        self.rule = rule
        self.dot = dot
        self.sent_pos = sent_pos
        self.chart_pos = chart_pos
        self.back_pointers = back_pointers

    def __eq__(self, other):
        if type(other) is EarleyState:
            return self.rule == other.rule and self.dot == other.dot and \
                   self.sent_pos == other.sent_pos

        return False

    def __len__(self):
        return len(self.rule)

    def __repr__(self):
        return self.__str__()

    def str_helper(self):
        return ('(' + self.rule.lhs + ' -> ' +
                self.rule.rhs[:self.dot] + '*' + self.rule.rhs[self.dot:] +
                (', [%d, %d])' % (self.sent_pos, self.chart_pos)))

    def __str__(self):
        return self.str_helper() + \
               ' (' + \
               ', '.join(s.str_helper() for s in self.back_pointers) +\
               ')'

    def next(self):
        """
        Return next symbol to parse, i.e. the one after the dot
        """
        if self.dot < len(self):
            return self.rule[self.dot]

    def is_complete(self):
        """
        Checks whether the given state is complete.
        """
        return len(self) == self.dot

    @staticmethod
    def init():
        """
        Returns the state used to initialize the chart in the Earley algorithm.
        """
        return EarleyState(Rule(EarleyState.GAM, [start_symbol]))


class ChartEntry(object):
    """
    Represents an entry in the chart used by the Earley algorithm.
    """

    def __init__(self, states):
        self.states = states

    def __iter__(self):
        return iter(self.states)

    def __len__(self):
        return len(self.states)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '\n'.join(str(s) for s in self.states)

    def add(self, state):
        """
        Add the given state (if it hasn't already been added).
        """
        if state not in self.states:
            self.states.append(state)


class Chart(object):
    """
    Represents the chart used in the Earley algorithm.
    """

    def __init__(self, entries):
        # List of chart entries.
        self.entries = entries

    def __getitem__(self, i):
        return self.entries[i]

    def __len__(self):
        return len(self.entries)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '\n\n'.join([("Chart[%d]:\n" % i) + str(entry) for i, entry in enumerate(self.entries)])

    @staticmethod
    def init(length):
        """
        Initializes a chart with l entries (Including the dummy start state).
        """
        return Chart([(ChartEntry([]) if i > 0 else ChartEntry([EarleyState.init()])) for i in range(length)])


class EarleyParser(object):
    """
    Represents the Earley-generated parse for a given sentence according to a
    given grammar.
    """

    def __init__(self, input_str, grammar):
        self.letters = list(input_str)
        self.grammar = grammar
        global start_symbol
        start_symbol = self.grammar.start_symbol
        self.chart = Chart.init(len(self.letters) + 1)

    def run(self):
        self.parse()
        output = self.get()
        print(output)
        return output

    def predictor(self, state, pos):
        """
        Earley Predictor.
        """
        for rule in self.grammar[state.next()]:
            self.chart[pos].add(EarleyState(rule, dot=0, sent_pos=state.chart_pos, chart_pos=state.chart_pos))

    def scanner(self, state, pos):
        """
        Earley Scanner.
        """
        if state.chart_pos < len(self.letters):
            word = self.letters[state.chart_pos]

            if any((word in r) for r in self.grammar[state.next()]):
                self.chart[pos + 1].add(EarleyState(Rule(state.next(),
                                                    [word]),
                                                    dot=1,
                                                    sent_pos=state.chart_pos,
                                                    chart_pos=(state.chart_pos + 1)))

    def completer(self, state, pos):
        """
        Earley Completer.
        """

        for prev_state in self.chart[state.sent_pos]:
            if prev_state.next() == state.rule.lhs:
                self.chart[pos].add(EarleyState(prev_state.rule,
                                                dot=(prev_state.dot + 1),
                                                sent_pos=prev_state.sent_pos,
                                                chart_pos=pos,
                                                back_pointers=(prev_state.back_pointers + [state])))

    def parse(self):
        """
        Parses the sentence by running the Earley algorithm and filling out the
        chart.
        """

        # Checks whether the next symbol for the given state is a tag.
        def is_tag(state):
            return self.grammar.is_tag(state.next())

        for i in range(len(self.chart)):
            for state in self.chart[i]:
                if not state.is_complete():
                    if is_tag(state):
                        self.scanner(state, i)
                    else:
                        self.predictor(state, i)
                else:
                    self.completer(state, i)

    def has_parse(self):
        """
        Checks whether the sentence has a parse.
        """

        for state in self.chart[-1]:
            if state.is_complete() and state.rule.lhs == self.grammar.start_symbol and \
                    state.sent_pos == 0 and state.chart_pos == len(self.letters):
                return True

        return False

    def get(self):
        """
        Returns the parse if it exists, otherwise returns None.
        """

        for state in self.chart[-1]:
            if state.is_complete() and state.rule.lhs == self.grammar.start_symbol and \
                    state.sent_pos == 0 and state.chart_pos == len(self.letters):
                return True
        return False

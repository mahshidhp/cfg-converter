import itertools


def is_terminal(char):
    return char.islower() or char in list('ε!*+-/,;:"\'')


def is_non_terminal(char):
    return char.isupper() or char == '$'


def find_all_combinations_of_arr(arr):
    combinations = []
    for i in range(1, len(arr) + 1):
        combinations += list(itertools.combinations(arr, i))
    return combinations

def is_terminal(char):
    return char.islower()


def is_non_terminal(char):
    return char.isupper() or char == '$'

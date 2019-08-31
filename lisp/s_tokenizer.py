"""
S-expression tokenizer.
Converts a string to a list of LISP tokens.
"""


def tokenize(s):
    """
    >>> list(tokenize('()'))
    ['(', ')']

    >>> list(tokenize('foo'))
    ['foo']

    >>> list(tokenize('(foo)'))
    ['(', 'foo', ')']

    >>> list(tokenize('(foo bar)'))
    ['(', 'foo', 'bar', ')']

    >>> list(tokenize('(cdr (quote (a b c)))'))
    ['(', 'cdr', '(', 'quote', '(', 'a', 'b', 'c', ')', ')', ')']
    """
    start = None
    for i, c in enumerate(s):
        if c in [' ', '\t', '\r', '\n']:
            if start is not None:
                yield s[start:i]
                start = None
        elif c in ['(', ')']:
            if start is not None:
                yield s[start:i]
                start = None
            yield c
        else:
            if start is None:
                start = i
    if start is not None:
        yield s[start:]

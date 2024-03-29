from symbol import Symbol
from cons import Cons
"""
Parser for LISP s-expressions
"""


def parse(s):
    """
    parse s-expression string into atom or nested atom tuple
    >>> parse('()')
    NIL

    >>> parse('(foo)')
    (FOO)

    >>> parse('(foo bar)')
    (FOO BAR)

    >>> parse('((foo))')
    ((FOO))

    >>> parse('(cdr (cons (quote a) (quote (b c))))')
    (CDR (CONS (QUOTE A) (QUOTE (B C))))

    >>> parse('t')
    T

    >>> parse('(a) b')
    Traceback (most recent call last):
    ValueError: extra stuff:['b']
    """
    t = _Tokens(s)
    ret = t.parse_expr(True)
    if len(t) != 0:
        raise ValueError('extra stuff:' + str(t))
    return ret


class _Tokens():
    def __init__(self, s):
        self.tokens = list(tokenize(s))

    def __len__(self):
        return len(self.tokens)

    def __repr__(self):
        return repr(self.tokens)

    def head(self):
        return self.tokens[0]

    def _next(self):
        self.tokens = self.tokens[1:]

    def _close(self):
        if self.tokens[0] != ')':
            ValueError('not found ")"')
        self._next()

    def parse_expr(self, first=False):
        if self.head() == '(':
            self._next()
            ret = self.parse_etuple()
            self._close()
            return ret
        elif self.head() == ')':
            raise ValueError('unmatched ")"')
        else:
            if first:
                ret = Symbol(self.head())  # <---<< symbol
                self._next()
                return ret
            raise ValueError('extra stuff after expression: ' + str(self.tokens))

    def parse_etuple(self):
        if self.head() == '(':
            self._next()
            car = self.parse_etuple()
            self._close()
            return Cons(car, self.parse_etuple())  # <---<< cons
        elif self.head() == ')':
            return Symbol.NIL  # <---<< empty list
        else:
            car = Symbol(self.head())
            self._next()
            return Cons(car, self.parse_etuple())  # <---<< cons


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

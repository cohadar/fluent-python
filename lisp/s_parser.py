"""
Parser and unparser for LISP s-expressions
"""


def parse(s):
    """
    parse s-expression string into nested atom tuple
    >>> parse('()')
    ()

    >>> parse('(foo)')
    ('foo',)

    >>> parse('(foo bar)')
    ('foo', 'bar')

    >>> parse('((foo))')
    (('foo',),)

    >>> parse('(cdr (cons (quote a) (quote (b c))))')
    ('cdr', ('cons', ('quote', 'a'), ('quote', ('b', 'c'))))
    """
    return _Tokens(s).parse_expr()


def unparse(e):
    """
    convert nested atom tuple to s-expression string
    >>> unparse(())
    '()'

    >>> unparse(('foo',))
    '(foo)'

    >>> unparse(('foo', 'bar'))
    '(foo bar)'

    >>> unparse((('foo',),))
    '((foo))'

    >>> unparse(('cdr', ('cons', ('quote', 'a'), ('quote', ('b', 'c')))))
    '(cdr (cons (quote a) (quote (b c))))'
    """
    assert e is not None
    if isinstance(e, str):
        return e
    else:
        return "({})".format(" ".join([unparse(v) for v in e]))


class _Tokens():
    def __init__(self, s):
        self.tokens = list(tokenize(s))
        self.tokens.append('(EOL)')

    def head(self):
        return self.tokens[0]

    def _next(self):
        self.tokens = self.tokens[1:]

    def _close(self):
        if self.tokens[0] != ')':
            ValueError('not found ")"')
        self._next()

    def parse_expr(self):
        if self.head() == '(':
            self._next()
            return self.parse_etuple()
        elif self.head() == ')':
            raise ValueError('unmatched ")"')
        elif self.head() == '(EOL)':
            raise ValueError('premature EOL')
        else:
            if len(self.tokens) > 1:
                raise ValueError('extra stuff after expression')
            return self.head()

    def parse_etuple(self):
        if self.head() == '(':
            self._next()
            ret = (self.parse_etuple(),)
            self._close()
            return ret + self.parse_etuple()
            return ret
        elif self.head() == ')':
            return tuple()
        elif self.head() == '(EOL)':
            raise ValueError('premature EOL')
        else:
            ret = (self.head(),)
            self._next()
            return ret + self.parse_etuple()


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

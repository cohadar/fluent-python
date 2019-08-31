"""
Parser and unparser for LISP s-expressions.
Converts a text to a series of nested string collections.
"""
from s_tokenizer import tokenize


def parse(s, coltype):
    """
    parse s-expression string into atom or nested atom tuple
    >>> parse('()', tuple)
    ()
    >>> parse('()', list)
    []

    >>> parse('(foo)', tuple)
    ('foo',)
    >>> parse('(foo)', list)
    ['foo']

    >>> parse('(foo bar)', tuple)
    ('foo', 'bar')
    >>> parse('(foo bar)', list)
    ['foo', 'bar']

    >>> parse('((foo))', tuple)
    (('foo',),)
    >>> parse('((foo))', list)
    [['foo']]

    >>> parse('(cdr (cons (quote a) (quote (b c))))', tuple)
    ('cdr', ('cons', ('quote', 'a'), ('quote', ('b', 'c'))))
    >>> parse('(cdr (cons (quote a) (quote (b c))))', list)
    ['cdr', ['cons', ['quote', 'a'], ['quote', ['b', 'c']]]]

    >>> parse('t', tuple)
    't'
    >>> parse('t', list)
    't'

    >>> parse('(a) b', tuple)
    Traceback (most recent call last):
    ValueError: extra stuff:['b']
    >>> parse('(a) b', list)
    Traceback (most recent call last):
    ValueError: extra stuff:['b']
    """
    t = _Tokens(s)
    ret = t.parse_expr(coltype, True)
    if len(t) != 0:
        raise ValueError('extra stuff:' + str(t))
    return ret


def unparse(e):
    """
    convert atom or nested atom tuple to s-expression string
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

    >>> unparse('t')
    't'
    """
    assert e is not None
    if isinstance(e, str):
        return e
    else:
        return "({})".format(" ".join([unparse(v) for v in e]))


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

    def parse_expr(self, coltype, first=False):
        if self.head() == '(':
            self._next()
            ret = self.parse_collection(coltype)
            self._close()
            return ret
        elif self.head() == ')':
            raise ValueError('unmatched ")"')
        else:
            if first:
                ret = self.head()
                self._next()
                return ret
            raise ValueError('extra stuff after expression: ' + str(self.tokens))

    def parse_collection(self, coltype):
        if self.head() == '(':
            self._next()
            ret = []
            ret.append(self.parse_collection(coltype))
            ret = coltype(ret)
            self._close()
            return ret + self.parse_collection(coltype)
        elif self.head() == ')':
            return coltype()
        else:
            ret = []
            ret.append(self.head())
            ret = coltype(ret)
            self._next()
            return ret + self.parse_collection(coltype)

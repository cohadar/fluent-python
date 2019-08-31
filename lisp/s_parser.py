"""
Parser and unparser for LISP s-expressions
Converts a text to a series
"""
from s_tokenizer import tokenize


def parse(s, collection=tuple):
    """
    parse s-expression string into atom or nested atom tuple
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

    >>> parse('t')
    't'

    >>> parse('(a) b')
    Traceback (most recent call last):
    ValueError: extra stuff:['b']
    """
    t = _Tokens(s)
    ret = t.parse_expr(collection, True)
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

    def parse_expr(self, collection, first=False):
        if self.head() == '(':
            self._next()
            ret = self.parse_collection(collection)
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

    def parse_collection(self, collection):
        if self.head() == '(':
            self._next()
            ret = []
            ret.append(self.parse_collection(collection))
            ret = collection(ret)
            self._close()
            return ret + self.parse_collection(collection)
        elif self.head() == ')':
            return collection()
        else:
            ret = []
            ret.append(self.head())
            ret = collection(ret)
            self._next()
            return ret + self.parse_collection(collection)

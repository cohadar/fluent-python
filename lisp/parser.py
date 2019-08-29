"""
Parser for LISP s expressions, returns nested lists of with string atoms

>>> parse('()')
[]

>>> parse('(foo)')
['foo']

>>> parse('(foo bar)')
['foo', 'bar']

>>> parse('((foo))')
[['foo']]

>>> parse('(cdr (cons (quote a) (quote (b c))))')
['cdr', ['cons', ['quote', 'a'], ['quote', ['b', 'c']]]]
"""


def parse(s):
    return Tokens(s).parse_expr()


class Tokens():
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
            return self.parse_elist()
        elif self.head() == ')':
            raise ValueError('unmatched ")"')
        elif self.head() == '(EOL)':
            raise ValueError('premature EOL')
        else:
            if len(self.tokens) > 1:
                raise ValueError('extra stuff after expression')
            return self.head()

    def parse_elist(self):
        if self.head() == '(':
            self._next()
            ret = [self.parse_elist()]
            self._close()
            ret.extend(self.parse_elist())
            return ret
        elif self.head() == ')':
            return []
        elif self.head() == '(EOL)':
            raise ValueError('premature EOL')
        else:
            ret = [self.head()]
            self._next()
            ret.extend(self.parse_elist())
            return ret


def tokenize(s):
    """
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

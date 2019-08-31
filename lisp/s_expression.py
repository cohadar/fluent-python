class S():
    """
    Class representing LISP S-expressions
    """
    def __init__(self, data=None):
        """
        constructor takes None or a string or an iterable containing only
        strings or other S-expressions.
        >>> S()._data
        ()
        >>> S('foo')._data
        'foo'
        >>> S(())._data
        ()
        >>> s = S(('foo', S('bar'))); s._data[0]; s._data[1]._data
        'foo'
        'bar'
        """
        if data is None:
            self._data = ()
        elif isinstance(data, str):
            assert data.find('(') == -1
            assert data.find(')') == -1
            self._data = data
        else:
            self._data = tuple(data)
            for x in self._data:
                assert isinstance(x, str) or isinstance(x, S)

    def __repr__(self):
        """
        print S-expressions in canonical form
        >>> S()
        ()
        >>> S('foo')
        foo
        >>> S(('foo', 'bar'))
        (foo bar)
        >>> S(('foo', S(('aaa', 'bbb')), 'bar'))
        (foo (aaa bbb) bar)
        """
        if self._data is None:
            return '()'
        elif isinstance(self._data, str):
            return self._data
        else:
            return "({})".format(" ".join([str(v) for v in self._data]))

    def isNil(self):
        return self._data == ()

    def isVariable(self):
        return isinstance(self._data, str)

    def isAtom(self):
        return self.isNil() or self.isVariable()

    def __iter__(self):
        assert not self.isVariable()
        return iter(self._data)

    def __getitem__(self, i):
        return self._data[i]

    def __eq__(self, other):
        if isinstance(self._data, str):
            return self._data == other._data
        else:
            return id(self._data) == id(other._data)

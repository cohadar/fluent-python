"""
klasa koja predstavlja s-expression
i lista i sam string su s-expression

interni data da je ili str ili nested tuple S expressiona

da ima fromStrTuple method koji prihvata izlaz parsera i vraća S kao prelazno
rešenje.
Prvo vidi kako će da se uklopi u eval, a onda napravi direktan parser za S

ima lep quote handling

ima isAtom, isNil i __eq__ __hash__ implementirano, 
kao i razne potrebne konstruktore i __iter__
"""


class S():
    """
    LISP S-expression.
    Wrapper around str and tuple
    """
    def __init__(self, data=None):
        """
        >>> S()._data
        ()
        >>> S('foo')._data
        'foo'
        >>> S(())._data
        ()
        >>> S(('foo',))._data
        ('foo',)
        >>> S(('foo','bar'))._data
        ('foo', 'bar')
        >>> S(('foo', ('aa', 'bb'), 'bar'))._data
        ('foo', ('aa', 'bb'), 'bar')
        >>> S(55)._data
        Traceback (most recent call last):
        AssertionError: '55' must be str or tuple, not '<class 'int'>'
        >>> S(('foo', ('a', 'b', ('x', [], 'y'), 'bar')))._data
        Traceback (most recent call last):
        AssertionError: '[]' must be str or tuple, not '<class 'list'>'
        """
        if data is None:
            data = ()
        S._validate(data)
        self._data = data

    @staticmethod
    def _validate(data):
        if isinstance(data, str):
            return True
        elif isinstance(data, tuple):
            return all((S._validate(el) for el in data))
        else:
            assert False, "'{}' must be str or tuple, not '{}'".format(data, type(data))

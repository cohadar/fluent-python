
class Njak():
    def __init__(self, d=None):
        """
        >>> d = {}; d; \
            n = Njak(); n
        {}
        Njak{}
        >>> d = dict({'aa': 33, 'bb':444}); d; \
            n = Njak({'aa': 33, 'bb':444}); n
        {'aa': 33, 'bb': 444}
        Njak{'aa': 33, 'bb': 444}
        >>> d = Njak({'aa': 33, 'bb':444}); \
            n = Njak(d); n
        Njak{'aa': 33, 'bb': 444}
        """
        if d is None:
            d = {}
        if isinstance(d, Njak):
            self._dict = d._dict
        else:
            self._dict = dict(d)

    def __getitem__(self, key):
        """
        >>> n = Njak({'aa': 33, 'bb':444}); n['aa']; n['bb']
        33
        444
        """
        return self._dict[key]

    def __setitem__(self, key, value):
        """
        >>> n = Njak({'aa': 33, 'bb':444}); n['aa'] = 5; n
        Njak{'aa': 5, 'bb': 444}
        """
        self._dict[key] = value

    def update(self, other):
        """
        >>> n = Njak({'aa': 33, 'bb':444}); n.update({'bb': 123, 'cc': 7}); n
        Njak{'aa': 33, 'bb': 123, 'cc': 7}
        >>> n = Njak({'aa': 33, 'bb':444}); n.update(Njak({'bb': 123, 'cc': 7})); n
        Njak{'aa': 33, 'bb': 123, 'cc': 7}
        """
        if other is None:
            other = {}
        if isinstance(other, Njak):
            self._dict.update(other._dict)
        else:
            self._dict.update(dict(other))

    def __repr__(self):
        return 'Njak' + repr(self._dict)

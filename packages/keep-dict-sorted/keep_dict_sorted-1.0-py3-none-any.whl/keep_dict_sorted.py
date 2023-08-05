#
##
##  SPDX-FileCopyrightText: © 2007-2023 Benedict Verhegghe <bverheg@gmail.com>
##  SPDX-License-Identifier: GPL-3.0-or-later
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see http://www.gnu.org/licenses/.
##
"""Keep dict sorted

This module defines the ODict class, an ordered dict with sorting capabilities.
Odict derives from dict, but keeps the items in the dict ordered according to
the provided sortkey.

Examples
--------
The default ODict works like the Python dict: the items in the dict
are returned in order of insertion.

>>> D = ODict({'a':0, 'c':1, 'b':3, 'd':2})  # insertion order
>>> print(D)
{'a': 0, 'c': 1, 'b': 3, 'd': 2}

With sortkey='key', items are kept sorted on the keys. Only use
this if you know that the keys can be sorted.

>>> D = ODict({'a':0, 'c':1, 'b':3, 'd':2}, sortkey='key')
>>> print(D)
{'a': 0, 'b': 3, 'c': 1, 'd': 2}

Add some new item:

>>> D['aa'] = 5
>>> print(D)
{'a': 0, 'aa': 5, 'b': 3, 'c': 1, 'd': 2}

Let's sort on the values instead:

>>> D = ODict({'a':0, 'c':1, 'b':3, 'd':2}, sortkey='value')
>>> print(D)
{'a': 0, 'c': 1, 'd': 2, 'b': 3}

Add another item:

>>> D['c'] = 4
>>> print(D)
{'a': 0, 'd': 2, 'b': 3, 'c': 4}

Add/update multiple items:

>>> D.update({'e':3, 'a':5})
>>> print(D)
{'d': 2, 'b': 3, 'e': 3, 'c': 4, 'a': 5}

In what position is the item with key 'b'?

>>> D.index('b')
1

Get and remove the item at postion 2:

>>> D.popitem(2)
('e', 3)
>>> D
ODict({'d': 2, 'b': 3, 'c': 4, 'a': 5})

Change the sorting key to the distance of the value from
the value 3:

>>> D.set_sortkey(lambda key: abs(D[key] - 3))
>>> print(D)
{'b': 3, 'd': 2, 'c': 4, 'a': 5}

"""


class ODict(dict):
    """An ordered dict with sorting capabilities.

    This is a dictionary that keeps the keys in order of insertion or
    in order of a provided sortkey function.

    Parameters
    ----------
    data:
        Any data that can initialize a dict
    sortkey: None | str | callable
        Defines how the keys are kept sorted: None will keep the default dict
        insertion order. 'key' will keep the keys sorted (the keys should be
        sortable). 'value' will keep the values sorted (again, make sure they
        are sortable). A callable will be used as the sortkey argument in
        sorting the list of keys.

    """
    def __init__(self, data={}, sortkey=None):
        """Create a new ODict instance."""
        dict.__init__(self, data)
        if isinstance(data, ODict):
            self._order = data._order
        elif isinstance(data, dict):
            self._order = list(data.keys())
        elif isinstance(data, (list, tuple)):
            self._order = []
            self._add_keys([i[0] for i in data])
        else:
            raise ValueError("Invalid data for ODict")
        self.set_sortkey(sortkey)

    def set_sortkey(self, sortkey):
        """Set the sort key

        - 'key': sorts on the keys
        - 'value': sorts on the values
        - callable: used as key in sorting
        - None: keeps the insertion order

        Examples
        --------
        >>> d = ODict(dict.fromkeys(['aaa', 'a', 'aa']))
        >>> print(d.keys())
        ['aaa', 'a', 'aa']
        >>> d.set_sortkey(lambda key:len(key))
        >>> print(d.keys())
        ['a', 'aa', 'aaa']
        """
        if sortkey == 'key':
            self.sortkey = lambda key: key
        elif sortkey == 'value':
            self.sortkey = lambda key: self[key]
        elif callable(sortkey):
            self.sortkey = sortkey
        else:
            self.sortkey = None
        self._sortkeys()

    def _sortkeys(self):
        if self.sortkey:
            self._order.sort(key=self.sortkey)

    def _add_keys(self, keys):
        """Add a list of keys to the ordered list, removing existing keys."""
        for key in keys:
            if key in self._order:
                self._order.remove(key)
        self._order += keys
        self._sortkeys()

    def clear(self):
        """Remove all items from the ODict"""
        dict.clear(self)
        self._order = []

    def copy(self):
        """Return a shallow copy of self"""
        return self.__class__(self, sortkey=self.sortkey)

    def update(self, data={}):
        """Add a dictionary to the ODict object.

        The values of other take precedence. If data is another ODict,
        sorting is according to self.
        """
        dict.update(self, data)
        self._add_keys(ODict(data)._order)

    def __ior__(self,other):
        """Allows d.update(other) to be written as d |= other"""
        self.update(other)

    def __or__(self, other):
        """New dictionary with merged values from self and other"""
        return self.copy().update(other)

    def __iter__(self):
        return self._order.__iter__()

    def __str__(self):
        return '{' + ', '.join(f"{k!r}: {self[k]!r}" for k in self) + '}'

    def __repr__(self):
        return f"ODict({self})"

    def __setitem__(self,key,value):
        """Allows items to be set using self[key] = value."""
        dict.__setitem__(self,key,value)
        if key not in self._order:
            self._order.append(key)
        self._sortkeys()

    def __delitem__(self,key):
        """Allow items to be deleted using del self[key]."""
        dict.__delitem__(self,key)
        self._order.remove(key)

    def __add__(self,data):
        """Add two ODicts's together, returning the result."""
        self.update(data)
        return self

    def keys(self):
        """Return the keys in order."""
        return self._order

    def values(self):
        """Return the values in order of the keys."""
        return [self[k] for k in self._order]

    def items(self):
        """Iterate over key,value pairs in order of the keys."""
        for k in self:
            yield k,self[k]

    def index(self, key):
        """Return the current position of the specified key."""
        return self._order.index(key)

    def pop(self, key, default=None):
        if key in self:
            self._order.remove(key)
            val = self.pop(key)
        else:
            if default is not None:
                val = default
            else:
                raise KeyError(key)
        return val

    def popitem(self, index=-1):
        """Remove the item at position index"""
        key = self._order[index]
        item = (key, self[key])
        del self[key]
        return item

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        elif default is not None:
            self[key] = default
            return default


# End

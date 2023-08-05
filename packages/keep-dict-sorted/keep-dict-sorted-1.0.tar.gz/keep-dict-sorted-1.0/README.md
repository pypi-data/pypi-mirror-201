# Keep Dict Sorted

This package contains the ODict class, which is an ordered dict with the
capability to keep the items sorted not only in insertion order, but in any
order that can be achieved by sorting. Typically this can be sorted on the
keys or on the values, but a general sort key function is also possible.

## Documentation

Just a small example, with items sorted on the values:
```python
from keep_dict_sorted import ODict
D = ODict({'a':0, 'c':1, 'b':3, 'd':2}, sortkey='value')
print(D)  # {'a': 0, 'c': 1, 'd': 2, 'b': 3}
# now change a value:
D['c'] = 4
print(D)  # {'a': 0, 'd': 2, 'b': 3, 'c': 4}
```
For more: see the docstring of the keep_dict_sorted module and the ODict class.

## History

Back in the old times the [pyFormex project](https:pyformex.org) had its
own ordered dict with the capability to sort the items on request. After
Python's default dict became ordered, it was dropped from pyFormex as its
applications could easily be got with a plane dict and sorting comprehensions.
Triggered by a recent discussion on
[discuss.python.org](https://discuss.python.org/t/sorting-ordered-dicts/25336)
I grabbed the old source, updated it to Python3, added some more functionality
(keeping the items sorted at all times, instead of sorting them on request),
and threw the whole thing on PyPi. Enjoy.

## License

  pyFormex is licensed under the
  [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.html)
  or later (GPLv3+) and so is this package.

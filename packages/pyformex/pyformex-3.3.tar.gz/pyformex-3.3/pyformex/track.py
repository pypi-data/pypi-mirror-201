##
##
##  SPDX-FileCopyrightText: © 2007-2023 Benedict Verhegghe <bverheg@gmail.com>
##  SPDX-License-Identifier: GPL-3.0-or-later
##
##  This file is part of pyFormex 3.3  (Sun Mar 26 20:16:15 CEST 2023)
##  pyFormex is a tool for generating, manipulating and transforming 3D
##  geometrical models by sequences of mathematical operations.
##  Home page: https://pyformex.org
##  Project page: https://savannah.nongnu.org/projects/pyformex/
##  Development: https://gitlab.com/bverheg/pyformex
##  Distributed under the GNU General Public License version 3 or later.
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

"""track.py

Functions for creating classes with access tracking facilities.
This can e.g. be use to detect if the contents of a list or dict
has been changed.
"""

_attributes_ = ['track_methods']

track_methods = [
    '__setitem__', '__setslice__', '__delitem__', 'update', 'append', 'extend',
    'add', 'insert', 'pop', 'popitem', 'remove', 'setdefault', '__iadd__'
]
"""
List of names of methods that can possibly change an object
of type dict or list.
"""


def track_decorator(func):
    """Create a wrapper function for tracked class methods.

    The wrapper function increases the 'hits' attribute of the
    class and then executes the wrapped method.
    Note that the class is passed as the first argument.
    """

    def wrapper(*args, **kw):
        """Wrapper function for a class method."""
        # print(f"NOTIF {func.__name__} {id(args[0])}")
        args[0].hits += 1
        return func(*args, **kw)

    wrapper.__name__ = func.__name__
    return wrapper


def track_class_factory(cls, name='', methods=track_methods):
    """Create a wrapper class with method tracking facilities.

    Tracking a class counts the number of times any of the specified
    class methods has been used.
    Given an input class, this will return a class with tracking
    facilities. The tracking occurs on all the specified methods.
    The default will

    Parameters
    ----------
    cls: class
        The class to be tracked.
    name: str, optional
        The name of the class wrapper. If not provided, the name
        will be 'Tracked' followed by the capitalized class name.
    methods: list of str
        List of class method names that should be taken into account in
        the tracking. Calls to any of these methods will increment the
        number of hits.
        The methods should be owned by the class itself, not by a parent class.
        The default list will track all methods which could possibly change
        a 'list' or a 'dict'.

    Returns
    -------
    class
        A class wrapping the input class and tracking access to any of
        the specified methods. The class has an extra attribute 'hits'
        counting the number accesses to one of these methods.
        This value can be reset to zero to track changes after some
        breakpoint.

    Examples
    --------
    >>> TrackedDict = track_class_factory(dict)
    >>> D = TrackedDict({'a':1,'b':2})
    >>> print(D.hits)
    0
    >>> D['c'] = 3
    >>> print(D.hits)
    1
    >>> D.hits = 0
    >>> print(D.hits)
    0
    >>> D.update({'d':1,'b':3})
    >>> del D['a']
    >>> print(D.hits)
    2
    """
    new_dct = cls.__dict__.copy()
    if 'hits' in new_dct:
        raise ValueError("The input class should not have an attribute 'hits'")

    for key in new_dct:
        if key in track_methods:
            value = new_dct[key]
            new_value = track_decorator(value)
            new_dct[key] = new_value
    new_dct['hits'] = 0
    new_dct['__doc__'] = f"Tracked {cls.__name__} class"
    if not name:
        name = 'Tracked' + cls.__name__.capitalize()
    return type(name, (cls,), new_dct)


TrackedDict = track_class_factory(dict)
TrackedList = track_class_factory(list)

# End

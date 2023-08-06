#
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

"""Timer class.

"""
import time

class Timer():
    """A class for measuring elapsed time.

    The Timer class is a conventient way to measure and report the elapsed
    time during some processing. It uses Python's :func:`time.perf_counter`,
    providing the highest resolution available.

    A Timer instance can be used as a context manager, with automatic
    reading and even reporting the time spent in the context block.
    Timers can also remember any number of measured timings and report
    them later.

    The Timer value is a floating point value giving a number of seconds
    elapsed since some undefined reference point. By default this is the
    moment of creation of the Timer, but the starting point can be set at
    any time.

    Parameters
    ----------
    tag: str, optional
        A label identifying the current measurement. It is used as the key
        to store the value in the Timer memory, and it is printed out together
        with the value when printing the Timer.
    dec: int, optional
        The number of decimals that will be shown or remembered. The default
        (6) provides microsecond accuracy, which is more than enough for
        all purposes.
    start: float, optional
        The starting time of the Timer. If provided, it is normally a value
        obtained from another Timer instance or from :func:`time.perf_counter`.
        If not provided, the time of the initialization of the Timer is used.
    auto: bool, optional
        If True, the value of the Timer will be printed on exit of the
        context manager. Also, the default value for acc becomes False.
        This is very convenient to quickly do timing to some code block.
        See Examples.
    acc: bool, optional
        If True, values read from the Timer are accumulated under the tag
        value. If False, the read value overwrites the value under the tag.
        The default is True if ``acc`` is False, and False is ``acc`` is True.

    Examples
    --------
    The examples use :func:`time.sleep` to provide a code block
    with some known execution time.

    >>> from time import sleep

    The Timer class acts as a context manager, so it can be used in a
    with statement. This is the recommended way to use the Timer.
    It measures the time spent in the block inside the with clause.

    >>> t = Timer()
    >>> with t:
    ...     sleep(0.2)
    >>> print(t)
    Timer: 0.20... sec.

    Printing out the Timer value after measurement is so common, that
    there is an option to do it automatically. Just set the auto mode on
    (it can also be done at instantiation time):

    >>> t.auto = True
    >>> sleep(0.05)
    >>> with t:
    ...     sleep(0.12)
    Timer: 0.32... sec.

    Notice that the Timer accumulated the measured time with the previous.
    This is the default.You can avoid the accumulation by using separate tags
    for the measurements.

    >>> with t.tag('New tag'): sleep(0.23)
    New tag: 0.23... sec.

    Without a tag, the measurement is accumulated to the last specified tag:
    >>> with t: sleep(0.15)
    New tag: 0.38... sec.

    You can switch off accumulation completely if you want to:

    >>> t1 = Timer(dec=2, auto=True, acc=False)
    >>> with t1: sleep(0.06)
    Timer: 0.06 sec.
    >>> with t1: sleep(0.09)
    Timer: 0.09 sec.

    The Timer remembers the last value (accumulated or not) for each of
    the tags that was used. This is very convenient to do a series of
    measurements and then print the Timer :meth:`report`:

    >>> print(t.report())
    Timer: 0.32... sec.
    New tag: 0.38... sec.

    If you want to process the readings in another way, you can access
    them from the Timer memory, which is a dict with the tags a keys:

    >>> print(t.mem)
    {'Timer': 0.32..., 'New tag': 0.38...}

    The last memory item (the one with the current tag) is also available:

    >>> print(t.last)
    New tag: 0.38... sec.

    All Timers keep incrementing at the same pace (that of the unique Python
    :func:`time.perf_counter` counter). So you may think that using a single
    Timer with different tags may suffice. However, to do nested measurements
    with the context manager, you have to use multiple Timers, because our
    context manager is currently not reentrant. So, the following doesn't
    work:

    >>> with Timer("Outer block") as t:
    ...    sleep(0.08)
    ...    with t.tag("Inner block"): sleep(0.12)
    ...    sleep(0.07)
    ...    with t.tag("Inner block 2"): sleep(0.17)
    ...    sleep(0.06)
    ...
    >>> print(t.report())
    Inner block: 0.12... sec.
    Inner block 2: 0.40... sec.

    See how the timings from the outer block are added to the
    "Inner block 2" tag and there is no "Outer block" result at all.
    The correct way to do nested measurement is using multiple Timers:

    >>> with Timer("Outer block") as t:
    ...    sleep(0.08)
    ...    with Timer("Inner block") as t1: sleep(0.12)
    ...    sleep(0.07)
    ...    with t1.tag("Inner block 2"): sleep(0.05)
    ...    sleep(0.06)
    ...
    >>> print(t1.report())
    Inner block: 0.12... sec.
    Inner block 2: 0.05... sec.
    >>> print(t.report())
    Outer block: 0.38... sec.

    There may be times when the use of a context manager is not useful
    or even possible (like when the start and end of measurement are in
    different functions). Then you can always use the low level interface.

    The measurement is always done with the :meth:`read` method. It measures
    and returns the time since the last :meth:`reset` or the creation of the
    Timer. Here is an example:

    >>> t = Timer(dec=2)
    >>> sleep(0.03)
    >>> v = t.read()
    >>> sleep(0.05)
    >>> t.reset()
    >>> sleep(0.07)
    >>> v1 = t.read()
    >>> print(v, v1)
    0.03... 0.07...

    As we use a single tag, the memory shows the accumulated result:

    >>> print(t.mem)
    {'Timer': 0.10...}

    You can have a peek at the current value of the timer, without
    actually reading it:

    >>> sleep(0.07)
    >>> t.value
    0.14...
    >>> print(t.last)
    Timer: 0.1 sec.

    Any read will however update the current tag:

    >>> v = t.read()
    >>> print(v)
    0.14...
    >>> print(t.last)
    Timer: 0.24 sec.

    When not explicitely calling :meth:`read` (like when using the context
    manager), you can still get the last value read:

    >>> print(t.lastread)
    0.14...

    """
    def __init__(self, tag='Timer', *, dec=6, start=None, auto=False, acc=None):
        """Create and reset the timer."""
        self.mem = {}
        self._last_read = None
        self.tag(tag)
        self.dec = int(dec)
        self.auto = bool(auto)
        self.acc = (not self.auto) if acc is None else bool(acc)
        self.reset(start=start)

    def tag(self, tag):
        self._tag = str(tag)
        return self

    def reset(self, tag=None, *, start=None):
        """(Re)Start the timer and optionally changes the tag.

        Parameters
        ----------
        tag: str, optional
            A label to override the current Timer tag.
        start: float, optional
            The new starting time of the Timer. Default is to use the
            time of the reset call.

        Returns
        -------
        Timer
            Returns self so that one can use the reset directly in a
            with statement. See examples.

        """
        if tag is not None:
            self._tag = str(tag)
        if start is None:
            self.start = time.perf_counter()
        else:
            self.start = float(start)

    def read(self, tag=None, *, reset=False):
        """Read the timer.

        Parameters
        ----------
        reset: bool, optional
            If True, the Timer is reset after reading, thus the next read
            will measure from this point.

        Returns
        -------
        float
            The elapsed time in seconds since the last reset or since the
            creation of the Timer if there hasn't been a reset.
        """
        now = time.perf_counter()
        value = now - self.start
        if tag is not None:
            self._tag = str(tag)
        if self.acc and self._tag in self.mem:
            self.mem[self._tag] += value
        else:
            self.mem[self._tag] = value
        if self.auto:
            print(self.report(keys=[self._tag]))
        if reset:
            self.start = time.perf_counter()
        self._last_read = round(value, self.dec)
        return value

    @property
    def value(self):
        """Return the current value of the Timer without reading it.

        Returns
        -------
        float
            The current value of the Timer. This value is not stored.
        """
        now = time.perf_counter()
        return now - self.start

    @property
    def lastread(self):
        """Return the value of the last read rounded to the Timer accuracy"""
        return self._last_read

    def __enter__(self):
        """Enter the context manager"""
        self.reset()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context manager

        Records the time passed since entry.
        If auto, also prints the Timer report.
        """
        self.read()

    def format(self, tag=None):
        """Return the formatted last read valuefor the specified tag.

        Returns
        -------
        string
            The value of the last :meth:`read` operation on the Timer (whether
            explicitly called or implicitly from the context manager),
            or None if the Timer hasn't been read yet.
        """
        if tag is None:
            tag = self._tag
        if tag in self.mem:
            val = round(self.mem[tag], self.dec)
        else:
            val = None
        return f"{tag}: {val} sec."

    @property
    def last(self):
        """Print the formatted value of the last used tag"""
        return self.format(self._tag)

    def report(self, keys=None, dec=None):
        """Return the formatted readings in the Timer memory.

        """
        if keys is None:
            keys = self.mem
        return '\n'.join(self.format(tag) for tag in keys)

    def __str__(self):
        """Return a string with the current reading of the Timer"""
        return self.report()


if __name__ == "__main__":

    print(f"Running doctests on {__file__}")
    import doctest
    doctest.testmod()

# End

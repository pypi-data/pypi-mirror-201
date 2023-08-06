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
"""A collection of miscellaneous utility functions.

The pyformex.utils module contains a wide variety of utilitary functions.
Because there are so many and they are so widely used, the utils module
is imported in the environment where scripts and apps are executed, so
that users can always call the utils functions without explicitely
importing the module.

Module attributes
~~~~~~~~~~~~~~~~~

Attributes
----------
FileTypes: dict
    A collection of :class:`FileType` records. Each FileType instance holds
    the definition of a file type, and is accessible from this dict with a
    simple mnemonic key. These are the ones that are commonly used in
    pyFormex.  But users can add their own definitions too, just by creating
    an instance of :class:`FileType`.

Examples
--------
>>> for k,v in FileTypes.items(): print(f"{k} = '{v}'")
all = 'All files (*)'
ccx = 'CalCuliX files (*.dat *.inp)'
dcm = 'DICOM images (*.dcm)'
dxf = 'AutoCAD DXF files (*.dxf)'
dxftext = 'Converted AutoCAD files (*.dxftext)'
flavia = 'flavia results (*.flavia.msh *.flavia.res)'
gts = 'GTS files (*.gts)'
gz = 'Compressed files (*.gz *.bz2)'
html = 'Web pages (*.html)'
icon = 'Icons (*.xpm)'
img = 'Images (*.png *.jpg *.jpeg *.eps *.gif *.bmp)'
inp = 'Abaqus or CalCuliX input files (*.inp)'
neu = 'Gambit Neutral files (*.neu)'
obj = 'Wavefront OBJ files (*.obj)'
off = 'Geomview object files (*.off)'
pgf = 'pyFormex geometry files (*.pgf)'
ply = 'Stanford Polygon File Format files (*.ply)'
png = 'PNG images (*.png)'
poly = 'Polygon files (*.off *.obj *.ply)'
postproc = 'Postproc scripts (*.post.py)'
pyformex = 'pyFormex scripts (*.py *.pye)'
pyf = 'pyFormex projects (*.pyf)'
python = 'Python files (*.py)'
pzf = 'pyFormex zip files (*.pzf)'
smesh = 'Tetgen surface mesh files (*.smesh)'
stl = 'STL files (*.stl)'
stlb = 'Binary STL files (*.stl)'
surface = 'Surface models (*.gts *.stl *.off *.obj *.ply)'
tetsurf = 'Tetgen surface (*.smesh)'
tetgen = 'Tetgen files (*.poly *.smesh *.ele *.face *.edge *.node *.neigh)'
video = 'Video (*.mp4)'
vtk = 'VTK types (*.vtk *.vtp)'
vtp = 'vtkPolyData file (*.vtp)'
geometry = 'All Geometry files (*.gts *.inp *.neu *.obj *.off *.pgf *.ply *.pzf *.stl *.vtk *.vtp)'
"""  # noqa: E501
import os
import re
import tempfile
import time
import random
import types
import warnings
from functools import wraps

import pyformex as pf
from pyformex import process
from pyformex.path import Path

# These are here to re-export them as utils functions
from pyformex.software import Module, External    # noqa: F401
from pyformex.mydict import formatDict            # noqa: F401

def pzf_register(clas):
    """Class decorator to allow load from PZF format.

    Adding this decoratot to a class registers the class with the
    :mod:`pzffile` module. Objects in a PZF file with class name equal
    to clas.__name__ will then be restored using this class.
    """
    from pyformex import pzffile
    pzffile.register(clas)
    return clas


shuffle = random.shuffle

# Some regular expressions
_re_digits = re.compile(r'(\d+)')
_re_filedesc = re.compile(r'.*\((.*)\).*')


### Decorators ###

def memoize(func):
    """Remember the result of an instance method call.

    This is a decorator function that saves the result of an instance
    method call into the instance.
    Subsequent use of the function will return the result from
    memory instead of recomputing it.

    Notes
    ----_
    If the decorated function has no arguments other than self, this
    decorator can be stacked with @property to create a cached property.

    The result is saved in a dict with the function name and its arguments
    as key. The dict is stored as an instance attribute _memory. It is
    created automatically on first used of a memoizing method.

    Examples
    --------
    We create a class with a single method, returning a list of 10
    random ints in the range from 0 to 20. The method's result is
    memoized.
    >>> class C:
    ...     @memoize
    ...     def random_ints(self):
    ...         print("Computing random ints")
    ...         return [random.randint(0,20) for i in range(10)]

    We create an instance and call the random_ints method.

    >>> c = C()
    >>> a = c.random_ints()
    Computing random ints
    >>> print(len(a), min(a) >= 0, max(a) <= 20)
    10 True True

    When calling the random_ints method again, the method is not actually
    executed, but the memoized values are returned, so they are the same
    as the previous.

    >>> b = c.random_ints()
    >>> print(len(b), a == b)
    10 True

    If we create another instance, we get other values, because the
    memoizing is done per instance.

    >>> b = C().random_ints()
    Computing random ints
    >>> print(len(b), a == b)
    10 False

    The results are stored in the _memory attribute. They can be deleted
    to force recomputation.

    >>> print(c._memory)
    {'random_ints': [...]}
    """
    @wraps(func)
    def wrapper(self, *args, **kargs):
        key = func.__name__
        if args:
            key += str(args)
        if kargs:
            key += str(kargs)
        if not hasattr(self, '_memory'):
            self._memory = {}
        if key in self._memory:
            # return saved result
            res = self._memory[key]
        else:
            # compute and memoize result
            self._memory[key] = res = func(self, *args, **kargs)
        return res
    return wrapper


######### WARNINGS ##############

def rev_lookup(dictionary, value, default=None):
    """Reverse lookup in a dict

    Lookup a value in a dict, and return its key (the first match).

    Parameters
    ----------
    dictionary: dict
        The dict in which to lookup a value
    value: anything
        The value to lookup in the dict
    default: anything
        The key to return if the value was not found

    Returns
    -------
    key: anything
        The first key in the dict whose value matches the given ``value``,
        or ``default`` if no match was found.
    """
    for key, val in dictionary.items():
        if val==value:
            return key
    return default


def warningCategory(category):
    """Return a warning category and its alias

    The input can be a category or an alias. Returns both as a tuple
    (alias, category).
    Invalid values return the default category ('W', Warning).
    """
    _warn_category = {'W': Warning, 'U': UserWarning, 'F': FutureWarning}
    if category in _warn_category:
        alias = category
    else:
        alias = rev_lookup(_warn_category, category, 'W')
    return alias, _warn_category[alias]


def warningAction(action):
    """Return a warning action and its alias

    The input can be an action string or an alias. Returns both as a tuple
    (alias, action).
    Invalid values return the default action ('i', 'ignore').
    """
    _warn_action = {'d': 'default', 'i': 'ignore', 'a': 'always',
                    'o': 'once', 'e': 'error'}
    if action in _warn_action:
        alias = action
    else:
        alias = rev_lookup(_warn_action, action, 'i')
    return alias, _warn_action[alias]


def filterWarning(message, module='', category='U', action='i', save=False):
    """Add a warning message to the warnings filter.

    category can be a Warning subclass or a key in the _warn_category dict

    If save is True, the filter is saved in the user settings for future
    sessions.
    """
    message = str(message)
    if message.isidentifier() or len(message) < 40:
        # Avoid short messages hiding longer ones starting with
        # the same string. This is because Python filters test whether
        # the message starts with the given re.
        message = message + '$'
    c, category = warningCategory(category)
    a, action = warningAction(action)
    pf.debug(f"Warning filter: {action} {category.__name__} '{message}' "
             f"from module '{module}'", pf.DEBUG.WARNING)
    warnings.filterwarnings(action, message, category, module)

    if save:
        filters = pf.prefcfg['warnings/filters']
        newfilter = (message, '', c)
        if action != 'i':
            newfilter = (*newfilter, a)
        filters.add(newfilter)
        pf.debug(f"Saved warning filters: {pf.prefcfg['warnings/filters']}",
                 pf.DEBUG.WARNING)


_saved_warnings = None

def resetWarningFilters():
    """Reset the warning filters

    Reset the warning filters to the Python defaults plus the ones
    listed in the 'warnings/filters' configuration variable.
    """
    if pf.cfg['warnings/reset']:
        warnings.resetwarnings()
    pf.debug(
        f"Current warning filters: {pf.cfg['warnings/filters']}",
        pf.DEBUG.WARNING
    )
    # We always add the refcfg filters, to avoid having to store them
    a = set(pf.prefcfg['warnings/filters'])
    b = set(pf.refcfg['warnings/filters'])
    for w in a | b:
        try:
            filterWarning(*w)
        except Exception:
            pf.debug(
                f"Error while processing warning filter: {w}",
                pf.DEBUG.WARNING
            )


def warn(message, level=UserWarning, stacklevel=2, uplevel=0, data=None):
    import sys
    if 'pytest' not in sys.modules:
        from pyformex import messages
        messages._message_data = data
        warnings.warn(message, level, stacklevel+uplevel)


def deprec(message, stacklevel=4, data=None):
    warn(message, level=FutureWarning, stacklevel=stacklevel, data=data)


def warning(message, level=UserWarning, stacklevel=3):
    """Decorator to add a warning to a function.

    Adding this decorator to a function will warn the user with the
    supplied message when the decorated function gets executed for
    the first time in a session.
    An option is provided to switch off this warning in future sessions.

    Decorating a function is done as follows::

      @utils.warning('This is the message shown to the user')
      def function(args):
          ...

    """
    import functools

    def decorator(func):
        def wrapper(*_args, **_kargs):
            warn(message, level=level, stacklevel=stacklevel)
            # For some reason these messages are not auto-appended to
            # the filters for the currently running program
            # Therefore we do it here explicitely
            filterWarning(message, category=level)
            return func(*_args, **_kargs)
        functools.update_wrapper(wrapper, func)
        return wrapper

    return decorator


def deprecated(message, stacklevel=4):
    """Decorator to deprecate a function

    This is like :func:`warning`, but the level is set to FutureWarning.
    """
    return warning(message, level=FutureWarning, stacklevel=stacklevel)


def deprecated_by(old, new, stacklevel=4):
    """Decorator to deprecate a function by another one.

    Adding this decorator to a function will warn the user with a
    message that the `old` function is deprecated in favor of `new`,
    at the first execution of `old`.

    See also: :func:`deprecated`.
    """
    return deprecated(f"{old} is deprecated: use {new} instead",
                      stacklevel=stacklevel)


def deprecated_future():
    """Decorator to warn that a function may be deprecated in future.

    See also: :func:`deprecated`.
    """
    return deprecated("This functionality is deprecated and will probably "
                      "be removed in future, unless you explain to the "
                      "developers why they should retain it.")


##########################################################################
## Running external commands ##
###############################

# Store the outcome of the last command
last_command = None

def system(args, *, verbose=False, wait=True, **kargs):
    """Execute a command through the operating system.

    This is a wrapper around the :func:`process.run` function,
    aimed particularly at the pyFormex GUI user. It has one extra parameter:
    `verbose`. See :func:`process.run` for the other parameters.

    Parameters
    ----------
    verbose: bool
        If True, the command, and a report of its outcome in case of failure,
        timeout or error exit, are written to stdout.

    Returns
    -------
    :class:`DoneProcess` or subprocess.Popen
        If `wait` is True, returns a :class:`DoneProcess` with the outcome of
        the command.
        If `wait` is False, returns a subprocess.Popen which can be used to
        communicate with the started subprocess.

    See Also
    --------
    process.run: run a system command in a subprocess
    command: call :func:`system` with some other defaults

    Examples
    --------
    >>> P = system("pwd")
    >>> P.stdout.strip('\\n') == os.getcwd()
    True

    >>> P = system('true')
    >>> P
    DoneProcess(args=['true'], returncode=0, stdout='', stderr='')
    >>> P = system('false', capture_output=False)
    >>> P
    DoneProcess(args=['false'], returncode=1)
    >>> P = system('False', verbose=True)
    Running command: False
    DoneProcess report
    args: ['False']
    Command failed to run!
    returncode: 127

    >>> P = system("sleep 5", timeout=1, verbose=True)
    Running command: sleep 5
    DoneProcess report
    args: ['sleep', '5']
    returncode: -1
    stdout:
    stderr:
    timedout: True

    """
    global last_command

    if verbose:
        print(f"Running command: {args}")
        if pf.app:
            pf.app.processEvents()

    P = process.run(args, wait=wait, **kargs)

    if wait:
        last_command = P
        if verbose and (P.failed or P.timedout or P.returncode != 0):
            print(P)

    return P


def command(args, verbose=True, check=True, **kargs):
    """Run an external command in a user friendly way.

    This is equivalent with :func:`system` with verbose=True by default.
    """
    return system(args, verbose=verbose, **kargs)


def killProcesses(pids, signal=15):
    """Send the specified signal to the processes in list

    Parameters
    ----------
    pids: list of int
        List of process ids to be killed.
    signal: int
        Signal to be send to the processes. The default (15) will
        try to terminate the process in a friendly way.
        See ``man kill`` for more values.
    """
    for pid in pids:
        try:
            os.kill(pid, signal)
        except Exception:
            pf.debug(f"Error in killing of process {pid}", pf.DEBUG.INFO)


# NOT USED.
# def execSource(script, glob={}):
#     """Execute Python code in another thread.

#     Parameters
#     ----------
#     script: str
#         A string containing some executable Python/pyFormex code.
#     glob: dict, optional
#         A dict with globals specifying the environment in which the
#         source code is executed.
#     """
#     pf.interpreter.locals = glob
#     pf.interpreter.runsource(script, '<input>', 'exec')


##########################################################################
## match multiple patterns
##########################


def matchMany(regexps, target):
    """Return multiple regular expression matches of the same target string."""
    return [re.match(r, target) for r in regexps]


def matchCount(regexps, target):
    """Return the number of matches of target to  regexps."""
    return len([_f for _f in matchMany(regexps, target) if _f])


def matchAny(regexps, target):
    """Check whether target matches any of the regular expressions."""
    return matchCount(regexps, target) > 0


def matchNone(regexps, target):
    """Check whether target matches none of the regular expressions."""
    return matchCount(regexps, target) == 0


def matchAll(regexps, target):
    """Check whether targets matches all of the regular expressions."""
    return matchCount(regexps, target) == len(regexps)


##########################################################################
## File types ##
################

FileTypes = {}

def combined_suffixes(*args):
    suff = set()
    for arg in args:
        try:
            suff |= set(FileTypes[arg].suffixes())
        except KeyError:
            suff |= {arg}
    return sorted(suff)


class FileType:
    """A class for holding file types and the related filename patterns.

    Parameters
    ----------
    key: str
        A short and unique mnemonic string, by preference lower case,
        that wil be used as lookup key for this FileType definition
        in the global :attr:`FileTypes` collection.
    text: str
        A textual description of the file type.
    *suffixes: sequence of str
        All remaining parameters are file suffixes that should be used
        to filter files that are supposed to be of this type. Any number
        of suffixes is allowed. If None are provided, all files will match
        the file type.

    See Also
    --------
    FileTypes: the set of FileType's knownd by pyFormex

    """
    def __init__(self, key, text, *suffixes):
        self.text = text
        self.suff = suffixes
        FileTypes[key] = self


    def suffixes(self, compr=False):
        """Return a list of file suffixes for the FileType.

        Parameters
        ----------
        compr: bool
            If True, the file suffixes for compressed files of this type
            are automatically added.

        Examples
        --------
        >>> FileTypes['pgf'].suffixes()
        ['pgf']
        >>> FileTypes['pgf'].suffixes(compr=True)
        ['pgf', 'pgf.gz', 'pgf.bz2']
        >>> FileTypes['all'].suffixes()
        []
        """
        suff = list(self.suff)
        if compr:
            compr_types = FileTypes['gz'].suff
            suff.extend([f"{s}.{c}" for s in suff for c in compr_types])
        return suff


    def patterns(self, compr=False):
        """Return a list with the file patterns matching the FileType.

        Parameters
        ----------
        compr: bool
            If True, the file suffixes for compressed files of this type
            are automatically added.

        Examples
        --------
        >>> FileTypes['pgf'].patterns()
        ['*.pgf']
        >>> FileTypes['pgf'].patterns(compr=True)
        ['*.pgf', '*.pgf.gz', '*.pgf.bz2']
        >>> FileTypes['all'].patterns()
        ['*']
        """
        if self.suff:
            return [f"*.{s}" for s in self.suffixes(compr)]
        else:
            return ['*']


    def desc(self, compr=False):
        """Create a filetype description compatible with Qt Widgets.

        Parameters
        ----------
        compr: bool
            If True, the file patterns for compressed files are automatically
            added.

        Returns
        -------
        str
            A string that can be directly used in the Qt File Dialog
            widgets to filter the selectable files. This string has the
            format::

                file type text (*.ext1 *.ext2)

        Examples
        --------
        >>> FileTypes['img'].desc()
        'Images (*.png *.jpg *.jpeg *.eps *.gif *.bmp)'
        >>> fileDescription('inp')
        'Abaqus or CalCuliX input files (*.inp)'
        >>> fileDescription('doc')
        'DOC files (*.doc)'
        >>> fileDescription('*.inp')
        '*.inp'
        >>> fileDescription('pgf',compr=True)
        'pyFormex geometry files (*.pgf *.pgf.gz *.pgf.bz2)'
        """
        return f"{self.text} ({' '.join(self.patterns(compr))})"


    __str__ = desc


# The builtin file types. Only types that are relevant for pyFormex
# should be added here. Users can of course add their own types.
FileType('all', 'All files')
FileType('ccx', 'CalCuliX files', 'dat', 'inp')
FileType('dcm', 'DICOM images', 'dcm')
FileType('dxf', 'AutoCAD DXF files', 'dxf')
FileType('dxftext', 'Converted AutoCAD files', 'dxftext')
FileType('flavia', 'flavia results', 'flavia.msh', 'flavia.res')
FileType('gts', 'GTS files', 'gts')
FileType('gz', 'Compressed files', 'gz', 'bz2')
FileType('html', 'Web pages', 'html')
FileType('icon', 'Icons', 'xpm')
FileType('img', 'Images', 'png', 'jpg', 'jpeg', 'eps', 'gif', 'bmp')
FileType('inp', 'Abaqus or CalCuliX input files', 'inp')
FileType('neu', 'Gambit Neutral files', 'neu')
FileType('obj', 'Wavefront OBJ files', 'obj')
FileType('off', 'Geomview object files', 'off')
FileType('pgf', 'pyFormex geometry files', 'pgf')
FileType('ply', 'Stanford Polygon File Format files', 'ply')
FileType('png', 'PNG images', 'png')
FileType('poly', 'Polygon files', 'off', 'obj', 'ply')
FileType('postproc', 'Postproc scripts', 'post.py')
FileType('pyformex', 'pyFormex scripts', 'py', 'pye')
FileType('pyf', 'pyFormex projects', 'pyf')
FileType('python', 'Python files', 'py')
FileType('pzf', 'pyFormex zip files', 'pzf')
FileType('smesh', 'Tetgen surface mesh files', 'smesh')
FileType('stl', 'STL files', 'stl')
FileType('stlb', 'Binary STL files', 'stl')  # Use only for output
FileType('surface', 'Surface models', 'gts', 'stl', 'off', 'obj', 'ply')
FileType('tetsurf', 'Tetgen surface', 'smesh')
FileType('tetgen', 'Tetgen files', 'poly', 'smesh', 'ele', 'face',
         'edge', 'node', 'neigh')
FileType('video', 'Video', 'mp4')
FileType('vtk', 'VTK types', 'vtk', 'vtp')
FileType('vtp', 'vtkPolyData file', 'vtp')
FileType('geometry', 'All Geometry files', *combined_suffixes(
    'pzf', 'pgf', 'surface', 'poly', 'vtk', 'inp', 'neu'))


def fileDescription(ftype, compr=False):
    """Return a description of the specified file type(s).

    Parameters
    ----------
    ftype: str or list of str
        The file type (or types) for which a description is requested.
        The case of the string(s) is ignored: it is converted to lower case.

    Returns
    -------
    str of list of str
        The file description(s) corresponding with the specified file type(s).
        The return value(s) depend(s) on the value of the input string(s) in the
        the following way (see Examples below):

        - if it is a key in the :attr:`file_description` dict, the
          corresponding value is returned;
        - if it is a string of only alphanumerical characters: it is interpreted
          as a file extension and the corresponding return value is
          ``FTYPE files (*.ftype)``;
        - any other string is returned as as: this allows the user to compose
          his filters himself.

    Examples
    --------
    >>> fileDescription('img')
    'Images (*.png *.jpg *.jpeg *.eps *.gif *.bmp)'
    >>> fileDescription(['stl','all'])
    ['STL files (*.stl)', 'All files (*)']
    >>> fileDescription('inp')
    'Abaqus or CalCuliX input files (*.inp)'
    >>> fileDescription('doc')
    'DOC files (*.doc)'
    >>> fileDescription('Video (*.mp4 *.ogv)')
    'Video (*.mp4 *.ogv)'
    >>> fileDescription('pgf',compr=True)
    'pyFormex geometry files (*.pgf *.pgf.gz *.pgf.bz2)'
    """
    if isinstance(ftype, list):
        return [fileDescription(f, compr) for f in ftype]
    ltype = ftype.lower()
    if ltype in FileTypes:
        ret = FileTypes[ltype].desc(compr)
    elif ftype.isalnum():
        ret = f"{ftype.upper()} files (*.{ftype})"
    else:
        ret = ftype
    return ret


def fileTypes(ftype, compr=False):
    """Return the list of file extension types for a given type.

    Parameters
    ----------
    ftype: str
        The file type (see :func:`fileDescription`.
    compr: bool,optional
        If True, the compressed file types are automatically added.

    Returns
    -------
    list of str
        A list of the normalized matching extensions for this type.
        Normalized extension do not have the leading dot and are
        lower case only.

    Examples
    --------
    >>> fileTypes('pgf')
    ['pgf']
    >>> fileTypes('pgf',compr=True)
    ['pgf', 'pgf.gz', 'pgf.bz2']
    """
    return FileTypes[ftype].suffixes(compr)


def fileTypesFromFilter(fdesc):
    """Extract the filetypes from a file type descriptor.

    A file type descriptor is a string consisting of an initial part
    followed by a second part enclosed in parentheses. The second part
    is a space separated list of glob patterns. An example
    file descriptor is 'file type text (\\*.ext1 \\*.ext2)'.
    This is the format as returned by :meth:`FileType.desc`.

    Parameters
    ----------
    fdesc: str
        A file descriptor string.
    compr: bool,optional
        If True, the compressed file types are automatically added.

    Returns
    -------
    desc: str
        The file type description text.
    ext: list of str
        A list of the matching extensions (without dot) for this type.
        An empty string means that any extension is accepted.

    Examples
    --------
    >>> fileTypesFromFilter(FileTypes['img'].desc())
    ['png', 'jpg', 'jpeg', 'eps', 'gif', 'bmp']
    >>> fileTypesFromFilter(FileTypes['pgf'].desc(compr=True))
    ['pgf', 'pgf.gz', 'pgf.bz2']
    >>> fileTypesFromFilter('* *.png')
    ['', 'png']
    >>> fileTypesFromFilter('Images (*.png *.jpg *.jpeg)')
    ['png', 'jpg', 'jpeg']
    """
    m = _re_filedesc.match(fdesc)
    ext = m.groups()[0] if m else fdesc
    return [e.lstrip('*').lstrip('.') for e in ext.split(' ')]


def setFiletypeFromFilter(filename, fdesc):
    """Make sure a filename has an acceptable suffix.

    Parameters
    ----------
    filename: :class:`~path.Path`
        The filename to chaeck and set the suffix.
    fdesc: str
        A file descriptor string.

    Returns
    -------
    Path
        If `filename` had a suffix included in `accept`, returns the
        input filename unaltered. Else returns the filename with a dot
        and the first suffix from `accepted` appeded to it.

    Examples
    --------
    >>> setFiletypeFromFilter('image01.jpg', 'Images (*.png *.jpg *.jpeg)')
    Path('image01.jpg')
    >>> setFiletypeFromFilter('image01', 'Images (*.png *.jpg *.jpeg)')
    Path('image01.png')
    """
    filename = Path(filename)
    okext = fileTypesFromFilter(fdesc)
    if not ('' in okext or filename.filetype() in okext):
        filename = filename.with_suffix('.'+okext[0])
    return filename


def okURL(url):
    """Check that an URL is displayable in the browser.

    Parameters
    ----------
    url: URL
        The URL to be checked.

    Returns
    -------
    bool
        True if ``url`` starts with a protocol that is either
        'http:', 'https:' or 'file:'; else False
    """
    s = url.split(':')
    return len(s) > 1 and s[0] in ['http', 'https', 'file']


##########################################################################
## Filenames ##
###############

# TODO: these should go to path module


def projectName(fn):
    """Derive a project name from a file name.

    The project name is the basename of the file without the extension.
    It is equivalent with Path(fn).stem

    Examples
    --------
    >>> projectName('aa/bb/cc.dd')
    'cc'
    >>> projectName('cc.dd')
    'cc'
    >>> projectName('cc')
    'cc'
    """
    return Path(fn).stem


def findIcon(name):
    """Return the file name for an icon with given name.

    Parameters
    ----------
    name: str
        Name of the icon: this is the stem fof the filename.

    Returns
    -------
    str
        The full path name of an icon file with the specified name, found
        in the pyFormex icon folder, or the question mark icon file, if
        no match was found.

    Examples
    --------
    >>> print(findIcon('view-xr-yu').relative_to(pf.cfg['pyformexdir']))
    icons/view-xr-yu.xpm
    >>> print(findIcon('right').relative_to(pf.cfg['pyformexdir']))
    icons/64x64/right.png
    >>> print(findIcon('xyz').relative_to(pf.cfg['pyformexdir']))
    icons/question.xpm
    >>> print(findIcon('recording').relative_to(pf.cfg['pyformexdir']))
    icons/recording.gif
    """
    for icondir in pf.cfg['gui/icondirs']:
        for icontype in pf.cfg['gui/icontypes']:
            fname = icondir / (name+icontype)
            if fname.exists():
                return fname

    return pf.cfg['icondir'] / 'question.xpm'


def listIconNames(dirs=None, types=None):
    """Return the list of available icons by their name.

    Parameters
    ----------
    dirs: list of paths, optional
        If specified, only return icons names from these directories.
    types: list of strings, optional
        List of file suffixes, each starting with a dot. If specified,
        Only names of icons having one of these suffixes are returned.

    Returns
    -------
    list of str
        A sorted list of the icon names available in the pyFormex icons folder.

    Examples
    --------
    >>> listIconNames()[:4]
    ['clock', 'dist-angle', 'down', 'down']
    >>> listIconNames([pf.cfg['icondir'] / '64x64'])[:4]
    ['down', 'ff', 'info', 'lamp']
    >>> listIconNames(types=['.xpm'])[:4]
    ['clock', 'dist-angle', 'down', 'empty']
    """
    if dirs is None:
        dirs = pf.cfg['gui/icondirs']
    if types is None:
        types = pf.cfg['gui/icontypes']
    types = ['.+\\'+t for t in types]
    icons = []
    for icondir in dirs:
        icons += [Path(f).stem for f in icondir.filenames()
                  if matchAny(types, f)]
    return sorted(icons)


##########################################################################
## File lists ##
################


def sourceFiles(relative=False, symlinks=True, extended=False):
    """Return the list of pyFormex .py source files.

    Parameters
    ----------
    relative: bool
        If True, returned filenames are relative to the current directory.
    symlinks: bool
        If False, files that are symbolic links are retained in the
        list. The default is to remove them.
    extended: bool
        If True, also return the .py files in all the paths in the configured
        appdirs and scriptdirs.

    Returns
    -------
    list of str
        A list of filenames of .py files in the pyFormex source tree, and,
        if ``extended`` is True, .py files in the configured app and script
        dirs as well.
    """
    path = pf.cfg['pyformexdir']
    ftypes = 'Hf' if symlinks else 'HSf'
    if relative:
        path = path.relative_to(Path.cwd())
    files = path.listTree(
        includedir=pf.cfg['sourcedirs'],
        includefile=[r'.*\.py', 'pyformexrc'],
        ftypes=ftypes)
    if extended:
        searchdirs = [Path(i[1]) for i in pf.cfg['appdirs'] + pf.cfg['scriptdirs']]
        for path in set(searchdirs):
            if path.exists():
                files += path.listTree(
                    includefile=[r'.*\.py'], ftypes=ftypes)
    return files


def grepSource(pattern, options='', relative=True, verbose=False):
    """Finds pattern in the pyFormex source files.

    Uses the `grep` program to find all occurrences of some specified
    pattern text in the pyFormex source .py files (including the examples).
    Extra options can be passed to the grep command. See `man grep` for
    more info.

    Returns the output of the grep command.
    """
    opts = options.split(' ')
    if '-a' in opts:
        opts.remove('-a')
        options = ' '.join(opts)
        extended = True
    else:
        extended = False
    files = sourceFiles(relative=relative, extended=extended, symlinks=False)
    cmd = f"grep {options} '{pattern}' {' '.join(files)}"
    P = system(cmd, verbose=verbose)
    if not P.returncode:
        return P.stdout


def moduleList(package='all'):
    """Return a list of all pyFormex modules in a subpackage.

    This is like :func:`sourceFiles`, but returns the files in a
    Python module syntax.
    """
    exclude = ['examples', 'scripts', 'opengl3']
    files = sourceFiles(relative=True)
    directory = os.path.split(files[0])[0]
    dirlen = len(directory)
    if dirlen > 0:
        dirlen += 1
    # Retain only .py files and convert to Python pkg.module format
    modules = [fn[dirlen:].replace('.py', '').replace('/', '.')
               for fn in files if fn.endswith('.py')]
    if package == 'core':
        # only core
        modules = [m for m in modules if '.' not in m]
    elif package == 'all':
        # everything except examples
        modules = [m for m in modules if m.split('.')[0] not in exclude]
    elif package == 'all+ex':
        # everything including examples
        pass
    else:
        modules = [m for m in modules if m.startswith(package+'.')]
    for i, m in enumerate(modules):
        if m.endswith('__init__'):
            if m == '__init__':
                modules[i] = 'pyformex'
            else:
                modules[i] = m[:-9]
    return modules


def findModuleSource(module):
    """Find the path of the source file of a module

    module is either an imported module (pkg.mod) or a string with the module
    name ('pkg.mod'), imported or not.
    Returns the source file from which the module was/would be loaded when
    imported.
    Raises an error if the module can not be imported or
    does not have a source file.
    """
    import importlib.util
    if isinstance(module, str):
        spec = importlib.util.find_spec(module)
        if spec is None:
            raise ImportError(f"Can't find module {module}")
    else:
        spec = module.__spec__
    return spec.origin


def diskSpace(path, units=None, ndigits=2):
    """Returns the amount of diskspace of a file system.

    Parameters
    ----------
    path: :term:`path_like`
        A path name inside the file system to be probed.
    units: str
        If provided, results are reported in this units. See
        :meth:`humanSize` for possible values. The default
        is to return the number of bytes.
    ndigits: int
        If provided, and also ``units`` is provided, specifies the number
        of decimal digits to report. See :meth:`humanSize` for details.

    Returns
    -------
    total: int | float
        The total disk space of the file system containing ``path``.
    used: int | float
        The used disk space on the file system containing ``path``.
    available: int | float
        The available disk space on the file system containing ``path``.

    Notes
    -----
    The sum ``used + available`` does not necessarily equal ``total``,
    because a file system may (and usually does) have reserved blocks.
    """
    stat = os.statvfs(Path(path).resolve())
    total = stat.f_blocks * stat.f_frsize
    avail = stat.f_bavail * stat.f_frsize
    used = (stat.f_blocks - stat.f_bfree) * stat.f_frsize
    if units:
        total = humanSize(total, units, ndigits)
        avail = humanSize(avail, units, ndigits)
        used = humanSize(used, units, ndigits)
    return total, used, avail


def humanSize(size, units, ndigits=-1):
    """Convert a number to a human size.

    Large numbers are often represented in a more human readable
    form using k, M, G prefixes. This function returns the input
    size as a number with the specified prefix.

    Parameters
    ----------
    size: int or float
        A number to be converted to human readable form.
    units: str
        A string specifying the target units. The first character should
        be one of k,K,M,G,T,P,E,Z,Y. 'k' and 'K' are equivalent. A second
        character 'i' can be added to use binary (K=1024) prefixes instead of
        decimal (k=1000).
    ndigits: int, optional
        If provided and >=0, the result will be rounded to this number of
        decimal digits.

    Returns
    -------
    float
        The input value in the specified units and possibly rounded
        to ``ndigits``.

    Examples
    --------
    >>> humanSize(1234567890,'k')
    1234567.89
    >>> humanSize(1234567890,'M',0)
    1235.0
    >>> humanSize(1234567890,'G',3)
    1.235
    >>> humanSize(1234567890,'Gi',3)
    1.15
    """
    size = float(size)
    order = '.KMGTPEZY'.find(units[0].upper())
    if units[1:2] == 'i':
        scale = 1024.
    else:
        scale = 1000.
    size = size / scale**order
    if ndigits >= 0:
        size = round(size, ndigits)
    return size


##########################################################################
## Temporary Files ##
#####################


class TempDir(tempfile.TemporaryDirectory):
    """A temporary directory that can be used as a context manager.

    This is a wrapper around Python's tempfile.TemporaryDirectory,
    with the following differences:

    - the default value for prefix is set to ``pyf_``,
    - it has an extra attribute '.path' returning the directory name as a Path,
    - the context manager returns a Path instead of a str,
    - the context wrapper can automatically change into the tempdir
    - the context manager automatically changes back to the original workdir

    """
    def __init__(self, suffix=None, prefix='pyf_', dir=None, chdir=False, keep=False):
        super().__init__(suffix, prefix, dir)
        self.prev = os.getcwd()
        self.chdir = chdir
        self.keep = keep

    @property
    def path(self):
        return Path(self.name)

    def __enter__(self):
        if self.chdir:
            os.chdir(self.name)
        return self.path

    def __exit__(self, *args):
        os.chdir(self.prev)
        if not self.keep:
            super().__exit__(*args)


def TempFile(*args, **kargs):
    """Return a temporary file that can be used as a context manager.

    This is a wrapper around Python's tempfile.NamedTemporaryFile,
    with the difference that the returned object has an extra attribute
    '.path', returning the file name as a Path.
    """
    tmpfile = tempfile.NamedTemporaryFile(*args, **kargs)
    tmpfile.path = Path(tmpfile.name)
    return tmpfile


class ChDir:
    """A context manager to temporarily change the working directory.

    The context manager changes the current working directory and guarantees
    to come back to the previous, even if an exception occurs.

    Parameters
    ----------
    dirname: :term:`path_like` | None
        The relative or absolute path name of the directory to change into.
        If the directory does not exist, it will be created, unless
        ``create=False`` was specified.
        If None, a temporary working directory will be created and used,
        and be deleted with all its contents on leaving the contex.
    create: bool
        If True(default), the directory (including missing parents) will be
        created if it does not exist.
        If False, and a path was specified for ``dirname``, the directory
        should exist and be accessible.

    Returns
    -------
    context
        A context manager object that can be used in a with statement.
        On entry , it changes into the specified or temporary directory,
        and on exit it change back to the previous working directory.

    Raises
    ------
    OSError or subclass
        If the specified path can no be changed into or can not be created.

    Examples
    --------
    >>> olddir = os.getcwd()
    >>> with ChDir() as newdir:
    ...    print(os.getcwd()==newdir, newdir!=olddir)
    True True
    >>> os.getcwd()==olddir
    True

    """

    def __init__(self, dirname=None, create=True):
        self.saved = Path.cwd()
        if dirname is None:
            self.tempdir = tempfile.TemporaryDirectory()
            self.path = Path(self.tempdir.name)
        else:
            self.tempdir = None
            self.path = Path(dirname)
            if not self.path.exists():
                self.path.mkdir(parents=True)

    def __enter__(self):
        os.chdir(self.path)
        if self.tempdir is not None:
            self.tempdir.__enter__()
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.saved)
        if self.tempdir is not None:
            return self.tempdir.__exit__(exc_type, exc_val, exc_tb)
        return False


##########################################################################
##  ZIP Files
#####################


def zipList(filename):
    """List the files in a zip archive

    Returns a list of file names
    """
    from zipfile import ZipFile
    zfil = ZipFile(filename, 'r')
    return zfil.namelist()


def zipExtract(filename, members=None):
    """Extract the specified member(s) from the zip file.

    The default extracts all.
    """
    from zipfile import ZipFile
    zfil = ZipFile(filename, 'r')
    zfil.extractall(members=members)


###################### locale ###################

def setSaneLocale(localestring=''):
    """Set a sane local configuration for LC_NUMERIC.

    `localestring` is the locale string to be set, e.g. 'en_US.UTF-8' or
    'C.UTF-8' for no locale.

    Sets the ``LC_ALL`` locale to the specified string if that is not empty,
    and (always) sets ``LC_NUMERIC`` and ``LC_COLLATE`` to 'C.UTF-8'.

    Changing the LC_NUMERIC setting is a very bad idea! It makes floating
    point values to be read or written with a comma instead of a the decimal
    point. Of course this makes input and output files completely incompatible.
    You will often not be able to process these files any further and
    create a lot of troubles for yourself and other people if you use an
    LC_NUMERIC setting different from the standard.

    Because we do not want to help you shoot yourself in the foot, this
    function always sets ``LC_NUMERIC`` back to a sane 'C' value and we
    call this function when pyFormex is starting up.
    """
    import locale
    if localestring:
        locale.setlocale(locale.LC_ALL, localestring)
    locale.setlocale(locale.LC_ALL, 'C.UTF-8')


##########################################################################
## Text conversion  tools ##
############################


def rreplace(source, old, new, count=1):
    """Replace substrings starting from the right.

    Replaces count occurrences of old substring with a new substring.
    This is like str.replace, but counting starts from the right.
    The default count=1 replaces only the last occurrence,
    and is identical to str.replace (which is then preferred).

    Parameters
    ----------
    source: str
        The input string. It can be subclass of str, e.g. :class:`~path.Path`.
    old: str
        The substring to be replaced.
    new: str
        The string to replace old.
    count: int
        The maximum number of replacements.

    Returns
    -------
    str
        The string with the replacements made. If source was a subclass
        of str, the returned string will be of the same subclass.

    Examples
    --------
    >>> print(rreplace('abababa', 'ab', '+de'))
    abab+dea
    >>> print(rreplace('abababa', 'ab', '+de', 2))
    ab+de+dea
    >>> for i in (0, 1, 2, 3, 4, -1):
    ...     print(f"{i}: {rreplace('abcabcabc', 'ab', '-ef', i)}")
    0: abcabcabc
    1: abcabc-efc
    2: abc-efc-efc
    3: -efc-efc-efc
    4: -efc-efc-efc
    -1: -efc-efc-efc
    >>> rreplace(Path('dirname/filename.ext'), 'name.e', 'name00.n')
    Path('dirname/filename00.nxt')
    """
    return source.__class__(new.join(source.rsplit(old, count)))


def to_str(s):
    """Silently convert bytes to str.

    The input is either str or bytes. The output is always str.
    """
    if isinstance(s, str):
        return s
    elif isinstance(s, bytes):
        return bytes.decode(s)
    else:
        raise ValueError("Input should be str or bytes")


def strNorm(s):
    """Normalize a string.

    Text normalization removes all '&' characters and converts it to lower case.

    >>> strNorm("&MenuItem")
    'menuitem'

    """
    return str(s).replace('&', '').lower()


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')


def slugify(text, delim='-'):
    """Convert a string into a URL-ready readable ascii text.

    Example:
    >>> slugify("http://example.com/blog/[Some] _ Article's Title--")
    'http-example-com-blog-some-article-s-title'
    >>> slugify("&MenuItem")
    'menuitem'

    """
    import unicodedata
    text = str(text)
    result = []
    for word in _punct_re.split(text.lower()):
        word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            word = to_str(word)
            result.append(word)
    return delim.join(result)

###################### ReST conversion ###################


if Module.has('docutils', quiet=True):
    def rst2html(text, writer='html'):
        from docutils.core import publish_string
        #warnings.filterwarnings("ignore", category=DeprecationWarning)
        try:
            s = publish_string(text, writer_name=writer)
        except Exception as e:
            print(e)
            return text
        return s
        #warnings.filterwarnings("default", category=DeprecationWarning)
else:
    def rst2html(text, writer='html'):
        return """.. note:
   This is a reStructuredText message, but it is currently displayed
   as plain text, because it could not be converted to html.
   If you install python-docutils, you will see this text (and other
   pyFormex messages) in a much nicer layout!

""" + text


def convertText(text, format=''):
    """Convert a text to a format recognized by Qt.

    Input text format is plain, html or reStructuredText.
    Output text format is plain or html, with reStructuredText being
    converted to html.

    Parameters
    ----------
    text: str
        A multiline string in one of the supported formats:
        plain text, html or reStructuredText.
    format: str, optional
        The format of the text: one of 'plain', 'html' ot 'rest'. The
        default '' will autorecognize the supported formats.

    Returns
    -------
    text: str
        The converted text, being either plain or html.

    Notes
    -----
    For the conversion of reStructuredText to work,
    the Python docutils have to be installed on the system.

    Examples
    --------
    >>> convertText('''..
    ...     Header
    ...     ------
    ... ''').startswith('<?xml')
    True
    """
    if format not in ['plain', 'html', 'rest']:
        # autorecognition of 'rest'
        if isinstance(text, str) and text.startswith('..'):
            format = 'rest'

    # conversion
    if format == 'rest' and pf.cfg['gui/rst2html']:
        # Try conversion to html
        text = rst2html(text)

    if isinstance(text, bytes):
        text = text.decode()

    return text


def forceReST(text, underline=False):
    """Convert a text string to have it recognized as reStructuredText.

    Parameters
    ----------
    text: str
        A multiline string with some text that is formated as
        reStructuredText.
    underline: bool
        If True, the first line of the text will be underlined to make
        it a header in the reStructuredText.

    Returns
    -------
    str:
        The input text with two lines prepended: a line with '..'
        and a blank line. The pyFormex text display functions will then
        recognize the text as being reStructuredText.
        Since the '..' starts a comment in reStructuredText, the extra
        lines are not displayed. If underline=True, an extra line is
        added below the (original) first line, to make that line appear
        as a header.

    Examples
    --------
    >>> print(forceReST('Header\\nBody', underline=True))
    ..
    <BLANKLINE>
    Header
    ------
    Body

    """
    if underline:
        text = underlineHeader(text)
    return "..\n\n" + text


def underlineHeader(s, c='-'):
    """Underline the first line of a text.

    Parameters
    ----------
    s: str
        A multiline string.
    c: char, optional
        The character to use for underlining. Default is '-'.

    Returns
    -------
    str:
        A multiline string with the original text plus an extra line
        inserted below the first line. The new line has the same length
        as the first, but all characters are equal to the specified char.

    >>> print(underlineHeader("Hello World"))
    Hello World
    -----------
    """
    i = s.find('\n')
    if i < 0:
        i = len(s)
    return s[:i] + '\n' + c*i + s[i:]


def sameLength(lines, length=-1, adjust='l'):
    """Make a sequence of strings the same length.

    Parameters
    ----------
    lines: list of str
        A sequence of single line strings.
    length: int
        The required length of the lines. If negative, the length is
        set to the maximum input line length.
    adjust: 'l' | 'c' | 'r'
        How the input lines are adjusted to respectively the left,
        the center or the right of the total length of the line.

    Examples
    --------
    >>> sameLength(['a', 'bb', 'ccc'])
    ['a  ', 'bb ', 'ccc']
    >>> sameLength(['a', 'bb', 'ccc'], adjust='c')
    [' a ', ' bb', 'ccc']
    >>> sameLength(['a', 'bb', 'ccc'], adjust='r')
    ['  a', ' bb', 'ccc']
    >>> sameLength(['a', 'bb', 'ccc'], length=2)
    ['a ', 'bb', 'cc']
    """
    if length < 0:
        length = max([len(l) for l in lines])
    _adjust = {'c': str.center, 'l': str.ljust, 'r': str.rjust}[adjust]
    return [_adjust(line, length) if len(line) <= length else line[:length]
            for line in lines]


def framedText(text,
               padding=[0, 2, 0, 2], border=[1, 2, 1, 2], margin=[0, 0, 0, 0],
               borderchar='####', adjust='l'):
    """Create a text with a frame around it.

    Parameters
    ----------
    padding: list of int
        Number of blank spaces around text, at the top, right, bottom, left.
    border: list of int
        Border width, at the top, right, bottom, left.
    margin: list of int
        Number of blank spaces around border, at the top, right, bottom, left.
    borderchar: str
        Border charater, at the top, right, bottom, left.
    width: int
        Intended width of the
    adjust: 'l' | 'c' | 'r'
        Adjust the text to the left, center or right.

    Returns
    -------
    str:
        A multiline string with the formatted framed text.

    Examples
    --------
    >>> print(framedText("Hello World,\\nThis is me calling",adjust='c'))
    ##########################
    ##     Hello World,     ##
    ##  This is me calling  ##
    ##########################
    >>> print(framedText("Hello World,\\nThis is me calling",margin=[1,0,0,3]))
    <BLANKLINE>
       ##########################
       ##  Hello World,        ##
       ##  This is me calling  ##
       ##########################
    """
    lines = text.splitlines()
    maxlen = max([len(l) for l in lines])
    lines = sameLength(lines, maxlen)
    prefix = borderchar[3]*border[3] + ' '*padding[3]
    suffix = ' '*padding[1] + borderchar[1]*border[1]
    width = len(prefix) + maxlen + len(suffix)
    lmargin = ' '*margin[3]
    prefix = lmargin + prefix
    paddingline = prefix + ' '*maxlen + suffix
    borderline = lmargin + borderchar[0]*width
    s = []
    for i in range(margin[0]):
        s.append('')
    for i in range(border[0]):
        s.append(borderline)
    for i in range(padding[0]):
        s.append(paddingline)
    for l in lines:
        s.append(prefix + l + suffix)
    for i in range(padding[2]):
        s.append(paddingline)
    for i in range(border[2]):
        s.append(borderline)
    for i in range(margin[2]):
        s.append('')
    return '\n'.join(s)


def prefixText(text, prefix):
    """Add a prefix to all lines of a text.

    Parameters
    ----------
    text: str
        A multiline string with the input text.
    prefix: str
        A string to be inserted at the start of all lines of text.

    Returns
    -------
    str
        A multiline string with the input lines prefixed with prefix.

    Examples
    --------
    >>> print(prefixText("line1\\nline2","** "))
    ** line1
    ** line2

    """
    return '\n'.join([prefix+line for line in text.split('\n')])


###################### file conversion ###################


def dos2unix(infile):
    """Convert a text file to unix line endings."""
    return system(f"sed -i 's|$|\\r|' {infile}")


def unix2dos(infile, outfile=None):
    """Convert a text file to dos line endings."""
    return system(f"sed -i 's|\\r||' {infile}")


def gzip(filename, gzipped=None, remove=True, level=5, compr='gz'):
    r"""Compress a file in gzip/bzip2 format.

    Parameters
    ----------
    filename: :term:`path_like`
        The input file name.
    gzipped: :term:`path_like`, optional
        The output file name. If not specified, it will be set to
        the input file name + '.' + `compr`. An existing output file will be
        overwritten.
    remove: bool
        If True (default), the input file is removed after
        successful compression.
    level: int 1..9
        The gzip/bzip2 compression level.
        Higher values result in smaller files, but require longer compression
        times. The default of 5 gives already a fairly good compression ratio.
    compr: 'gz' | 'bz2'
        The compression algorithm to be used.
        The default is 'gz' for gzip compression. Setting to 'bz2' will use
        bzip2 compression.
    Returns
    -------
    :class:`Path`
        The path of the compressed file.

    Examples
    --------
    >>> f = Path('./test_gzip.out')
    >>> f.write_text('This is a test\n'*100)
    1500
    >>> print(f.size)
    1500
    >>> g = gzip(f)
    >>> print(g)
    test_gzip.out.gz
    >>> print(g.size)
    60
    >>> f.exists()
    False
    >>> f = gunzip(g)
    >>> f.exists()
    True
    >>> print(f.read_text().split('\n')[50])
    This is a test
    >>> g.exists()
    False

    """
    filename = Path(filename)
    if gzipped is None:
        gzipped = filename + '.' + compr
    if compr == 'gz':
        import gzip
        gz = gzip.GzipFile(gzipped, 'wb', compresslevel=level)
    elif compr == 'bz2':
        import bz2
        gz = bz2.BZ2File(gzipped, 'wb', compresslevel=level)
    else:
        raise ValueError("`compr` should be 'gz' or 'bz2'")
    with open(filename, 'rb') as fil:
        gz.write(fil.read())
    gz.close()
    if remove:
        filename.remove()
    return gzipped


def gunzip(filename, unzipped=None, remove=True, compr='gz'):
    """Uncompress a file in gzip/bzip2 format.

    Parameters
    ----------
    filename: :term:`path_like`
        The compressed input file name (usually ending in '.gz' or
        '.bz2').
    unzipped: :term:`path_like`, optional
        The output file name. If not provided and `filename` ends with
        '.gz' or '.bz2', it will be set to the `filename` with the '.gz' or
        '.bz2' removed.
        If not provided and `filename` does not end in '.gz' or '.bz2',
        or if an empty string is provided, the name of a temporary file is
        generated. Since you will normally want to read something from the
        decompressed file, this temporary file is not deleted after closing.
        It is up to the user to delete it (using the returned file name) when
        the file has been dealt with.
    remove: bool
        If True (default), the input file is removed after successful
        decompression. You probably want to set this to False when
        decompressing to a temporary file.
    compr: 'gz' | 'bz2'
        The compression algorithm used in the input file.
        If not provided, it is automatically set from the extension of the
        `filename` if that is either '.gz' or '.bz2', or else the default 'gz'
        is used.

    Returns
    -------
    :class:`Path`
        The name of the uncompressed file.

    Examples
    --------
    See `gzip`.
    """
    filename = Path(filename)
    if filename.suffix in ['.gz', '.bz2']:
        compr = filename.suffix[1:]
    if compr == 'gz':
        import gzip
        gz = gzip.GzipFile(filename, 'rb')
    elif compr == 'bz2':
        import bz2
        gz = bz2.BZ2File(filename, 'rb')
    else:
        raise ValueError("`compr` should be 'gz' or 'bz2'")
    if unzipped is None and filename.endswith('.'+compr):
        unzipped = filename.without_suffix
    if unzipped:
        fil = open(unzipped, 'wb')
    else:
        fil = TempFile(prefix='gunzip-', delete=False)
        unzipped = fil.name
    fil.write(gz.read())
    gz.close()
    fil.close()
    if remove:
        filename.remove()
    return unzipped


class File:
    """Transparent file compression.

    This class is a context manager providing transparent file compression
    and decompression. It is commonly used in a `with` statement, as follows::

      with File('filename.ext','w') as f:
          f.write('something')
          f.write('something more')

    This will create an uncompressed file with the specified name, write some
    things to the file, and close it. The file can be read back similarly::

      with File('filename.ext','r') as f:
          for line in f:
              print(f)

    Because File is a context manager, the file is closed automatically when
    leaving the `with` block.

    By specifying a filename ending with '.gz' or '.bz2', the file will be
    compressed (on writing) or decompressed (on reading) automatically.
    The code can just stay the same as above.

    Parameters
    ----------
    filename: :term:`path_like`
        Path of the file to open.
        If the filename ends with '.gz' or '.bz2', transparent (de)compression
        will be used, with gzip or bzip2 compression algorithms respectively.
    mode: str
        File open mode: 'r' for read, 'w' for write or 'a' for
        append mode. See also the Python documentation for the
        :func:`.open` builtin function.
        For compressed files, append mode is not yet available.
    compr: 'gz' | 'bz2'
        The compression algorithm to be used: gzip or bzip2.
        If not provided and the file name ends with '.gz' or '.bz2',
        `compr` is set automatically from the extension.
    level: int (1..9)
        Compression level for gzip/bzip2.
        Higher values result in smaller files, but require longer compression
        times. The default of 5 gives already a fairly good compression ratio.
    delete_temp: bool
        If True (default), the temporary files needed to
        do the (de)compression are deleted when the File instance is closed.


    The File class can also be used outside a ``with`` statement. In that case
    the user has to open and close the File himself. The following are more
    or less equivalent with the above examples (the ``with`` statement is
    better at handling exceptions)::

      fil = File('filename.ext','w')
      f = fil.open()
      f.write('something')
      f.write('something more')
      fil.close()

    This will create an uncompressed file with the specified name, write some
    things to the file, and close it. The file can be read back similarly::

      fil = File('filename.ext','r')
      f = fil.open()
      for line in f:
          print(f)
      fil.close()

    """

    def __init__(self, filename, mode, compr=None, level=5, delete_temp=True):
        """Initialize the File instance"""
        filename = Path(filename)
        if compr is None:
            if filename.suffix in ['.gz', '.bz2']:
                # A recognized compression format
                compr = filename.suffix[1:]

        self.name = filename
        self.tmpfile = None
        self.tmpname = None
        self.mode = mode
        self.compr = compr
        self.level = level
        self.delete = delete_temp
        self.file = None


    def open(self):
        """Open the File in the requested mode.

        This can be used to open a File object outside a `with`
        statement. It returns a Python file object that can be used
        to read from or write to the File. It performs the following:

        - If no compression is used, ope the file in the requested mode.
        - For reading a compressed file, decompress the file to a temporary
          file and open the temporary file for reading.
        - For writing a compressed file, open a tem[porary file for writing.

        See the documentation for the :class:`File` class for an example of
        its use.
        """
        if not self.compr:
            # Open an uncompressed file:
            # - just open the file with specified mode
            self.file = open(self.name, self.mode)

        elif self.mode[0:1] in 'ra':
            # Open a compressed file in read or append mode:
            # - first decompress file
            self.tmpname = gunzip(self.name, unzipped='', remove=False)
            # - then open the decompressed file in read/append mode
            self.file = open(self.tmpname, self.mode)

        else:
            # Open a compressed file in write mode
            # - open a temporary file (to be compressed after closing)
            self.tmpfile = TempFile(prefix='File-', mode=self.mode, delete=False)
            self.tmpname = self.tmpfile.name
            self.file = self.tmpfile.file

        return self.file


    # this is needed to make this a context manager
    __enter__ = open


    def close(self):
        """Close the File.

        This can be used to close the File if it was not opened using a
        `with` statement. It performs the following:

        - The underlying file object is closed.
        - If the file was opened in write or append mode and compression is
          requested, the file is compressed.
        - If a temporary file was in use and delete_temp is True,
          the temporary file is deleted.

        See the documentation for the :class:`File` class for an example of
        its use.

        """
        self.file.close()
        if self.compr and self.mode[0:1] in 'wa':
            # compress the resulting file
            gzip(self.tmpname, gzipped=self.name, remove=True,
                 compr=self.compr, level=self.level)
        if self.tmpname and self.delete:
            Path(self.tmpname).remove()


    def __exit__(self, exc_type, exc_value, traceback):
        """Close the File

        """
        if exc_type is None:
            self.close()
            return True

        else:
            # An exception occurred
            if self.file:
                self.file.close()

            if self.tmpfile:
                self.tmpfile.close()

            if self.tmpname and self.delete:
                Path(self.tmpname).remove()

            return False


    def reopen(self, mode='r'):
        """Reopen the file, possibly in another mode.

        This allows e.g. to read back data from a just saved file
        without having to destroy the File instance.

        Returns the open file object.
        """
        self.close()
        self.mode = mode
        return self.open()


# These two functions are undocumented for a reason. Believe me! BV
def splitme(s):  # noqa: E302
    return s[::2], s[1::2]
def mergeme(s1, s2):  # noqa: E302
    return ''.join([a+b for a, b in zip(s1, s2)])


def timeEval(s, glob=None):
    """Return the time needed for evaluating a string.

    s is a string with a valid Python instructions.
    The string is evaluated using Python's eval() and the difference
    in seconds between the current time before and after the evaluation
    is printed. The result of the evaluation is returned.

    This is a simple method to measure the time spent in some operation.
    It should not be used for microlevel instructions though, because
    the overhead of the time calls. Use Python's timeit module to measure
    microlevel execution time.
    """
    start = time.time()
    res = eval(s, glob)
    stop = time.time()
    print(f"Timed evaluation: {stop-start} seconds")
    return res


def countLines(fn):
    """Return the number of lines in a text file."""
    P = system(["wc", fn])
    if P.returncode == 0:
        return int(P.stdout.split()[0])
    else:
        return 0


##########################################################################
##  Miscellaneous            ##
###############################

def userName():
    """Find the name of the user."""
    import getpass
    return getpass.getuser()


def isString(o):
    """Test if an object is a string (ascii or unicode)"""
    return isinstance(o, (str, bytes))


def isFile(o):
    """Test if an object is a file"""
    import io
    return isinstance(o, io.IOBase)


def is_script(appname):
    """Checks whether an application name is rather a script name

    Parameters
    ----------
    appname: str
        The name of a script file or an app.

    Returns
    -------
    bool:
        True if appname ends with '.py' or '.pye', or contains a '/'.
    """
    appname = str(appname)
    return appname.endswith('.py') or appname.endswith('.pye') or '/' in appname


def is_app(appname):
    return not is_script(appname)


def getDocString(scriptfile):
    """Return the docstring from a script file.

    This actually returns the first multiline string (delimited by
    triple double quote characters) from the file.
    It does relies on the script file being structured properly and
    indeed including a doctring at the beginning of the file.
    """
    fil = open(scriptfile, 'r')
    s = fil.read()
    i = s.find('"""')
    if i >= 0:
        j = s.find('"""', i+1)
        if j >= i+3:
            return s[i+3:j]
    return ''


def hsorted(l):
    """Sort a list of strings in human order.

    When human sort a list of strings, they tend to interprete the
    numerical fields like numbers and sort these parts numerically,
    instead of the lexicographic sorting by the computer.

    Returns the list of strings sorted in human order.

    Example:
    >>> hsorted(['a1b','a11b','a1.1b','a2b','a1'])
    ['a1', 'a1.1b', 'a1b', 'a2b', 'a11b']
    """
    from pyformex.path import hsortkey
    return sorted(l, key=hsortkey)


def numsplit(s):
    """Split a string in numerical and non-numerical parts.

    Returns a series of substrings of s. The odd items do not contain
    any digits. The even items only contain digits.
    Joined together, the substrings restore the original.

    The number of items is always odd: if the string ends or starts with a
    digit, the first or last item is an empty string.

    Example:

    >>> print(numsplit("aa11.22bb"))
    ['aa', '11', '.', '22', 'bb']
    >>> print(numsplit("11.22bb"))
    ['', '11', '.', '22', 'bb']
    >>> print(numsplit("aa11.22"))
    ['aa', '11', '.', '22', '']
    """
    return _re_digits.split(s)


def splitDigits(s, pos=-1):
    """Split a string at a sequence of digits.

    The input string is split in three parts, where the second part is
    a contiguous series of digits. The second argument specifies at which
    numerical substring the splitting is done. By default (pos=-1) this is
    the last one.

    Returns a tuple of three strings, any of which can be empty. The
    second string, if non-empty is a series of digits. The first and last
    items are the parts of the string before and after that series.
    Any of the three return values can be an empty string.
    If the string does not contain any digits, or if the specified splitting
    position exceeds the number of numerical substrings, the second and
    third items are empty strings.

    Example:

    >>> splitDigits('abc123')
    ('abc', '123', '')
    >>> splitDigits('123')
    ('', '123', '')
    >>> splitDigits('abc')
    ('abc', '', '')
    >>> splitDigits('abc123def456fghi')
    ('abc123def', '456', 'fghi')
    >>> splitDigits('abc123def456fghi',0)
    ('abc', '123', 'def456fghi')
    >>> splitDigits('123-456')
    ('123-', '456', '')
    >>> splitDigits('123-456',2)
    ('123-456', '', '')
    >>> splitDigits('')
    ('', '', '')
    """
    g = numsplit(s)
    n = len(g)
    i = 2*pos
    if i >= -n and i+1 < n:
        if i >= 0:
            i += 1
        return ''.join(g[:i]), g[i], ''.join(g[i+1:])
    else:
        return s, '', ''

######################## Useful classes ##################

class Counter:
    def __init__(self, start=0, step=1):
        self.nr = start
        self.step = step

    def peek(self):
        return self.nr

    def __next__(self):
        nr = self.nr
        self.nr += self.step
        return nr

    __call__ = __next__


class NameSequence:
    """A class for autogenerating sequences of names.

    Sequences of names are autogenerated by combining a fixed string with
    a numeric part. The latter is incremented at each creation of a new
    name (by using the next() function or by calling the NameSequence).

    Parameters
    ----------
    template: str
        Either a template to generate the names, or an example name from
        which the template can be derived. If the string contains a '%'
        character, it is considered a template and will be used as such.
        It must be a valid template to format a single int value. For
        example, a template 'point-%d' with a value 5 will generate a name
        'point-5'.

        If the string does not contain a '%' character, a template is generated
        as follows. The string is split in three parts (prefix, numeric,
        suffix), where numeric only contains digits and suffix does not contain
        any digits. Thus, numeric is the last numeric part in the string.
        Use ``ext`` if the variable part is not the last numeric part of names.
        If the string does not contain any numeric part, it is split as a file
        name in stem and suffix, and '-0' is appended to the stem. Thus,
        'point.png' will be treated like 'point-0.png'. Finally, if the string
        is empty, it is replaced with '0'. To create the template, the
        numeric part is replaced with a '%0#d' format (where # is the
        length of the numeric part, concatened again with prefix and suffix,
        and ``ext`` is appended. Also, the start value is set to the numeric
        part (unless a nonzero start value is provided).
    ext: str, optional
        If provided, this is an invariable string appended to the template.
        It is mostly useful when providing a full name as ``template`` and
        the variable numeric part is not the last numeric part in the name.
        For example, NameSequence('x1', '.5a') will generate names 'x1.5a',
        'x2.5a', ...
    start: int, optional
        Starting value for the numerical part. If ``template`` contains a full
        name, it will only be acknowledged if nonzero.
    step: int, optional
        Step for incrementing the numerical value.

    Notes
    -----
    If N is a NameSequence, then next(N) and N() are equivalent.

    Examples
    --------
    >>> N = NameSequence('obj')
    >>> next(N)
    'obj-0'
    >>> N()
    'obj-1'
    >>> [N() for i in range(3)]
    ['obj-2', 'obj-3', 'obj-4']
    >>> N.peek()
    'obj-5'
    >>> N()
    'obj-5'
    >>> N.template
    'obj-%d'
    >>> N = NameSequence('obj-%03d', start=5)
    >>> [next(N) for i in range(3)]
    ['obj-005', 'obj-006', 'obj-007']
    >>> N = NameSequence('obj-005')
    >>> [next(N) for i in range(3)]
    ['obj-005', 'obj-006', 'obj-007']
    >>> N = NameSequence('abc.98', step=2)
    >>> [next(N) for i in range(3)]
    ['abc.98', 'abc.100', 'abc.102']
    >>> N = NameSequence('abc-8x.png')
    >>> [next(N) for i in range(3)]
    ['abc-8x.png', 'abc-9x.png', 'abc-10x.png']
    >>> N.template
    'abc-%01dx.png'
    >>> N.glob()
    'abc-*x.png'
    >>> next(NameSequence('abc','.png'))
    'abc-0.png'
    >>> next(NameSequence('abc.png'))
    'abc-0.png'
    >>> N = NameSequence('/home/user/abc23','5.png')
    >>> [next(N) for i in range(2)]
    ['/home/user/abc235.png', '/home/user/abc245.png']
    >>> N = NameSequence('')
    >>> next(N), next(N)
    ('0', '1')
    >>> N = NameSequence('12')
    >>> next(N), next(N)
    ('12', '13')

    """
    def __init__(self, template, ext='', start=0, step=1):
        """Initialize a new NameSequence"""
        self.nr = int(start)
        self.step = int(step)
        if '%' in template:
            self.template = template
        else:
            self.set_template_from_name(template, ext)
            if start != 0:
                self.nr = int(start)
        try:
            s = self.peek()
        except:
            raise ValueError("Invalid parameters for NameSeq")

    def peek(self):
        """Peek at the next name"""
        return self.template % self.nr

    def __next__(self):
        """Return the next name"""
        name = self.peek()
        self.nr += self.step
        return name

    __call__ = __next__

    def set_template_from_name(self, name, ext=''):
        """Set template and current number from a given name"""
        prefix, number, suffix = splitDigits(name)
        if len(number) > 0:
            self.nr = int(number)
            fmt = f"%0{len(number)}d"
        else:
            self.nr = 0
            if name:
                p = Path(name)
                prefix, suffix = p.stem, p.suffix
                fmt = "-%d"
            else:
                prefix = suffix = ''
                fmt = "%d"
        self.template = prefix+fmt+suffix+ext

    def glob(self):
        """Return a UNIX glob pattern for the generated names.

        A NameSequence is often used as a generator for file names.
        The glob() method returns a pattern that can be used in a
        UNIX-like shell command to select all the generated file names.
        """
        m = re.match(r'(.*)%\d*d(.*)', self.template)
        if m:
            return f"{m.group(1)}*{ m.group(2)}"
        else:
            raise ValueError("Invalid template")


################### automatic naming of objects ##########################

_autoname = {}

def autoName(clas):
    """Return the autoname class instance for objects of type clas.

    This allows for objects of a certain class to be automatically
    named throughout pyFormex.

    Parameters
    ----------
    clas: str or class or object
        The object class name. If a str, it is the class name. If a class,
        the name is found from it. If an object, the name is taken from
        the object's class. In all cases the name is converted to lower
        case

    Returns
    -------
    NameSequence instance
        A NameSequence that will generate subsequent names corresponding
        with the specified class.

    Examples
    --------
    >>> from pyformex.formex import Formex
    >>> F = Formex()
    >>> print(next(autoName(Formex)))
    formex-0
    >>> print(next(autoName(F)))
    formex-1
    >>> print(next(autoName('Formex')))
    formex-2

    """
    if isinstance(clas, str):
        name = clas
    else:
        try:
            name = clas.__name__
        except Exception:
            try:
                name = clas.__class__.__name__
            except Exception:
                raise ValueError("Expected an instance, class or string")
    name = name.lower()
    if name not in _autoname:
        _autoname[name] = NameSequence(name+'-0')
    return _autoname[name]


def prefixDict(d, prefix=''):
    """Prefix all the keys of a dict with the given prefix.

    Parameters
    ----------
    d: dict
        A dict where all keys are strings.
    prefix: str
        A string to prepend to all keys in the dict.

    Returns
    -------
    dict
        A dict with the same contents as the input, but where all keys
        have been prefixed with the given prefix string.

    Examples
    --------
    >>> prefixDict({'a':0,'b':1},'p_')
    {'p_a': 0, 'p_b': 1}
    """
    return dict([(prefix+k, d[k]) for k in d])


def subDict(d, prefix='', strip=True, remove=False):
    """Return a dict with the items whose key starts with prefix.

    Parameters
    ----------
    d: dict
        A dict where all the keys are strings.
    prefix: str
        The string that is to be found at the start of the keys.
    strip: bool
        If True (default), the prefix is stripped from the keys.

    Returns
    -------
    dict
        A dict with all the items from ``d`` whose key starts
        with ``prefix``. The keys in the returned dict will have the prefix
        stripped off, unless strip=False is specified.

    Examples
    --------
    >>> subDict({'p_a':0,'q_a':1,'p_b':2}, 'p_')
    {'a': 0, 'b': 2}
    >>> subDict({'p_a':0,'q_a':1,'p_b':2}, 'p_', strip=False)
    {'p_a': 0, 'p_b': 2}
    >>> a = {'p_a':0,'q_a':1,'p_b':2}
    >>> b = subDict(a, 'p_', remove=True, strip=False)
    >>> a, b
    ({'q_a': 1}, {'p_a': 0, 'p_b': 2})
    """
    keys = [k for k in d if k.startswith(prefix)]
    if strip:
        subd = dict([(k.replace(prefix, '', 1), d[k]) for k in keys])
    else:
        subd = dict([(k, d[k]) for k in keys])
    if remove:
        for k in keys:
            del d[k]
    return subd


def selectDict(d, keys, remove=False):
    """Return a dict with the items whose key is in keys.

    Parameters
    ----------
    d: dict
        The dict to select items from.
    keys: set of str
        The keys to select from ``d``. This can be a set or list of key
        values, or another dict, or any object having the ``key in object``
        interface.
    remove: bool
        If True, the selected keys are removed from the input dict.

    Returns
    -------
    dict
        A dict with all the items from ``d`` whose key is in ``keys``.

    See Also
    --------
    removeDict: the complementary operation, returns items not in ``keys``.

    Examples
    --------
    >>> d = dict([(c,c*c) for c in range(4)])
    >>> print(d)
    {0: 0, 1: 1, 2: 4, 3: 9}
    >>> selectDict(d,[2,0])
    {2: 4, 0: 0}
    >>> print(d)
    {0: 0, 1: 1, 2: 4, 3: 9}
    >>> selectDict(d,[2,0,6],remove=True)
    {2: 4, 0: 0}
    >>> print(d)
    {1: 1, 3: 9}
    """
    keys = [k for k in keys if k in d]
    sel = dict([(k, d[k]) for k in keys])
    if remove:
        for k in keys:
            del d[k]
    return sel


def removeDict(d, keys):
    """Return a dict with the specified keys removed.

    Parameters
    ----------
    d: dict
        The dict to select items from.
    keys: set of str
        The keys to select from ``d``. This can be a set or list of key
        values, or another dict, or any object having the ``key in object``
        interface.

    Returns
    -------
    dict
        A dict with all the items from ``d`` whose key is not in ``keys``.

    See Also
    --------
    selectDict: the complementary operation returning the items in ``keys``

    Examples
    --------
    >>> d = dict([(c,c*c) for c in range(6)])
    >>> removeDict(d,[4,0])
    {1: 1, 2: 4, 3: 9, 5: 25}
    """
    return dict([(k, d[k]) for k in set(d)-set(keys)])


def mutexkeys(d, keys):
    """Enforce a set of mutually exclusive keys in a dictionary.

    This makes sure that d has only one of the specified keys.
    It modifies the dictionary inplace.

    Parameters
    ----------
    d: dict
        The input dictionary.
    keys:
        A list of dictionary keys that are mutually exclusive.

    >>> d = {'a':0, 'b':1, 'c':2}
    >>> mutexkeys(d, ['b', 'c', 'a'])
    >>> print(d)
    {'b': 1}
    """
    keep = None
    for k in keys:
        if k in d:
            keep = k
            break
    if keep:
        for k in keys:
            if k != keep:
                d.pop(k, None)


def refreshDict(d, src):
    """Refresh a dict with values from another dict.

    The values in the dict d are update with those in src.
    Unlike the dict.update method, this will only update existing keys
    but not add new keys.
    """
    d.update(selectDict(src, d))


def inverseDict(d):
    """Return the inverse of a dictionary.

    Returns a dict with keys and values interchanged.

    Example:

    >>> inverseDict({'a':0,'b':1})
    {0: 'a', 1: 'b'}
    """
    return dict([(d[k], k) for k in d])


def selectDictValues(d, values):
    """Return the keys in a dict which have a specified value

    - `d`: a dict where all the keys are strings.
    - `values`: a list/set of values.

    The return value is a list with all the keys from d whose value
    is in keys.

    Example:

    >>> d = dict([(c,c*c) for c in range(6)])
    >>> selectDictValues(d,range(10))
    [0, 1, 2, 3]
    """
    return [k for k in d if d[k] in values]


class DictDiff():
    """A class to compute the difference between two dictionaries

    Parameters
    ----------
    current_dict: dict
    past_dict: dict

    The differences are reported as sets of keys:
    - items added
    - items removed
    - keys same in both but changed values
    - keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.current_keys, self.past_keys = [
            set(d.keys()) for d in (current_dict, past_dict)]
        self.intersect = self.current_keys.intersection(self.past_keys)

    def added(self):
        """Return the keys in current_dict but not in past_dict"""
        return self.current_keys - self.intersect

    def removed(self):
        """Return the keys in past_dict but not in current_dict"""
        return self.past_keys - self.intersect

    def changed(self):
        """Return the keys for which the value has changed"""
        return set(o for o in self.intersect
                   if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        """Return the keys with same value in both dicts"""
        return set(o for o in self.intersect
                   if self.past_dict[o] == self.current_dict[o])


    def equal(self):
        """Return True if both dicts are equivalent"""
        return len(self.added() | self.removed() | self.changed()) == 0


    def report(self):
        """Create a reports of the differences"""
        return(f"""Dict difference report:
    (1) items added : {', '.join(self.added())}
    (2) items removed : {', '.join(self.removed())}
    (3) keys same in both but changed values : {', '.join(self.changed())}
    (4) keys same in both and unchanged values : {', '.join(self.unchanged())}
""")


def listFonts(mono=False):
    """List the fonts known to the system.

    Parameters
    ----------
    mono: bool
        If True, only returns the monospace fonts. Default is to return all
        fonts.

    Returns
    -------
    list of :class:`Path`
        A list of the font files found on the system.

    Notes
    -----
    This uses the 'fc-list' command from the fontconfig package and will
    produce a warning if fontconfig is not installed.
    """
    cmd = "fc-list : file | sed 's|.*file=||;s|:||'"
    P = system(cmd, shell=True)
    if P.returncode:
        warning("fc-list could not find your font files.\n"
                "Maybe you do not have fontconfig installed?")
        fonts = []
    else:
        fonts = sorted([Path(f.strip()) for f in P.stdout.split('\n')])
        if len(fonts[0]) <= 1:
            fonts = fonts[1:]
    if mono:
        fonts = [f for f in fonts if is_valid_mono_font(f)]
    return fonts


def is_valid_mono_font(fontfile):
    """Filter valid monotype fonts

    Parameters
    ----------
    fontfile: Path
        Path of a font file.

    Returns
    -------
    bool
        True if the provided font file has a .ttf suffix, is a fixed width
        font and the font basename is not listed in the 'fonts/ignore'
        configuration variable.
    """
    from pyformex import freetype as ft
    return fontfile.suffix == '.ttf' and \
        fontfile.name not in pf.cfg['fonts/ignore'] and \
        ft.Face(fontfile).is_fixed_width


def defaultMonoFont():
    """Return a default monospace font for the system."""
    fonts = listFonts(mono=True)
    if not fonts:
        raise ValueError("I could not find any monospace font file on your system")
    for f in fonts:
        if f.endswith('DejaVuSansMono.ttf'):
            return f
    return fonts[0]


def listMonoFonts():
    """List only the monospace fonts

    See Also
    --------
    listFonts
    """
    return listFonts(mono=True)


#######################################################
##  Namespace  ##
#################

class Namespace(types.SimpleNamespace):
    """A SimpleNamespace subclass that also has dict access methods.

    The NameSpace class adds three dunder methods to the
    :class:`types.SimpleNamespace` class:
    __getitem__, __setitem__ and__delitem__.
    This allows the attributes also to be accessed with dict methods.
    Furthermore, it defines an _attrs method to get a list of the
    defined attributes.

    Examples
    --------
    >>> S = Namespace(a=0, b=1)
    >>> print(S)
    Namespace(a=0, b=1)
    >>> S['c'] = 2
    >>> S.a = 3
    >>> print(S)
    Namespace(a=3, b=1, c=2)
    >>> print(S.a, S['a'])
    3 3
    >>> del S.a
    >>> T = Namespace(**{'b':1, 'c':2})
    >>> print(S, T)
    Namespace(b=1, c=2) Namespace(b=1, c=2)
    >>> print(S == T)
    True
    >>> del S['c']
    >>> print(S == T)
    False
    >>> print(T._attrs())
    ['b', 'c']
    """
    def __getitem__(self, k):
        return self.__getattribute__(k)

    def __setitem__(self, k, v):
        self.__setattr__(k, v)

    def __delitem__(self, k):
        self.__delattr__(k)

    def _attrs(self):
        return list(self.__dict__)


###########################################################################


def execFile(f, *args, **kargs):
    with open(f, 'r') as fil:
        return exec(compile(fil.read(), f, 'exec'), *args, **kargs)


def interrogate(item):
    """Print useful information about item."""
    info = {}
    if hasattr(item, '__name__'):
        info["NAME:    "] = item.__name__
    if hasattr(item, '__class__'):
        info["CLASS:   "] = item.__class__.__name__
    info["ID:      "] = id(item)
    info["TYPE:    "] = type(item)
    info["VALUE:   "] = repr(item)
    info["CALLABLE:"] = callable(item)
    if hasattr(item, '__doc__'):
        doc = getattr(item, '__doc__')
        doc = doc.strip()   # Remove leading/trailing whitespace.
        firstline = doc.split('\n')[0]
        info["DOC:     "] = firstline
    for k in info:
        print(f"{k} {info[k]}")


def memory_report(keys=None):
    """Return info about memory usage"""
    import gc
    gc.collect()
    P = system('cat /proc/meminfo')
    res = {}
    for line in str(P.stdout).split('\n'):
        try:
            k, v = line.split(':')
            k = k.strip()
            v = v.replace('kB', '').strip()
            res[k] = int(v)
        except Exception:
            break
    res['MemUsed'] = res['MemTotal'] - res['MemFree'] - res['Buffers'] - res['Cached']
    if keys:
        res = selectDict(res, keys)
    return res


def memory_diff(mem0, mem1, tag=None):
    m0 = mem0['MemUsed']/1024.
    m1 = mem1['MemUsed']/1024.
    m2 = m1 - m0
    m3 = mem1['MemFree']/1024.
    print(f"{m0:10.1f} MB before; {m1:10.1f} MB after; "
          f"{m2:10.1f} MB used; {m3:10.1f} MB free; {tag}")


_mem_state = None


def memory_track(tag=None, since=None):
    global _mem_state
    if since is None:
        since = _mem_state
    new_mem_state = memory_report()
    if tag and _mem_state is not None:
        memory_diff(since, new_mem_state, tag)
    _mem_state = new_mem_state
    return _mem_state


def totalMemSize(o, handlers={}, verbose=False):
    """Return the approximate total memory footprint of an object.

    This function returns the approximate total memory footprint of an
    object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    Adapted from http://code.activestate.com/recipes/577504/
    """
    from sys import getsizeof, stderr
    from itertools import chain
    from collections import deque
    try:
        from reprlib import repr
    except ImportError:
        pass

    def dict_handler(d):
        return chain.from_iterable(d.items())

    all_handlers = {
        tuple: iter,
        list: iter,
        deque: iter,
        dict: dict_handler,
        set: iter,
        frozenset: iter,
    }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ in all_handlers:
            if isinstance(o, typ):
                handler = all_handlers[typ]
                s += sum([sizeof(i) for i in handler(o)])
                break
        return s

    return sizeof(o)


def memUsed():
    return memory_report()['MemUsed']


###########################################################################
####  Deprecated  #####

is_pyFormex = is_script


@deprecated_by('utils.globFiles', 'Path.glob')
def globFiles(pattern, sort=hsorted):
    return Path.glob(pattern)

@deprecated_by('utils.listAllFonts', 'utils.listFonts')
def listAllFonts():
    return listFonts()

@deprecated_by('utils.runCommand', 'utils.command')
def runCommand(cmd, timeout=None, shell=True, **kargs):
    P = command(cmd, timeout=timeout, shell=shell, **kargs)
    return P.returncode, P.stdout.rstrip('\n')

@deprecated_by('utils.removeTree', 'Path.removeTree')
def removeTree(path, top=True):
    Path(path).removeTree(top)

@deprecated_by('utils.removeFile', 'Path.remove')
def removeFile(filename):
    Path(filename).remove()

@deprecated_by('utils.mtime', 'Path.mtime')
def mtime(fn):
    return os.stat(fn).st_mtime

@deprecated_by('utils.listDirs', 'Path.dirs')
def listDirs(path):
    return Path(path).dirnames()

@deprecated_by('utils.listFiles', 'Path.files')
def listFiles(path):
    return Path(path).filenames()

@deprecated_by('utils.splitFilename', 'Path')
def splitFilename(path, *args, **kargs):
    p = Path(path)
    return p.parent, p.stem, p.suffix

@deprecated_by('utils.listTree', 'Path.listTree')
def listTree(path, *args, **kargs):
    return Path(path).listTree(*args, **kargs)

@deprecated_by('utils.tempName', 'Path.TempFile')
def tempName(*args, **kargs):
    return tempfile.mkstemp(*args, **kargs)[1]

@deprecated_by('utils.changeExt', 'Path.with_suffix')
def changeExt(path, ext, accept_ext=None, reject_ext=None):
    p = Path(path)
    oldext = p.suffix
    if ((accept_ext and oldext not in accept_ext)
            or (reject_ext and oldext in reject_ext)):
        return str(p) + ext
    else:
        return str(p.with_suffix(ext))

@deprecated_by('utils.normalizeFileType', 'Path.ftype')
def normalizeFileType(ftype):
    return ftype.lower().lstrip('.')

@deprecated_by('utils.fileTypeFromExt', 'Path.ftype or Path.filetype')
def fileTypeFromExt(fname):
    return Path(fname).filetype()

@deprecated_by('utils.fileTypeComprFromExt', 'Path.ftype_compr')
def fileTypeComprFromExt(fname):
    return Path(fname).ftype_compr()

@deprecated_by('utils.fileSize', 'Path.size')
def fileSize(fn):
    return Path(fn).size

####  Removed  ####

# tildeExpand = os.path.expanduser
# splitExt: replaced with fileSuffix
# listDir: was only used in listDirs & listFiles
# prefixFiles: use: [prefix / f for f in files]
# unPrefixFiles: use: [f.relative_to(prefix) for f in files]
# fileName: use: dir / (name+ext)
# fileSuffix: use Path.filetype
# currentScript
# dictStr: use repr(dict)
# procInfo, vmSize, memory_used: not useful

### End

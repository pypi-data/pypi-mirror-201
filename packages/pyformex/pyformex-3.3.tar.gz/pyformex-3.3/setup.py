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
#
"""Setup script for pyFormex

To change the install location, see the prefix and exec-prefix in setup.cfg.
To uninstall pyFormex: pyformex --remove
"""
import os
import sys

# Detect platform
if sys.version_info < (3, 7):
    raise RuntimeError("Python version is %s.%s but pyFormex requires "
                       ">= 3.7." % sys.version_info[:2])

import numpy as np
from setuptools import setup, Extension

# pyFormex release
__RELEASE__ = '3.3'


import setuptools.command.install_lib
_install_lib = setuptools.command.install_lib.install_lib
class install_lib(_install_lib):
    def finalize_options(self):
        print(f"INSTALL_DIR = {self.install_dir}")
        _install_lib.finalize_options(self)
        self.install_dir = os.path.join(self.install_dir,'pyformex-' + __RELEASE__)
        print(f"INSTALL_DIR = {self.install_dir}")


# define the things to include
import manifest

def print_msgs(msgs):
    """Print status messages"""
    print('*' * 75)
    for msg in msgs:
        print(msg)
    print('*' * 75)


def run_setup(options):

    # The acceleration libraries
    LIB_MODULES = ['misc_c', 'nurbs_c', 'clust_c']

    ext_modules = [Extension(f"pyformex.lib.{m}",
                             [f"pyformex/lib/{m}.c"],
                             include_dirs=[np.get_include()],
                             )
                   for m in LIB_MODULES
                   ]

    kargs = {}
    if options['accel']:
        kargs['ext_modules'] = ext_modules

    #print(kargs)

    with open('Description') as file:
        long_description = file.read()

    # PKG_DATA, relative from pyformex path
    PKG_DATA = [
        'pyformexrc',
        'icons/README',
        'icons/*.xpm',
        'icons/*.gif',
        'icons/pyformex*.png',
        'icons/64x64/*',
        'fonts/*',
        'glsl/*',
        'examples/apps.cat',
        'bin/*',
        'data/*',
        'doc/*',
        'sphinx/**',
        'extra/Makefile',
        'extra/*/*',
        'scripts/*',
        ]

    setup(
        cmdclass={'install_lib': install_lib},
        #use_scm_version=True,
        #setup_requires=['setuptools_scm'],
        name='pyformex',
        version=__RELEASE__,
        description='Python framework to create, transform, manipulate and render 3D geometry',
        long_description=long_description,
        author='Benedict Verhegghe',
        author_email='bverheg@gmail.com',
        url='http://pyformex.org',
        download_url='http://download.savannah.gnu.org/releases/pyformex/pyformex-%s.tar.gz' % __RELEASE__,
        license='GNU General Public License (GPL)',
        packages=[
            'pyformex',
            'pyformex.gui',
            'pyformex.gui.menus',
            'pyformex.lib',
            'pyformex.opengl',
            'pyformex.plugins',
            'pyformex.appsdir',
            #  'pyformex.scripts',  # this is not a package!
            'pyformex.examples',
            'pyformex.fe',
            'pyformex.freetype',
            'pyformex.freetype.ft_enums',
        ],
        include_package_data=True,
        #package_data={ 'pyformex': PKG_DATA },
        # scripts=['pyformex/pyformex'],
        # entry_points = {
        #     'console_scripts': [
        #         f'pyformex-{__RELEASE__}=pyformex.main:run'
        #     ],
        # },
        #data_files=manifest.OTHER_DATA,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: X11 Applications :: Qt',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Education',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: C',
            'Topic :: Multimedia :: Graphics :: 3D Modeling',
            'Topic :: Multimedia :: Graphics :: 3D Rendering',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Topic :: Scientific/Engineering :: Visualization',
            'Topic :: Scientific/Engineering :: Physics',
        ],
        #          requires=['numpy','OpenGL','PyQt4 | PySide'],
        **kargs
    )


# Detect some --no-??? options
options = {
    'accel': True,
    'sphinx': True,
    }
for opt in options:
    try:
        i = sys.argv.index(f'--no-{opt}')
        del(sys.argv[i])
        options[opt] = False
    except ValueError:
        pass

msgs = []

if options['sphinx']:
    try:
        import sphinx
    except ImportError:
        msgs.append("""\
Sphinx is missing, so I can't compile the local html documentation.
You should install the package python3-sphinx.
Or you can setup pyFormex without local docs, using the command:
    python setup.py build --no-sphinx""")

if msgs:
    print_msgs(msgs)
    sys.exit()

try:
    run_setup(options)
except Exception as e:
    msgs.append(e)
    if options['accel']:
        msgs.append("""\
If the installation failed because the acceleration libraries could
not be compiled, you may try installing without them:
    python setup.py build --no-accel""")

if msgs:
    print_msgs(msgs)

# End

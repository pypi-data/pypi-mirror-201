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

"""RectangularMesh

This example illustrates the use of the mesh.rectangle function
and the use of seeds in generating Meshes.

"""
_status = 'checked'
_level = 'beginner'
_topics = ['geometry', 'mesh']
_techniques = ['rectangular', 'seed', 'layout']

from pyformex.gui.draw import *
from pyformex.mesh import rectangle
from pyformex.gui.menus.Viewport import clearAll


def run():
    """Main function.

    This is executed on each run.
    """
    clearAll()
    smoothwire()
    fgcolor(red)
    layout(6, 3)

    # Viewports are not correctly initialized!
    # we need to reset canvas settings
    viewport(0)
    smoothwire()
    fgcolor(red)
    M = rectangle(1., 1., 6, 3)
    draw(M)

    viewport(1)
    M = rectangle(1., 1., (6, 0.3), (6, 0.3))
    draw(M)

    viewport(2)
    smoothwire()
    fgcolor(red)
    M = rectangle(1., 1., (6, 0.3), (6, -0.5))
    draw(M)

    viewport(3)
    smoothwire()
    fgcolor(red)
    M = rectangle(1., 1., (6, 0.5, 0.5), (6, 1, 1))
    draw(M)

    viewport(4)
    smoothwire()
    fgcolor(red)
    M = rectangle(1., 1., (6, -1, -1), (6, -1, -1))
    draw(M)

    viewport(5)
    smoothwire()
    fgcolor(red)
    M = rectangle(2., 1., (6, -1, -1), (6, -1, -1))
    draw(M)


if __name__ == '__draw__':
    run()
# End

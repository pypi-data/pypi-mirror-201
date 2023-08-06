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
"""MeshMatch

This example illustrates the Mesh.match method.
It first constructs two Meshes: one with squares (red) and one with
triangles (green). Then it finds the nodes from the second that coincide
with nodes from the first. The matching nodes are marked with black
squares. The matching node numbers from the two meshes are printed out.

Then, after a pause, the parts of both meshes that are connected to the
common nodes are drawn.
"""


_status = 'checked'
_level = 'normal'
_topics = ['mesh']
_techniques = ['draw', 'replicate', 'match', 'cselect']

from pyformex.gui.draw import *

def run():
    transparent()
    smoothwire()
    clear()
    from pyformex.mesh import Mesh

    n=5
    nx=4*n
    ny=2*n

    # construct a Quad4 Mesh
    M = Formex('4:0123').replic2(nx, ny).cselect(np.arange(4*nx, int(7.5*nx))).toMesh().setProp(1)
    draw(M)
    drawNumbers(M.coords, color=red)

    # construct a Tri3 Mesh
    M1 = Formex('3:012').replic2(int(0.6*nx), int(0.45*ny), bias=1, taper=-2).toMesh().scale(2).trl(1, 1.).setProp(2)
    draw(M1)
    zoomAll()
    drawNumbers(M1.coords, color=yellow, trl=[0., -0.25, 0.])

    # find matching nodes
    match = M.matchCoords(M1)

    # get the matching node numbers
    n1 = np.where(match>=0)[0]     # node numbers in Mesh M1
    n0 = match[n1]              # node numbers in Mesh M

    print("List of the %s matching nodes" % len(n1))
    print(np.column_stack([n0, n1]))

    draw(M.coords[n0], marksize=10, bbox='last', ontop=True)

    # compute and draw parts connected to the common nodes
    sleep(4)
    clear()
    draw(M.coords[n0], marksize=10, bbox='last', ontop=True)
    M = M.select(M.connectedTo(n0))
    M1 = M.select(M1.connectedTo(n1))
    draw([M, M1])

if __name__ == '__draw__':
    run()
# End

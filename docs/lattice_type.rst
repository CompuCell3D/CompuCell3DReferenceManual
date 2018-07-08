Lattice Type
~~~~~~~~~~~~

Early versions of CompuCell3D allowed users to use only square lattice.
Most recent versions allow the simulation to be run on
hexagonal lattice as well.

.. note::

Full description of hexagonal lattice including detailed
derivations can be found in “Introduction to Hexagonal Lattices”
available from `http://www.compucell3d.org/BinDoc/cc3d_binaries/Manuals/HexagonalLattice.pdf <http://www.compucell3d.org/BinDoc/cc3d_binaries/Manuals/HexagonalLattice.pdf>`__

To enable hexagonal lattice you need to put
.. code-block:: xml

    <LatticeType>Hexagonal</LatticeType>

in the Potts section of the CC3DML configuration file.

There are few things to be aware of when using hexagonal lattice.
In 2D your pixels are hexagons but in 3D the voxels are rhombic dodecahedrons.
It is particularly important to realize that surface or perimeter of the pixel
(depending whether in 2D or 3D) is different than in the case of square
pixel. The way CompuCell3D hex lattice implementation was done was that
the volume of the pixel was constrained to be ``1`` regardless of the
lattice type.
There is also one to one correspondence between pixels of the square
lattice and pixels of the hex lattice. Consequently, we can come up with
transformation equations which give positions of hex pixels as a
function of square lattice pixel position:

.. math::
   :nowrap:

   \begin{cases}
    & \left [ x_{hex}, y_{hex}, z_{hex}  \right ] = \left [ \left ( x_{cart}+\frac{1}{2} \right ) L, \frac{\sqrt[]{3}}{2}y_{cart}L,\frac{\sqrt[]{6}}{3}z_{cart}L \right ] \text{for } y \mod 2=0 \text{ and } z \mod 3 = 0 \\
    & \left [ x_{hex}, y_{hex}, z_{hex}  \right ] = \left [ x_{cart} L, \frac{\sqrt[]{3}}{2}y_{cart}L,\frac{\sqrt[]{6}}{3}z_{cart}L \right ] \text{for } y \mod 2=1 \text{ and } z \mod 3 = 0 \\
    & \left [ x_{hex}, y_{hex}, z_{hex}  \right ] = \left [ x_{cart} L, \left ( \frac{\sqrt[]{3}}{2}y_{cart} +\frac{\sqrt[]{3}}{6} \right)L,\frac{\sqrt[]{6}}{3}z_{cart}L \right ] \text{for } y \mod 2=0 \text{ and } z \mod 3 = 1 \\
    & \left [ x_{hex}, y_{hex}, z_{hex}  \right ] = \left [ \left ( x_{cart}+\frac{1}{2} \right ) L, \left ( \frac{\sqrt[]{3}}{2}y_{cart} +\frac{\sqrt[]{3}}{6} \right)L,\frac{\sqrt[]{6}}{3}z_{cart}L \right ] \text{for } y \mod 2=1 \text{ and } z \mod 3 = 1 \\
   \end{cases}

Based on the above facts one can work out how unit length and unit
surface transform to the hex lattice. The conversion factors are given
below:

For the 2D case, assuming that each pixel has unit volume, we get:

where denotes length of the hexagon and denotes a distance between
centers of the hexagons. Notice that unit surface in 2D is simply a
length of the hexagon side and surface area of the hexagon with side 'a'
is:

In 3D we can derive the corresponding unit quantities starting with the
formulae for Volume and surface of rhombic dodecahedron (12 hedra)

where 'a' denotes length of dodecahedron edge.

Constraining the volume to be one we get

and thus unit surface is given by:

and unit length by:

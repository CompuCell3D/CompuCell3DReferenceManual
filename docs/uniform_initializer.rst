UniformInitializer Steppable
----------------------------

UniformInitializer Steppable
----------------------------

Th ``UniformInitializer`` steppable lays out cells on the lattice. It allows users to specify
rectangular regions of field with square (or cube in 3D) cells of user
defined types (or random types). Cells can be touching each other or can
be separated by a gap.

The syntax of the plugin is as follows:

.. code-block:: xml

    <Steppable Type="UniformInitializer">
       <Region>
         <BoxMin x="35" y="0" z="30"/>
           <BoxMax x="135" y="1" z="430"/>
           <Gap>0</Gap>
           <Width>5</Width>
          <Types>psm</Types>
       </Region>
    </Steppable>


Above we have defined a 2D rectangular box filled with ``5x5`` cells
touching each other (``Gap = 0``) and having type ``psm``. Notice that if you want
to initialize 2D box in xz plane as above then ``y_min`` and ``y_max`` have to
be ``0`` and ``1`` respectively.

Users can include as many regions as they want. The regions can overlap
each other and, as expected, region defined later in the code overshadows
the one defined earlier. As a result cells from "earlier" regions may
get overwritten by cells from regions defined later in the code. Cells
that are overwritten will either disappear or be truncated.

Additionally users can initialize region with random cell types chosen
from provided list of cell types:

.. code-block:: xml

    <Steppable Type="UniformInitializer">
        <Region>
            <BoxMin x="35" y="0" z="30"/>
            <BoxMax x="135" y="1" z="430"/>
            <Gap>0</Gap>
            <Width>5</Width>
            <Types>psm,ncad,ncam</Types>
        </Region>
    </Steppable>


When user specifies more than one cell type between ``<Types>`` tags then
cells for this region will be initialized with types chosen randomly
from the provided list (here the choices would be ``psm``, ``ncad``, ``ncam``).

.. note::

    The types have to be separated with ``','`` and there should be
    **no spaces**.

.. tip::

    If one of the type names is repeated inside ``<Types>`` element
    this type will get greater weighting means probability of assigning this
    type to a cell will be greater. For example:
    ``<Types>psm,ncad,ncam,ncam,ncam</Types>`` ncam will assigned to a cell with
    probability ``3/5`` and ``psm`` and ``ncad`` with probability ``1/5``.

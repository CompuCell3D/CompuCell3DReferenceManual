Building Simulation of Elongated Cells. Case Study in using Compartments, FPP Links, Curvature energy terms.
------------------------------------------------------------------------------------------------------------

The goal of this tutorial is to build a simulation of multiple elongated cells where each sell is composed of compartments.
We want the cells to stay elongated throughout the course of the simulation. In this tutorial we want to show you how
starting from a simulation involving a single cell you can scale up and build more sophisticated models


Understanding Contact Energies - how to get non-pixelated cell shape
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that we know about compartments and how they are handled by CC3D, let's see how we can  translate our knowledge
into building a simple simulation that involves contact energies. In particular, we want to show you a common pitfall
that you may encounter in your work and how to diagnose it.

In fact this tutorial is an intro to a more sophisticated simulation where we will leverage Focal Point Plasticity Plugin
and Curvature plugin.

.. note::

    Our intention is to teach you how you can start building complex simulation from grounds up
    by starting with a single ce,, understand the behavior of the single cell under different set of parameters
    and gradually adding complexity to your simulation. We strongly believe that in order to build robust and complex
    simulations you firs must master simple cases and build confidence needed to bring your modeling skills
    to the "next level". It is very much like playing the piano, in general it is advised to learn how to play
    "Chopsticks" https://www.youtube.com/watch?v=JM5fjgiFrxg before attempting to play the "Flight of the Bumblebee" https://www.youtube.com/watch?v=M93qXQWaBdE

Let's start. Our first simulation will involve single cell of type "Top" and two plugins - Volume and Contact.
The goal is to make the cell look non-pixelized and do not disappear.

The code for this simulation can be found in ``Demos/CompuCellPythonTutorial/ElongatedCellsTutorial/Tutorial_01``

Here is the XML

.. code-block:: xml

    <CompuCell3D>
        <Potts>
            <Dimensions x="100" y="100" z="1"/>
            <Steps>10000</Steps>
            <Temperature>10</Temperature>
            <Flip2DimRatio>1</Flip2DimRatio>
            <NeighborOrder>2</NeighborOrder>
        </Potts>


        <Plugin Name="Volume">
            <TargetVolume>25</TargetVolume>
            <LambdaVolume>2.0</LambdaVolume>
        </Plugin>


        <Plugin Name="CellType">
            <CellType TypeName="Medium" TypeId="0"/>
            <CellType TypeName="Top" TypeId="1"/>
        </Plugin>


        <Plugin Name="Contact">
            <Energy Type1="Medium" Type2="Medium">0</Energy>
            <Energy Type1="Top" Type2="Top">0</Energy>
            <Energy Type1="Top" Type2="Medium">0</Energy>
            <NeighborOrder>4</NeighborOrder>
        </Plugin>


    </CompuCell3D>

Note that while we are using Contact Energy all the coefficients there are set to 0. As you can expect

Main Python script is simple

.. code-block:: python

    from cc3d import CompuCellSetup

    from ElongatedCellsSteppables import ElongatedCellsSteppable

    CompuCellSetup.register_steppable(steppable=ElongatedCellsSteppable(frequency=1))

    CompuCellSetup.run()


and Python file with steppables is also not too complex:

.. code-block:: Python

    from cc3d.core.PySteppables import *


    class ElongatedCellsSteppable(SteppableBasePy):
        def __init__(self, frequency=1):

            SteppableBasePy.__init__(self, frequency)

        def start(self):
            """
            any code in the start function runs before MCS=0
            """
            top = self.new_cell(cell_type=1)
            self.cell_field[45:50, 25:30, 0] = top

In the steppable class ``ElongatedCellsSteppable`` we create a cell of type 1 (this is cell of type ``Top`` - see XML above).

The XML is also very simple. We defined 3 cell types there and set ``TargetVolume`` and ``LambdaVolume`` to ``25`` and 2.0
All contact energy coefficients are 0 - effectively stating that contact energy included in the actual simulation is always 0.

If we run this simulation we will get the following:

|img001|

A partially pixelated cell is not particularly interesting but we should expect this. We created a square cell -  see Steppable code above
and after few MCS it disintegrated into few pieces. Because we have only volume energy there is nothing to prevent cell pixelization
and any cell shape as long as the total number of pixel in the single cell is roughly 25 is perfectly fine.

Let's try using contact energy to see if we can make the cell non-pixelized - ``Demos/CompuCellPythonTutorial/ElongatedCellsTutorial/Tutorial_01``
The rationale is as follows: Volume energy will asure the number of pixel in the cell is roughly 25 and the
contact energy's task will be to keep cell from pixelizing by
penalizing cell-Medium interface. As you recall CC3D minimizes energy so if we use positive contact coefficient
between cell and the Medium the simulation the pixelized cell will have quite a high energy - because many single
pixels are surrounded by Medium and each such pixel will bring up total energy by multiples of contact energy coefficient.

The actual number of interfaces between single pixel and Medium is control by ``<NeighborOrder>`` input in Contact PLugin.
In our case we are including interfaces up to 4th nearest neighbor - ``<NeighborOrder>4</NeighborOrder>`` .

Let's look at the new specification of Contact energy:

.. code-block:: XML

    <Plugin Name="Contact">
        <Energy Type1="Medium" Type2="Medium">0</Energy>
        <Energy Type1="Top" Type2="Top">0</Energy>
        <Energy Type1="Top" Type2="Medium">15</Energy>
        <NeighborOrder>4</NeighborOrder>
    </Plugin>

By changing contact energy coefficient between ``Top`` cells and ``Medium`` to a positive number CC3D will work to
minimize Top-Medium interfaces while maintaining total number of pixels of the cell (due to Volume energy term).

It turns out that the cell disappears. Why? This is because Volume energy term was not "strong enough" to
overcome minimization of energy coming from Contact energy. Simply put when we get to one-pixel cell and we
try to overwrite this pixel by Medium the Volume energy plugin will contribute positive term to change of energy and Contact energy
will contribute negative term (because loosing cell medium interfaces leads to a negative change energy).

Let's try fixing it by "strengthening" Volume energy term


.. code-block:: XML

    <Plugin Name="Volume">
        <TargetVolume>25</TargetVolume>
        <LambdaVolume>4.0</LambdaVolume>
    </Plugin>


|img002|


This time we get the desired result.

Let's add few more cells (including of type ``Center``).


.. |img001| image:: images/elongated_cells_tutorial/img001.png
    :scale: 50%

.. |img002| image:: images/elongated_cells_tutorial/img002.png
    :scale: 50%
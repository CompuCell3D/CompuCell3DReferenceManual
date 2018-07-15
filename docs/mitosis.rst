Mitosis Steppable.
-----------------

Mitosis steppable is described in great detail in "Python Scripting Manual" - see for example
 https://pythonscriptingmanual.readthedocs.io/en/latest/mitosis.html?highlight=mitosis
but because of its importance we are including a copy of that description
here.

In developmental simulations we often need to simulate cells which grow
and divide. In earlier versions of CompuCell3D we had to write quite
complicated plugin to do that which was quite cumbersome and
unintuitive. The only advantage of the plugin was that mitosis was
taking place immediately after the pixel copy which had triggered
mitosis condition. This guaranteed that any cell which was supposed
divide at any instance in the simulation, actually did. However, because
state of the simulation is normally observed after completion of full a
Monte Carlo Step, and not in the middle of MCS it makes actually more
sense to implement ``Mitosis`` as a steppable. Let us examine the simplest
simulation which involves mitosis. We start with a single cell and grow
it. When cell reaches critical (doubling) volume it divides. We check if
the cell has reached doubling volume at the end of each MCS. The folder
containing this simulation is


*Demos/CompuCellPythonTutorial/steppableBasedMitosis*. The mitosis algorithm
is implemented in
*Demos/CompuCellPythonTutorial/steppableBasedMitosis/Simulation/steppableBasedMitosisSteppables.py*

File:

*Demos/CompuCellPythonTutorial/steppableBasedMitosis/Simulation/steppableBasedMitosisSteppables.py*

.. code-block:: python

    from PySteppables import *
    from PySteppablesExamples import MitosisSteppableBase
    import CompuCell

    class VolumeParamSteppable(SteppableBasePy):
        def __init__(self, _simulator, _frequency=1):
            SteppableBasePy.__init__(self, _simulator, _frequency)

        def start(self):
            for cell in self.cellList:
                cell.targetVolume = 25
                cell.lambdaVolume = 2.0

        def step(self, mcs):
            for cell in self.cellList:
                cell.targetVolume += 1

    class MitosisSteppable(MitosisSteppableBase):
        def __init__(self, _simulator, _frequency=1):
            MitosisSteppableBase.__init__(self, _simulator, _frequency)

            # 0 - parent child position will be randomized between mitosis event
            # negative integer - parent appears on the 'left' of the child
            # positive integer - parent appears on the 'right' of the child
            self.setParentChildPositionFlag(-1)

        def step(self, mcs):
            cells_to_divide = []
            for cell in self.cellList:
                if cell.volume > 50:
                    cells_to_divide.append(cell)

            for cell in cells_to_divide:
                # to change mitosis mode leave one of the below lines uncommented
                self.divideCellRandomOrientation(cell)

        def updateAttributes(self):
            self.parentCell.targetVolume /= 2.0  # reducing parent target volume
            self.cloneParent2Child()

            if self.parentCell.type == self.CONDENSING:
                self.childCell.type = self.NONCONDENSING
            else:
                self.childCell.type = self.CONDENSING

Two steppables:`` VolumeParamSteppable`` and ``MitosisSteppable`` are the
essence of the above simulation. The first steppable initializes volume
constraint for all the cells present at ``T=0`` MCS (only one cell) and then
every ``10`` MCS (see the frequency with which ``VolumeParamSteppable`` in
initialized to run -
*Demos/CompuCellPythonTutorial/steppableBasedMitosis/Simulation/steppableBasedMitosis.py*)
it increases target volume of cells, effectively causing cells to grow.

.. code-block:: python

    from steppableBasedMitosisSteppables import VolumeParamSteppable
    volumeParamSteppable=VolumeParamSteppable(sim ,10)
    steppableRegistry.registerSteppable(volumeParamSteppable)

    from steppableBasedMitosisSteppables import MitosisSteppable
    mitosisSteppable=MitosisSteppable(sim, 10)
    steppableRegistry.registerSteppable(mitosisSteppable)


The second steppable checks every ``10`` MCS (we can, of course, run it
every MCS) if cell has reached doubling volume of ``50``. If it did such
cell is added to the list cells\_to\_divide. After construction of
``cells_to_divide`` is complete we iterate over this list and divide all
the cells in it.

.. warning::

    It is important to divide cells outside the loop where we
    iterate over entire cell inventory. If we keep dividing cells in this
    loop we are adding elements to the list over which we iterate over and
    this might have unwanted side effects. The solution is to use use list
    of cells to divide as we did in the example.

Notice that we call ``self.divideCellRandomOrientation(cell``) function to
divide cells. Other modes of division are available as well and they are
as follows:

.. code-block:: python

    self.divideCellOrientationVectorBased(cell,1,0,0)
    self.divideCellAlongMajorAxis(cell)
    self.divideCellAlongMinorAxis(cell)

Notice that ``MitosisSteppable`` inherits ``MitosisSteppableBase`` class (defined in
``PySteppablesExamples.py``).It is the base class which ensures that
after we call any of the cell dividing function (e.g.
``divideCellRandomOrientation``) CompuCell3D will automatically call
``updateAttributes`` function as well. ``updateAttributes`` function is very
important and we must call it in order to ensure integrity and sanity of
the simulation. During mitosis a new cell is created (accessed in Python
as childCell – defined in ``MitosisSteppableBase`` -
``self.mitosisSteppable.childCell``) and as such this cell is uninitialized.
It does have default attributes (read-only) of a cell such as volume,
surface (if we decide to use surface constraint or ``SurfaceTracker``
plugin) but all other parameters of such cell are set to default values.
In our simulation we have been setting ``targetVolume`` and ``lambdaVolume``
individually for each cell. After mitosis ``childCell`` will need those
parameters to be set as well. To make things more interesting, in our
simulation we decided to change type of cell to be different than type
of parent cell. In more complex simulations where cells have more
attributes which are used in the simulation, we have to make sure that
in the ``updateAttributes`` function ``childCell`` and its attributes get
properly initialized. It is also very common practice to change
attributes of parentCell after mitosis as well to account for the fact
that parentCell is not the original parentCell from before the mitosis.

.. note::

    If you specify orientation vector for the mitosis the
    actual division will take place along the line/plane **perpendicular to
    this vector**.

.. note::

    The name of the function where we update attributes after
    mitosis has to be exactly ``updateAtttributes``. If it is called differently
    CC3D will not call it automatically. We can of course call such function
    by hand, immediately we do the mitosis but this is not very elegant
    solution.

FocalPointPlasticity Plugin
---------------------------

``FocalPointPlasticity`` puts constrains on the
distance between cells’ center of masses. A key feature of this plugin is that
the list of "focal point plasticity neighbors" can change as the
simulation evolves and user has to specifies the maximum number of "focal point
plasticity neighbors" a given cell can have. Let’s look at relatively
simple CC3DML syntax of ``FocalPointPlasticityPlugin`` (see
*Demos/PluginDemos/FocalPointPlasticity/FocalPointPlasticity* example and we will show more complex
examples later):

.. code-block:: xml

   <Plugin Name="FocalPointPlasticity">
      <Parameters Type1="Condensing" Type2="NonCondensing">
         <Lambda>10.0</Lambda>
         <ActivationEnergy>-50.0</ActivationEnergy>
         <TargetDistance>7</TargetDistance>
         <MaxDistance>20.0</MaxDistance>
         <MaxNumberOfJunctions>2</MaxNumberOfJunctions>
      </Parameters>

      <Parameters Type1="Condensing" Type2="Condensing">
         <Lambda>10.0</Lambda>
         <ActivationEnergy>-50.0</ActivationEnergy>
         <TargetDistance>7</TargetDistance>
         <MaxDistance>20.0</MaxDistance>
         <MaxNumberOfJunctions>2</MaxNumberOfJunctions>
      </Parameters>
      <NeighborOrder>1</NeighborOrder>
   </Plugin>

``Parameters`` section describes properties of links between cells.
``MaxNumberOfJunctions``, ``ActivationEnergy``, ``MaxDistance`` and ``NeighborOrder``
are responsible for establishing connections between cells. CC3D
constantly monitors pixel copies and during pixel copy between two
neighboring cells/subcells it checks if those cells are already
participating in focal point plasticity constraint. If they are not,
CC3D will check if connection can be made (e.g. ``Condensing`` cells can
have up to two connections with ``Condensing`` cells and up to 2 connections
with ``NonCondensing`` cells – see first line of ``Parameters`` section and
``MaxNumberOfJunctions`` tag). The ``NeighborOrder`` parameter determines the
pixel vicinity of the pixel that is about to be overwritten which CC3D
will scan in search of the new link between cells. ``NeighborOrder 1``
(which is default value if you do not specify this parameter) means that
only nearest pixel neighbors will be visited. The ``ActivationEnergy``
parameter is added to overall energy in order to increase the odds of
pixel copy which would lead to new connection.

Once cells are linked the energy calculation is carried out according to the formula:

.. math::
   :nowrap:
   \begin{eqnarray}
      E = \sum_{i,j,cell\ neighbors}\lambda_{ij}\left ( l_{ij}-L_{ij} \right )^2
   \end{eqnarray}

where :math:`l_{ij}` is a distance between center of masses of cells ``i`` and ``j`` and :math:`L_{ij}` is
a target length corresponding to :math:`l_{ij}`.

:math:`\lambda_{ij}` and :math:`L_{ij}` between different cell types are
specified using ``Lambda`` and ``TargetDistanc``e tags. The``MaxDistance``
determines the distance between cells’ center of masses past which the link
between those cells break. When the link breaks, then in order for the
two cells to reconnect they would need to come in contact again.
However it is usually more likely that there will be other
cells in the vicinity of separated cells so it is more likely to
establish new link than restore broken one.

The above example was one of the simplest examples of use of
``FocalPointPlasticity``. A more complicated one involves compartmental
cells. In this case each cell has separate "internal" list of links
between cells belonging to the same cluster and another list between
cells belonging to different clusters. The energy contributions from
both lists are summed up and everything that we have said when
discussing example above applies to compartmental cells. Sample syntax
of the ``FocalPointPlasticity`` plugin which includes compartmental cells is
shown below. We use ``InternalParameters`` tag/section to describe links
between cells of the same cluster (see *Demos/PluginDemos/FocalPointPlasticity/FocalPointPlasticityCompartments*
example):

.. code-block:: xml

   <Plugin Name="FocalPointPlasticity">

       <Parameters Type1="Top" Type2="Top">
          <Lambda>10.0</Lambda>
          <ActivationEnergy>-50.0</ActivationEnergy>
          <TargetDistance>7</TargetDistance>
          <MaxDistance>20.0</MaxDistance>
          <MaxNumberOfJunctions NeighborOrder="1">1</MaxNumberOfJunctions>
       </Parameters>

       <Parameters Type1="Bottom" Type2="Bottom">
          <Lambda>10.0</Lambda>
          <ActivationEnergy>-50.0</ActivationEnergy>
          <TargetDistance>7</TargetDistance>
          <MaxDistance>20.0</MaxDistance>
          <MaxNumberOfJunctions NeighborOrder="1">1</MaxNumberOfJunctions>
       </Parameters>

       <InternalParameters Type1="Top" Type2="Center">
          <Lambda>10.0</Lambda>
          <ActivationEnergy>-50.0</ActivationEnergy>
          <TargetDistance>7</TargetDistance>
          <MaxDistance>20.0</MaxDistance>
          <MaxNumberOfJunctions>1</MaxNumberOfJunctions>
       </InternalParameters>

       <InternalParameters Type1="Bottom" Type2="Center">
          <Lambda>10.0</Lambda>
          <ActivationEnergy>-50.0</ActivationEnergy>
          <TargetDistance>7</TargetDistance>
          <MaxDistance>20.0</MaxDistance>
          <MaxNumberOfJunctions>1</MaxNumberOfJunctions>
       </InternalParameters>

       <NeighborOrder>1</NeighborOrder>

   </Plugin>


We can also specify link constituent law and change it to different form
that "spring relation". To do this we use the following syntax inside
FocalPointPlasticity CC3DML plugin:

.. code-block:: xml

    <LinkConstituentLaw>
        <!--The following variables lare defined by default: Lambda,Length,TargetLength-->

        <Variable Name='LambdaExtra' Value='1.0'/>
        <Formula>LambdaExtra*Lambda*(Length-TargetLength)^2</Formula>

    </LinkConstituentLaw>


By default CC3D defines 3 variables (``Lambda``, ``Length``, ``TargetLength``) which
correspond to ,:math:`\lambda_{ij}` :math:`l_{ij}` and :math:`L_{ij}` from the formula
above. We can also define extra variables in the CC3DML (e.g.
``LambdaExtra``). The actual link constituent law obeys ``muParser`` syntax
convention. Once link constituent law is defined it is applied to all
focal point plasticity links. The example demonstrating the use of
custom link constituent law can be found in
*Demos/PluginDemos/FocalPointPlasticityCustom*.

Sometimes it is necessary to modify link parameters individually for
every cell pair. In this case we would manipulate ``FocalPointPlasticity``
links using Python scripting. Example
*Demos/PluginDemos/FocalPointPlasticity/FocalPointPlasticityCompartments* demonstrates exactly this
situation. You still need to include CC3DML section as the one shown
above for compartmental cells, because we need to tell CC3D how to link
cells. The only notable difference is that in the CC3DML we have to
include ``<Local/>`` tag to signal that we will set link parameters (``Lambda``,
``TargetDistance``, ``MaxDistance``) individually for each cell pair:

.. code-block:: xml

   <Plugin Name="FocalPointPlasticity">
       <Local/>
       <Parameters Type1="Top" Type2="Top">
          <Lambda>10.0</Lambda>
          <ActivationEnergy>-50.0</ActivationEnergy>
          <TargetDistance>7</TargetDistance>
          <MaxDistance>20.0</MaxDistance>
          <MaxNumberOfJunctions NeighborOrder="1">1</MaxNumberOfJunctions>
       </Parameters>
      ...
   </Plugin>



Python steppable where we manipulate cell-cell focal point plasticity
link properties is shown below:

.. code-block:: python

   class FocalPointPlasticityCompartmentsParams(SteppablePy):
       def __init__(self, _simulator, _frequency=10):
           SteppablePy.__init__(self, _frequency)
           self.simulator = _simulator
           self.focalPointPlasticityPlugin = CompuCell.getFocalPointPlasticityPlugin()
           self.inventory = self.simulator.getPotts().getCellInventory()
           self.cellList = CellList(self.inventory)

       def step(self, mcs):
           for cell in self.cellList:
               for fppd in InternalFocalPointPlasticityDataList(self.focalPointPlasticityPlugin, cell):
                   self.focalPointPlasticityPlugin.setInternalFocalPointPlasticityParameters(cell, fppd.neighborAddress,
                                                                                             0.0, 0.0, 0.0)

The syntax to change focal point plasticity parameters (or as here
internal parameters) is as follows:

.. code-block:: python

   setFocalPointPlasticityParameters(cell1, cell2, lambda, targetDistance, maxDistance)

.. code-block:: python

   setInternalFocalPointPlasticityParameters(cell1, cell2, lambda, targetDistance, maxDistance)


Similarly, to inspect current values of the focal point plasticity
parameters we would use the following Python construct:

.. code-block:: python

   for cell in self.cellList:
       for fppd in InternalFocalPointPlasticityDataList(self.focalPointPlasticityPlugin, cell):
           print "fppd.neighborId", fppd.neighborAddress.id
           " lambda=", fppd.lambdaDistance


For non-internal parameters we simply use ``FocalPointPlasticityDataList``
instead of ``InternalFocalPointPlasticityDataList`` .

Examples *Demos/PluginDemos/FocalPointPlasticity…* show in relatively simple way how
to use ``FocalPointPlasticity`` plugin. Those examples also contain useful
comments.

.. note::

   When using ``FocalPointPlasticity`` Plugin from ``Mitosis`` module one might
   need to break or create focal point plasticity links. To do so
   ``FocalPointPlasticity`` Plugin provides 4 convenience functions which can
   be invoked from the Python level:

   .. code-block:: python

      deleteFocalPointPlasticityLink(cell1, cell2)

      deleteInternalFocalPointPlasticityLink(cell1, cell2)

      createFocalPointPlasticityLink(cell1, cell2, lambda , targetDistance, maxDistance)

      createInternalFocalPointPlasticityLink(cell1, cell2, lambda , targetDistance, maxDistance)



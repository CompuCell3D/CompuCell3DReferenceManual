Vector Field Polarization plugin
==================================

**VectorFieldPolarization** is a CompuCell3D plugin that introduces a custom energy term to bias cellular motion based on alignment with a spatially defined vector field. 
This is useful for scenarios where cells follow physical or chemical directional cues, such as fiber alignment in extracellular matrices (i.e. ECM fibers). 

When enabled, the plugin favors cell movement along the local direction specified by the vector field,
thereby increasing the likelihood of copy attempts that align with the vector direction. 
Unlike the Chemotaxis plugin, this plugin uses a vector field that exists independently as opposed to a chemical field that cells may interact with.

Related Demo: ``Demos/PluginDemos/VectorFieldPolarization/vector_field_polarization.cc3d``

------------------------
XML Syntax
------------------------

This will register a vector field named ``Fibers``. 
CompuCell3D can only support one VectorFieldPolarization plugin at a time. 

.. code-block:: xml

    <Plugin Name="VectorFieldPolarization">
        <Field Name="Fibers"/>
        <PolarizationLambda>2.0</PolarizationLambda>
    </Plugin>

------------------------
XML Attributes
------------------------

``<Field Name="..."/>`` (required): 
  Specifies the name of the vector field that encodes directional cues for the cells.
  This field must be initialized in Python using ``self.field.<FieldName>``.  
  Each vector at a lattice point defines the preferred direction of movement at that point.

``<PolarizationLambda>`` (required): 
  A non-negative floating-point value controlling the strength of the polarization effect.
  Higher values increase the influence of the vector field on cell motility. 
  Since we take the absolute value, the sign does not matter. 

------------------------
Python Manipulation
------------------------

We can use the ``start`` function to define where the vectors point. 
In this example, the cells will migrate in the negative x/y direction at specific positions.

.. code-block:: python

    class VectorFieldSteppable(SteppableBasePy):
        def __init__(self, frequency=10):
            SteppableBasePy.__init__(self, frequency)

        def start(self):
            fiber_field_cpp = self.field.Fibers
            fiber_field_cpp[30, 10, 0] = [-30, -10, 0]
            fiber_field_cpp[20, 30, 0] = [-20, -30, 0]

This field can be updated dynamically during the simulation to reflect changing environments.

------------------------
Energy Contribution
------------------------

The plugin changes energy according: 

.. math::

    E = -\left| \lambda \cdot (\vec{v}_{\text{field}} \cdot \vec{d}_{\text{COM (Old cell)}}) \right| - \left| \lambda \cdot (\vec{v}_{\text{field}} \cdot \vec{d}_{\text{COM (New cell)}}) \right|

Where:

- :math:`\lambda` is the polarization coefficient (``PolarizationLambda``).
- :math:`\vec{v}_{\text{field}}` is the vector from the field at the cell’s center of mass.
- :math:`\vec{d}_{\text{COM}}` is the displacement vector resulting from a pixel copy attempt. We evaluate this for both the new cell (if it exists) and old cell (if it exists). 

Since the energy contribution is negative, VectorFieldPolarization generally reduces the energy needed for cells to align in the direction specified by the vector field. 

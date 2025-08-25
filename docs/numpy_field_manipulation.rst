NumPy Field Manipulation
==================================

NumPy-backed fields are a **new feature in CompuCell3D 4.7.0** that allows direct access to scalar or vector field data as NumPy arrays. 
In comparison to traditional field manipulation, using NumPy offers easier array manipulation syntax and efficient computational performance.
The array data is shared memory between your Python code and CompuCell3D's C++ backend. 

The demo **shared_numpy_fields** shows this feature in action. 

Creating Shared NumPy Fields
###############################################

**padding**: adds extra layers around the field. Useful for PDE solvers.

**precision_type**: a NumPy dtype such as ``"int16"`` or ``"float32"``. The following NumPy data types are supported:

- ``int8`` (signed char)
- ``uint8`` (unsigned char)
- ``int16`` (short)
- ``uint16`` (unsigned short
- ``int32`` (int)
- ``uint32`` (unsigned int)
- ``int64`` (long long)
- ``uint64`` (unsigned long long)
- ``float32`` (float)
- ``float64`` (double)

You can create **scalar fields** using:

.. code-block:: python

    self.create_shared_scalar_numpy_field("exampleScalarNumpy", padding=1)

.. code-block:: python
    
    self.create_shared_scalar_numpy_field("exampleInt16FieldPythonNPY", precision_type="int16")

.. code-block:: python
    
    self.create_shared_scalar_numpy_field("exampleFloat32FieldPythonNPY", precision_type="float32")
    
You can create **vector fields** using:

.. code-block:: python
    
    self.create_shared_vector_numpy_field("exampleVectorNumpy")

.. code-block:: python
    
    self.create_shared_vector_numpy_field("exampleVectorNumpy", precision_type="float32")

Accessing Fields
###############################################

Once created, these fields can be accessed directly:

.. code-block:: python

    exampleScalarNumpy = self.field.exampleScalarNumpy
    exampleScalarNumpy[15, 25, 0] = 5  # Assign scalar

.. code-block:: python

    exampleVectorNumpy = self.field.exampleVectorNumpy
    exampleVectorNumpy[15, 25, 0] = [15, 25, 0]  # Assign vector

Or, to access the field and its padding, use ``raw_field``:

.. code-block:: python

    cpp_array = self.raw_field.exampleScalar  # Includes padding

    cpp_array_user = self.field.exampleScalar  # Excludes padding

**********************************************

Using Field Manager XML Helper
###############################################

NumPy fields can be created in XML too. This is just a different way of writing the syntax. 

**Name**: the unique name that will be used to identify the field in XML and Python.

**Type**: ``"scalar"`` (AKA ``"concentration"``) or ``"vector"``.

**Precision**: a NumPy dtype such as ``"int16"`` or ``"float32"``.

**Example**:

.. code-block:: XML

    <Steppable Type="FieldManager">
        <Field Name="fibers_field_manager" Type="vector"/>
        <Field Name="numpy_field_manager" Type="scalar"/>
        <Field Name="cell_type_field" Type="scalar" Precision="uint8"/>
        <Field Name="cell_volume_field" Type="scalar" Precision="int16"/>
    </Steppable>

They can then be accessed from Python as before:

.. code-block:: python

    fibers_fm = self.field.fibers_field_manager
    fibers_fm[15, 25, 0, ...] = [120, 120, 0]

**********************************************

Key Differences from Standard Field API
---------------------------------------

.. raw:: html

    <table>
    <thead>
        <tr>
            <th>Feature</th>
            <th>NumPy Field API</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Access Syntax</td>
            <td>NumPy-style slicing: <code>field[x1:x2, y1:y2, z1]</code></td>
        </tr>
        <tr>
            <td>Performance</td>
            <td>Significantly faster for bulk operations using NumPy</td>
        </tr>
        <tr>
            <td>Data Types</td>
            <td>Must specify <code>dtype</code> (e.g., <code>int16</code>, <code>float32</code>)</td>
        </tr>
        <tr>
            <td>Padding</td>
            <td>Use <code>raw_field</code> to access padded data regions</td>
        </tr>
        <tr>
            <td>In-place Editing</td>
            <td>Allows slicing and assignment directly</td>
        </tr>
    </tbody>
    </table>

**********************************************

Example Use Case: Copying Data from Standard Fields
----------------------------------------------------

The demo **shared_numpy_fields_steppables.py** shows that it's possible to edit standard field data into NumPy-backed fields using helper methods:

.. code-block:: python

    self.copy_cell_attribute_field_values_to("cell_type_field", "type")
    self.copy_cell_attribute_field_values_to("cell_volume_field", "id")

These populate the NumPy fields with values derived from cell attributes. However, if your workflow requires you to transfer data from NumPy arrays to cells, you should write code to do this after `copy_cell_attribute_field_values_to`. 

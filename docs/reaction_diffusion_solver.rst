ReactionDiffusionSolverFE Plugin
-----------------------------------

Related: `ReactionDiffusionSolverFVM (finite volume) Plugin <reaction_diffusion_solver_fvm.html>`_

ReactionDiffusionSolverFE is the predecessor of ReactionDiffusionSolverFVM. 
Its usage is relatively simpler, and it is primarily defined in XML. 
Unlike the ReactionDiffusionSolverFVM, this PDE solver supports the use of an :ref:`AdditionalTerm <AdditionalTerm>` expression that defines the reaction diffusion equation. 

For example usage, see our demos on FitzHugh-Nagumo, Schnakenberg, Gierer-Meinhardt, Gray-Scott, Oscillatory, and Thomas models.  

XML Properties
****************************

* **Element** ``<ConcentrationFileName>`` (optional)
    * Contains the relative path to a text file that contains values of concentration for every pixel.
    * We recommend using either InitialConcentrationExpression or ConcentrationFileName but not both.
    * See :ref:`Diffusion Solver Settings <ConcentrationFileName>` for more details
* **Element** ``<DeltaX>`` (optional)
    * Specifies discretization along the *x* dimension.
    * If only ``<DeltaX>`` is specified, then a uniform discretization is applied along all directions.
* **Element** ``<DeltaY>`` (optional)
    * Specifies discretization along the *y* dimension.
* **Element** ``<DeltaZ>`` (optional)
    * Specifies discretization along the *z* dimension.
* **Element** ``<DeltaT>`` (optional)
    * Allows calling of diffusion (and only diffusion) more than once per MCS
    * It is intended to be used with ``<ExtraTimesPerMCS>``
    * See :ref:`DeltaT <DeltaT>` and `Diffusion Solver Settings <diffusion_solver_settings.html>`_ for more details
* **Element** ``<DiffusionField>``
    * Defines a diffusion field
    * **Attribute** ``Name``: the name of the field
    * **Element** ``<DiffusionData>``
        * **Element** ``<AdditionalTerm>`` (optional)
            * Contains a `muParser expression <mu_parser.html>`_ that determines the reaction diffusion equation. See :ref:`here <AdditionalTerm>` for more details
            * The expression can be unique for each CellType with the use of ternary operators. 
        * **Element** ``<DecayCoefficient>`` (optional)
            * Specifies a constant decay coefficient for a cell type.
            * Can be set per cell during simulation execution
            * **Attribute** ``CellType``: name of the cell type
        * **Element** ``<DecayConstant>`` (optional)
            * Specifies a constant diffusion coefficient for the medium.
            * Note that ``<GlobalDecayConstant>`` performs the same function, despite its name.
        * **Element** ``<DiffusionCoefficient>`` (optional)
            * Specifies a constant diffusion coefficient for a cell type.
            * Can be set per cell during simulation execution
            * **Attribute** ``CellType``: name of the cell type
        * **Element** ``<DiffusionConstant>`` (optional)
            * Specifies a constant diffusion coefficient for the medium.
            * Note that ``<GlobalDiffusionConstant>`` performs the same function, despite its name.
    * **Element** ``<SecretionData>`` (optional)
        * Secretion data elements, defined in the same way as for :ref:`FlexibleDiffusionSolverFE <SecretionData>`
    * **Element** ``<BoundaryConditions>`` (optional)
        * Boundary condition elements, defined in the same as for DiffusionSolverFE.
        * Boundary conditions are applied at surfaces and can be manipulated at each site during simulation execution.
        * If a condition is not specified for a boundary, then it is assumed to be zero flux.
        * `BoundaryConditions <boundary_conditions_diffusion.html>`_ options:
            * NoFlux (default)
            * ConstantValue
            * ConstantDerivative
            * Periodic
* **Element** ``<ExtraTimesPerMCS>`` (optional)
    * Allows calling of diffusion (and only diffusion) more than once per MCS
    * It is intended to be used with ``<DeltaT>`` and ``<DeltaX>``
    * See :ref:`DeltaT <DeltaT>` and `Diffusion Solver Settings <diffusion_solver_settings.html>`_ for more details
* **Element** ``<FluctuationCompensator>`` (optional)
    * Enables deployment of the CC3D FluctuationCompensator.
* **Element** ``<InitialConcentrationExpression>`` (optional)
    * Contains a `muParser expression <mu_parser.html>`_ to define the level of concentration at each voxel on MCS 0.
    * You can use either InitialConcentrationExpression or ConcentrationFileName but not both. However, the preferred way to handle initial conditions is to use the ``start`` function of the Python Steppable and initialize fields there. 


Example Usage
****************************

The following is a representative example of a specification for the RD Solver using two fields, *F* and *H*.
``DeltaX/Y/Z``, ``DeltaT``, and ``ExtraTimesPerMCS`` apply to all RD equations. Notice, secretion is called only once per MCS regardless of how many times you call diffuse step.

.. code-block:: xml

    <Steppable Type="ReactionDiffusionSolverFE">
        <!-- <DeltaT>0.1</DeltaT>
        <DeltaX>1.0</DeltaX>
        <ExtraTimesPerMCS>9</ExtraTimesPerMCS> -->
        <DiffusionField>
            <DiffusionData>
                <FieldName>F</FieldName>
                <DecayConstant>0.005</DecayConstant>
                <DiffusionConstant>0.010</DiffusionConstant>
                <ConcentrationFileName>Simulation/diffusion_2D.pulse.txt</ConcentrationFileName>
                <AdditionalTerm>-0.01*H</AdditionalTerm>
            </DiffusionData>
            <BoundaryConditions>
                <Plane Axis="X">
                    <Periodic/>
                </Plane>
                <Plane Axis="Y">
                    <Periodic/>
                </Plane>
            </BoundaryConditions>
        </DiffusionField>
        <!-- Add more DiffusionFields here as desired -->
    </Steppable>

You can also define diffusion and decay coefficients on a per-cell basis. 

.. code-block:: xml

    <DiffusionData>
        <FieldName>VEGF</FieldName>
        <DiffusionConstant>0.25</GlobalDiffusionConstant>
        <DecayConstant>0</GlobalDecayConstant>
        <DiffusionCoefficient CellType="StalkCell">0.1</DiffusionCoefficient>
        <DiffusionCoefficient CellType="TipCell">0.1</DiffusionCoefficient>
        <DecayCoefficient CellType="StalkCell">0</DecayCoefficient>
        <DecayCoefficient CellType="TipCell">0</DecayCoefficient>
        <InitialConcentrationExpression>0*x/100</InitialConcentrationExpression>
        <!-- As an alternative to InitialConcentrationExpression, you can use ConcentrationFileName. -->
        <!-- <ConcentrationFileName>INITIAL CONCENTRATION FIELD - typically a file with path Simulation/NAME_OF_THE_FILE.txt</ConcentrationFileName> -->
    </DiffusionData>

ReactionDiffusionSolverFE supports the use of `InitialConcentrationExpression` or `ConcentrationFileName` to define the level of chemical present at MCS 0. 

.. code-block:: xml

    <DiffusionData>
        . . .
        <InitialConcentrationExpression>0*x/100</InitialConcentrationExpression>
        <!-- OR -->
        <ConcentrationFileName>Simulation/NAME_OF_THE_FILE.txt</ConcentrationFileName> -->
    </DiffusionData>

How It Works
***************************

The reaction diffusion solver solves the following system of N reaction
diffusion equations:

.. math::
    :nowrap:

    \begin{align*}
     \frac{\partial c_1}{\partial t} = D \nabla^2c_1-kc_1+\text{secretion} + f_1(c_1,c_2,...,c_N, W) \\
     \frac{\partial c_2}{\partial t} = D \nabla^2c_2-kc_2+\text{secretion} + f_2(c_1,c_2,...,c_N,W) \\
     {\text ...} \\
     \frac{\partial c_N}{\partial t} = D \nabla^2c_N-kC_N+\text{secretion} + f_N(c_1,c_2,...,c_N, W)
    \end{align*}

where ``W`` denotes cell type

Let's consider a simple example of such system:

.. math::
    :nowrap:

    \begin{align*}
     \frac{\partial F}{\partial t} = 0.1 \nabla^2F - 0.1H \\
     \frac{\partial H}{\partial t} = 0.0 \nabla^2H + 0.1F
    \end{align*}


It can be coded as follows:

.. code-block:: xml

    <Steppable Type="ReactionDiffusionSolverFE">
      <AutoscaleDiffusion/>
      <DiffusionField Name="F">
        <DiffusionData>
          <FieldName>F</FieldName>
          <DiffusionConstant>0.010</DiffusionConstant>
          <ConcentrationFileName>
          Demos/diffusion/diffusion_2D.pulse.txt
          </ConcentrationFileName>
          <AdditionalTerm>-0.01*H</AdditionalTerm>
        </DiffusionData>
      </DiffusionField>

      <DiffusionField Name="H">
        <DiffusionData>
          <FieldName>H</FieldName>
          <DiffusionConstant>0.0</DiffusionConstant>
          <AdditionalTerm>0.01*F</AdditionalTerm>
        </DiffusionData>
      </DiffusionField>
    </Steppable>

.. _AdditionalTerm:

Notice how we implement functions ``f`` from the general system of
reaction diffusion equations. We simply use ``<AdditionalTerm>`` tag and
there we type an arithmetic expression involving field names (tags
``<FieldName>``). In addition to this, we may include in those expressions the 
word ``CellType``. For example:

.. code-block:: xml

    <AdditionalTerm>0.01*F*CellType</AdditionalTerm>

This means that function ``f`` will depend also on ``CellType`` . ``CellType``
holds the value of the type of the cell at a particular location - ``x``, ``y``, ``z``
- of the lattice. The inclusion of the cell type might be useful if you
want to use additional terms which may change depending on the cell
type. Then all you have to do is to either use if statements inside
``<AdditionalTerm>`` or form equivalent mathematical expression using
functions allowed by ``muParser``: http://muparser.sourceforge.net/mup_features.html#idDef2

For example, let's assume that the additional term for the second equation is
the following:

.. math::
    :nowrap:

        f_F  =
         \begin{cases}
               0.1F  && \text{if CellType=1}\\
                0.51F  && \text{otherwise}
            \end{cases}


In such a case, additional terms would be coded as follows:

.. code-block:: xml

    <AdditionalTerm>CellType==1 ? 0.01*F : 0.15*F</AdditionalTerm>

We used a ternary operator, which functions the same as an `` if-then-else`` statement, to decide which expression to use based on whether or not the CellType is 1. (The syntax is similar to programming languages like C or C++)

The syntax of the ternary (aka ``if-then-else`` statement) is as follows:

.. code-block:: xml

    condition ? expression if condition is true : expression if condition false

.. warning::
    **Important:** If change the above expression to

    .. code-block::xml

        <AdditionalTerm>CellType<1 ? 0.01*F : 0.15*F</AdditionalTerm>

    we will get an XML parsing error. Why? This is because the XML parser will think
    that ``<1`` is the beginning of the new XML element. To fix this, you could
    use two approaches:

    1. Present your expression as ``CDATA``

    .. code-block:: xml

        <AdditionalTerm>
            <![CDATA[
                CellType < 1 ? 0.01*F : 0.15*F
            ]]>
        </AdditionalTerm>

    In this case, the XML parser will correctly interpret the expression enclosed
    between ``<![CDATA[`` and ``]]>`` .

    2. Replace XML using `equivalent Python syntax <replacing_cc3dml_with_equivalent_python_syntax.html>`_)
    in which case you would code the above XML element as the following Python statement:

    .. code-block:: python

        DiffusionDataElmnt.ElementCC3D('AdditionalTerm', {}, 'CellType<1 ? 0.01*F : 0.15*F')

    In summary, if you would like to use muParser for more flexibility in your XML,
    make sure to use this general syntax: 

    .. code-block:: xml

        <AdditionalTerm>
            <![CDATA[
                YOUR EXPRESSION
            ]]>
        </AdditionalTerm>

One thing to remember is that the computing time of the additional term
depends on the level of complexity of this term. Thus, you might get some
performance degradation for very complex expressions coded in muParser.

Similarly as in the case of ``FlexibleDiffusionSolverFE``, we may use the 
``<AutoscaleDiffusion>`` tag, which tells CC3D to automatically rescale the diffusion constant. 
See section `FlexibleDiffusionSolver <flexible_diffusion_solver.html>`_ or the `Appendix <appendix.html>`_ for more
information.

Each diffusion field can have a localized ``DiffusionConstant`` and/or ``DecayConstant`` for ``ReactionDiffusionSolverFE``. Behind the scenes, the max stable decay coefficient is a value just under 1 (approx. ``1 - 1.17549e-38``).
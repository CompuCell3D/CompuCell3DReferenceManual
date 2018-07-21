Steady State diffusion solver
-----------------------------

Often in the multi-scale simulations we have to deal with chemicals
which have drastically different diffusion constants. For slow diffusion
fields we can use standard explicit solvers (*e.g.* ``FlexibleDiffusionSolverFE``)
but once the diffusion constant becomes large
the number of extra calls to explicit solvers becomes so large that
solving diffusion equation using Forward-Euler based solvers is simply
impractical. In situations where the diffusion constant is so large that
the solution of the diffusion equation is not that much different from
the asymptotic solution (i.e. at :math:`t=\infty`) it is often more convenient to use
``SteadyStateDiffusion`` solver which solves Helmholtz equation:


where *F* is a source function of the coordinates - it is an input to
the equation, *k* is decay constant and *c* is the concentration. The F
function in CC3D is either given implicitely by specifying cellular
secretion or explicitely by specifying concentration *c* before solving
Helmholtz equation.

The CC3D stead state diffusion solvers are stable and allow solutions
for large values of diffusion constants.

The example syntax for the steady-state solver is shown below:

<Steppable Type="SteadyStateDiffusionSolver2D">

<DiffusionField Name="INIT">

<DiffusionData>

<FieldName>INIT</FieldName>

<DiffusionConstant>1.0</DiffusionConstant>

<DecayConstant>0.01</DecayConstant>

</DiffusionData>

<SecretionData>

<Secretion Type="Body1">1.0</Secretion>

</SecretionData>

<BoundaryConditions>

<Plane Axis="X">

<ConstantValue PlanePosition="Min" Value="10.0"/>

<ConstantValue PlanePosition="Max" Value="5.0"/>

</Plane>

<Plane Axis="Y">

<ConstantDerivaive PlanePosition="Min" Value="0.0"/>

<ConstantDerivaive PlanePosition="Max" Value="0.0"/>

</Plane>

</BoundaryConditions>

</DiffusionField>

</Steppable>

The syntax is is similar (actually, almost identical) to the syntax of
the FlexibleDiffusionSolverFE. The only difference is that while
FlexibleDiffusionSolverFE works in in both 2D and 3D users need to
specify the dimensionality of the steady state solver. We use

<Steppable Type="SteadyStateDiffusionSolver2D">

for 2D simulations when all the cells lie in the xy plane and

<Steppable Type="SteadyStateDiffusionSolver">

for simulations in 3D.

**We can use Python to control secretion in the steady state solvers but
it requires a little bit of low level coding**. Implementing secretion
in steady state diffusion solver is different from “regular” Forward
Euler solvers. Steady state solver takes secretion rate that is
specified at t=0 and returns the solution at t=∞. For alrge diffusion
constants we approximate solution to the PDE during one MCS by using
solution at t=∞. However that means that if at each MCS secretion
changes we have to do three things 1) zero entire field, 2) set
secretion rate 3) solve steady state solver. The reason we need to zero
entire field is because any value left in the field at mcs=N is
interpreted by the solver as a secretion constant at this location at
mcs=N+1. **Moreover the the secretion constant needs to have negative
value if we want to secrete positive amount of substance - this weird
requirements comes from the fact that we re using 3\ :sup:`rd` party
solver which inverts signs of the secretion constants.**

An example below demonstrates how we control secretion of the steady
state in Python. First we need to include tag <ManageSecretionInPython/>
in the XML definition of the solver:

<Steppable Type="SteadyStateDiffusionSolver2D">

<DiffusionField>

<ManageSecretionInPython/>

<DiffusionData>

<FieldName>FGF</FieldName>

<DiffusionConstant>1.00</DiffusionConstant>

<DecayConstant>0.00001</DecayConstant>

</DiffusionData>

</DiffusionField>

</Steppable>

In Python the code to control the secretion involves iteration over
every pixel and adjusting concentration (which as we mentioned will be
interpreted by the solver as a secretion constant) and we have to make
sure that we inherit from SecretionBasePy not SteppableBasePy to ensure
proper ordering of calls to Python module and the C++ diffusion solver.
**Important:** make sure you inherit from SecretionBasePy when you try
to manage secretion in the steady state solver using Python. This will
ensure proper ordering of calls to steppable and to C++ solver code.

**Important:** Once you use <ManageSecretionInPython/> tag in the XML
all secretion tags in the SecretionData will be ignored. In other words,
for this solver you cannot mix secretion specification in Python and
secretion specification in the XML.

def \_\_init\_\_(self,\_simulator,\_frequency=1):

SecretionBasePy.\_\_init\_\_(self,\_simulator,\_frequency)

def start(self):

| self.field=CompuCell.getConcentrationField\\
| (self.simulator,"FGF")

secrConst=10

for x,y,z in self.everyPixel(1,1,1):

cell=self.cellField[x,y,z]

if cell and cell.type==1:

self.field[x,y,z]=-secrConst

else:

self.field[x,y,z]=0.0

def step(self, mcs):

secrConst=mcs

for x,y,z in self.everyPixel(1,1,1):

cell=self.cellField[x,y,z]

if cell and cell.type==1:

self.field[x,y,z]=-secrConst

else:

self.field[x,y,z]=0.0

Notice that all the pixels that do not secrete have to be 0.0 as
mentioned above. **If you don’t initialize field values in the
non-secreting pixels to 0.0 you will get wrong results**. The above
code, with comments, is available in our Demo suite.

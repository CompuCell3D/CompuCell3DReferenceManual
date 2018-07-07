Potts Section
-------------

The first section of the .xml file defines the global parameters of the
lattice and the simulation.

.. code-block:: xml

        <Potts>
            <Dimensions x="101" y="101" z="1"/>
            <Anneal>0</Anneal>
            <Steps>1000</Steps>
            <FluctuationAmplitude>5</ FluctuationAmplitude >
            <Flip2DimRatio>1</Flip2DimRatio>
            <Boundary_y>Periodic</Boundary_y>
            <Boundary_x>Periodic</Boundary_x>
            <NeighborOrder>2</NeighborOrder>
            <DebugOutputFrequency>20</DebugOutputFrequency>
            <RandomSeed>167473</RandomSeed>
            <EnergyFunctionCalculator Type="Statistics">
            <OutputFileName Frequency="10">statData.txt</OutputFileName>
            <OutputCoreFileNameSpinFlips Frequency="1" GatherResults="" OutputAccepted="" OutputRejected="" OutputTotal="">
            </EnergyFunctionCalculator>
        </Potts>



This section appears at the beginning of the configuration file. Line
``<Dimensions x="101" y="101" z="1"/>`` declares the dimensions of the
lattice to be``101 x 101 x 1``, *i.e.*, the lattice is two-dimensional and
extends in the ``xy`` plane. The basis of the lattice is 0 in each
direction, so the ``101`` lattice sites in the ``x`` and ``y`` directions have
indices ranging from ``0`` to ``100``.`` <Steps>1000</Steps>`` tells CompuCell how
long the simulation lasts in MCS. After executing this number of steps,
CompuCell can run simulation at zero temperature for an additional
period. In our case it will run for ``<Anneal>10</Anneal>`` extra steps.
``FluctuationAmplitude`` parameter determines intrinsic fluctuation or
motility of cell membrane. **Fluctuation amplitude is a temperature
parameter in classical GGH model formulation. We have decided to use
FluctuationAmplitude term instead of temperature because using word
“temperature” to describe intrinsic motility of cell membrane was quite
confusing.**

In the above example, fluctuation amplitude applies to all cells in the
simulation. To define fluctuation amplitude separately for each cell
type we use the following syntax:

.. code-block:: xml

    <FluctuationAmplitude>
        <FluctuationAmplitudeParameters CellType="Condensing"\
        FluctuationAmplitude="10"/>
        <FluctuationAmplitudeParameters CellType="NonCondensing”\
        FluctuationAmplitude="5"/>
    </FluctuationAmplitude>



When CompuCell3D encounters expanded definition of ``FluctuationAmplitude``
it will use it in place of a global definition –

.. code-block:: xml

    <FluctuationAmplitude>5</ FluctuationAmplitude >

To complete the picture CompuCell3D allows users to set fluctuation
amplitude individually for each cell. Using Python scripting we write:

.. code-block:: python

    for cell in self.cellList:
        if cell.type==1:
            cell.fluctAmpl=20



When determining which value of fluctuation amplitude to use, CompuCell
first checks if fluctAmpl is non-negative. If this is the case it will
use this value as fluctuation amplitude. Otherwise it will check if
users defined fluctuation amplitude for cell types using expanded CC3DML
definition and if so it will use those values as fluctuation amplitudes.
Lastly it will resort to globally defined fluctuation amplitude
(Temperature). Thus, it is perfectly fine to use FluctuationAmplitude
CC3DML tags and set fluctAmpl for certain cells. In such a case
CompuCell3D will use fluctAmpl for cells for which users defined it and
for all other cells it will use values defined in the CC3DML.

In GGH model, the fluctuation amplitude is determined taking into
account fluctuation amplitude of “source” (expanding) cell and
“destination” (being overwritten) cell. Currently CompuCell3D supports 3
type functions used to calculate resultant fluctuation amplitude (those
functions take as argument fluctuation amplitude of “source” and
“destination” cells and return fluctuation amplitude that is used in
calculation of pixel-copy acceptance). The 3 functions are Min, Max, and
ArithmeticAverage and we can set them using the following option of the
Potts section:

<Potts>

<FluctuationAmplitudeFunctionName>

Min

</FluctuationAmplitudeFunctionName>

…

</Potts>

By default we use Min function. Notice that if you use global
fluctuation amplitude definition (Temperature) it does not really matter
which function you use. The differences arise when “source” and
“destination” cells have different fluctuation amplitudes.

The above concepts are best illustrated by the following example:

<PythonScript>Demos/FluctuationAmplitude/FluctuationAmplitude.py\\

</PythonScript>

<Potts>

<Dimensions x="100" y="100" z="1"/>

<Steps>10000</Steps>

<FluctuationAmplitude>5</FluctuationAmplitude>

<FluctuationAmplitudeFunctionName>ArithmeticAverage\\

</FluctuationAmplitudeFunctionName>

<NeighborOrder>2</NeighborOrder>

</Potts>

Where in the CC3DML section we define global fluctuation amplitude and
we also use ArithmeticAverage function to determine resultant
fluctuation amplitude for the pixel copy.

In python script we will periodically set higher fluctuation amplitude
for lattice quadrants so that when running the simulation we can see
that cells belonging to different lattice quadrants have different
membrane fluctuations:

class FluctuationAmplitude(SteppableBasePy):

def \_\_init\_\_(self,\_simulator,\_frequency=1):

SteppableBasePy.\_\_init\_\_(self,\_simulator,\_frequency)

self.quarters=[[0,0,50,50],[0,50,50,100],\\

[50,50,100,100],[50,0,100,50]]

self.steppableCallCounter=0

def step(self, mcs):

quarterIndex=self.steppableCallCounter % 4

quarter=self.quarters[quarterIndex]

for cell in self.cellList:

if cell.xCOM>=quarter[0] and cell.yCOM>=quarter[1] and\\

cell.xCOM<quarter[2] and cell.yCOM<quarter[3]:

cell.fluctAmpl=50

else:

#this means CompuCell3D will use globally defined FluctuationAmplitude

cell.fluctAmpl=-1

self.steppableCallCounter+=1

Assigning negative fluctuationAmplitude cell.fluctAmpl=-1 is interpreted
by CompuCell3D as a hint to use fluctuation amplitude defined in the
CC3DML.

**The section below describes Temperature and CellMotility tags which
are beibng deprecated (however cor compatibility reasons we still
support those):**

The first section of the .xml file defines the global parameters of the
lattice and the simulation.

<Potts>

<Dimensions x="101" y="101" z="1"/>

<Anneal>0</Anneal>

<Steps>1000</Steps>

<Temperature>5</Temperature>

<Flip2DimRatio>1</Flip2DimRatio>

<Boundary\_y>Periodic</Boundary\_y>

<Boundary\_x>Periodic</Boundary\_x>

<NeighborOrder>2</NeighborOrder>

<DebugOutputFrequency>20</DebugOutputFrequency>

<RandomSeed>167473</RandomSeed>

<EnergyFunctionCalculator Type="Statistics">

<OutputFileName Frequency="10">statData.txt</OutputFileName>

| <OutputCoreFileNameSpinFlips Frequency="1" GatherResults=""
| OutputAccepted="" OutputRejected="" OutputTotal="">

statDataSingleFlip

</OutputCoreFileNameSpinFlips>

</EnergyFunctionCalculator>

</Potts>

This section appears at the beginning of the configuration file. Line
<Dimensions x="101" y="101" z="1"/> declares the dimensions of the
lattice to be 101 x 101 x 1, i.e., the lattice is two-dimensional and
extends in the xy plane. The basis of the lattice is 0 in each
direction, so the 101 lattice sites in the x and y directions have
indices ranging from 0 to 100. <Steps>1000</Steps> tells CompuCell how
long the simulation lasts in MCS. After executing this number of steps,
CompuCell can run simulation at zero temperature for an additional
period. In our case it will run for <Anneal>10</Anneal> extra steps.
Setting the temperature is as easyas writing
<Temperature>5</Temperature>.

We can also set temperature (or in other words cell motility)
individually for each cell type. The syntax to do this is following:

<CellMotility>

<MotilityParameters CellType="Condensing" Motility="10"/>

<MotilityParameters CellType="NonCondensing" Motility="5"/>

</CellMotility>

You may use it in the Potts section in place of <Temperature> .

Based on discussion about the difference between pixel-flip attempts and
MCS (see “Introduction to CompuCell3D”) we can specify how many pixel
copies should be attempted in every MCS. We specify this number
indirectly by specifying the Flip2DimRatio -
<Flip2DimRatio>1</Flip2DimRatio>, which tells CompuCell that it should
make 1 x number of lattice sites attempts per MCS – in our case one MCS
is 101x101x1 pixel-copy attempts. To set 2.5x101x101x1 pixel-copy
attempts per MCS you would write <Flip2DimRatio>2.5</Flip2DimRatio>.

The next line specifies the neighbor order. The higher neighbor order
the longer the Euclidian distance from a given pixel. In previous
versions of CompuCell3D we have been using <FlipNeighborMaxDistance> or
<Depth> (in Contact energy plugins) flag to accomplish same task. Since
now CompuCell3D supports two kinds of lattices it would be inconvenient
to change distances. It is much easier to think in terms n-th nearest
neighbors. For the backwards compatibility we still support old flags
but we discourage its use, especially that in the future we might
support more than just two lattice types.

Using nearest neighbor interactions may cause artifacts due to lattice
anisotropy. The longer the interaction range, the more isotropic the
simulation and the slower it runs. In addition, if the interaction range
is comparable to the cell size, you may generate unexpected effects,
since non-adjacent cells will contact each other.

On hex lattice those problems seem to be less seveare and there
1\ :sup:`st` or 2\ :sup:`nd` nearest neighbor usually are sufficient.

The Potts section also contains tags called <Boundary\_y> and
<Boundary\_x>.These tags impose boundary conditions on the lattice. In
this case the x and y axes are **periodic**
(<Boundary\_x>Periodic</Boundary\_x>) so that *e.g.* the pixel with x=0,
y=1, z=1 will neighbor the pixel with x=100, y=1, z=1. If you do not
specify boundary conditions CompuCell will assume them to be of type
**no-flux**, *i.e.* lattice will not be extended. The conditions are
independent in each direction, so you can specify any combination of
boundary conditions you like.

DebugOutputFrequency is used to tell CompuCell3D how often it should
output text information about the status of the simulation. This tag is
optional.

RandomSeed is used to initialize random number generator. If you do not
do this all simulations will use same sequence of random numbers.
Something you may want to avoid in the real simulations but is very
useful while debugging your models.

EnergyFunctionCalculator is another option of Potts object that allows
users to output statistical data from the simulation for further
analysis.

**Important:** CC3D has the option to run in the parallel mode but
output from energy calculator will only work when running in a single
CPU mode.

The OutputFileName tag is used to specify the name of the file to which
CompuCell3D will write average changes in energies returned by each
plugins with corresponding standard deviations for those MCS whose
values are divisible by the Frequency argument. Here it will write these
data every 10 MCS.

A second line with OutputCoreFileNameSpinFlips tag is used to tell
CompuCell3D to output energy change for every plugin, every pixel-copy
for MCS' divisible by the frequency. Option GatherResults=”” will ensure
that there is only one file written for accepted (OutputAccepted),
rejected (OutputRejected)and accepted and rejected (OutputTotal) pixel
copies. If you will not specify GatherResults CompuCell3D will output
separate files for different MCS's and depending on the Frequency you
may end up with many files in your directory.

One option of the Potts section that we have not used here is the
ability to customize acceptance function for Metropolis algorithm:

<Offset>-0.1</Offset>

<KBoltzman>1.2</KBoltzman>

This ensures that pixel copies attempts that increase the energy of the
system are accepted with probability

where δ and *k* are specified by Offset and KBoltzman tags respectively.
By default δ=0 and *k=1*.

As an alternative to exponential acceptance function you may use a
simplified version which is essentially 1 order expansion of the
exponential:

To be able to use this function all you need to do is to add the
following line in the Pots section:

<AcceptanceFunctionName>FirstOrderExpansion</AcceptanceFunctionName>
